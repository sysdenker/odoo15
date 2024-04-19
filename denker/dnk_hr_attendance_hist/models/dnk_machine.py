# -*- coding: utf-8 -*-
###################################################################################
#
#    This program is free software: you can modify
#    it under the terms of the GNU Affero General Public License (AGPL) as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###################################################################################
import pytz
import sys
from datetime import datetime,date, timedelta
import logging
import binascii
import os
import platform
import subprocess
import time

from odoo import api, fields, models
from odoo import _
from odoo.exceptions import UserError, ValidationError
_logger = logging.getLogger(__name__)
try:
    from zk import ZK, const
except ImportError:
    _logger.error("Unable to import pyzk library. Try 'pip3 install pyzk'.")

class ZkMachine(models.Model):
    _name = 'dnk.zk.machine'
    _description = "ZK Machine"

    name = fields.Char(string='Name', required=True)
    dnk_ip = fields.Char(string='Machine IP', required=True)
    port_no = fields.Integer(string='Port No', required=True, default="4370")
    address_id = fields.Many2one('res.partner', string='Working Address')
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.user.company_id.id)
    zk_timeout = fields.Integer(string='ZK Timeout', required=True, default="120")
    zk_after_date =  fields.Datetime(string='Attend Start Date', help='If provided, Attendance module will ignore records before this date.', required=True, default='2017-01-01 00:06:00')

    def device_connect(self, zkobj):
        try:
            device_connection =  zkobj.connect()
            return device_connection
        except:
            _logger.info("zk.exception.ZKNetworkError: can't reach device.")
            # raise UserError("Connection To Device cannot be established.")
            return False

    # @api.multi
    # def device_connect(self, zkobj):
    #     for i in range(10):
    #         try:
    #             device_connection =  zkobj.connect()
    #             return device_connection
    #         except:
    #             _logger.info("zk.exception.ZKNetworkError: can't reach device.")
    #             device_connection = False
    #     return False


    def try_connection(self):
        for r in self:
            device_ip = r.dnk_ip
            if platform.system() == 'Linux':
                response = os.system("ping -c 1 " + device_ip)
                if response == 0:
                    raise UserError("Biometric Device is Up/Reachable.")
                else:
                    raise UserError("Biometric Device is Down/Unreachable.")
            else:
                prog = subprocess.run(["ping", device_ip], stdout=subprocess.PIPE)
                if 'unreachable' in str(prog):
                    raise UserError("Biometric Device is Down/Unreachable.")
                else:
                    raise UserError("Biometric Device is Up/Reachable.")

    def clear_attendance(self):
        for info in self:
            try:
                device_ip = info.name
                device_port = info.port_no
                timeout = info.zk_timeout
                try:
                    zk_device = ZK(device_ip, port = device_port , timeout=timeout, password=0, force_udp=False, ommit_ping=False)
                except NameError:
                    raise UserError(_("Pyzk module not Found. Please install it with 'pip3 install pyzk'."))
                    device_connection = self.device_connect(zk_device)
                if device_connection:
                    device_connection.enable_device()
                    clear_data = zk_device.get_attendance()
                    if clear_data:
                        #device_connection.clear_attendance()
                        self._cr.execute("""delete from dnk_machine_attendance""")
                        device_connection.disconnect()
                        raise UserError(_('Attendance Records Deleted.'))
                    else:
                        raise UserError(_('Unable to clear Attendance log. Are you sure attendance log is not empty.'))
                else:
                    raise UserError(_('Unable to connect to Attendance Device. Please use Test Connection button to verify.'))
            except:
                raise ValidationError('Unable to clear Attendance log. Are you sure attendance device is connected & record is not empty.')

    def zkgetuser(self, zk_device):
        try:
            users = zk_device.get_users()
            return users
        except:
            raise UserError(_('Unable to get Users.'))

    @api.model
    def cron_download_zk_machine_data(self):
        machines = self.env['dnk.zk.machine'].search([])
        for machine in machines :
            #machine.zk_after_date = date.today()
            machine.download_attendance()


    def update_attendance(self):
        hr_attendance = self.env['hr.attendance']
        hr_attendance.dnk_update_attendance(self)
        return True

    def download_attendance(self):
        _logger.info("++++++++++++Cron Executed++++++++++++++++++++++")
        zk_attendance = self.env['dnk.machine.attendance']
        hr_attendance = self.env['hr.attendance']
        for info in self:
            device_ip = info.dnk_ip
            device_port = info.port_no
            timeout = info.zk_timeout
            #Pruebas
            #hr_attendance.dnk_crate_att("2020-01-22")
            #hr_attendance.dnk_create_att_from_date("2020-01-25","2020-01-25")
            #hr_attendance.dnk_update_attendance(self)
            #return True
            try:
                zk_device = ZK(device_ip, port=device_port, timeout=timeout, password=0, force_udp=False, ommit_ping=False)
            except NameError:
                raise UserError(_("Pyzk module not Found. Please install it with 'pip3 install pyzk'."))
            _logger.info("Trying to device_connect" + info.name)
            device_connection = info.device_connect(zk_device)
            if device_connection:
                try:
                    device_users = device_connection.get_users()
                except:
                    device_users = False
                try:
                    device_attendances = device_connection.get_attendance()
                except:
                    device_attendances = False

                ####
                ### VOY A HACER MI PROPIO CICLO, A VER QUÉ TAL ME VA
                ###
                if device_attendances:
                    for device_attendance in device_attendances:
                        device_attendance_timestamp = device_attendance.timestamp
                        device_attendance_comp = datetime.strptime(device_attendance_timestamp.strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')
                        local_tz = pytz.timezone(self.env.user.partner_id.tz or 'GMT')
                        local_dt = local_tz.localize(device_attendance_comp, is_dst=None)
                        utc_dt = local_dt.astimezone(pytz.utc)
                        utc_dt = utc_dt.strftime("%Y-%m-%d %H:%M:%S")
                        device_attendance_timestamp_utc = datetime.strptime(utc_dt, "%Y-%m-%d %H:%M:%S")
                        #Éste es ya sin zona horaria
                        if device_attendance_timestamp != False and device_attendance_timestamp_utc > datetime.strptime(info.zk_after_date,'%Y-%m-%d %H:%M:%S'):
                            if device_attendance.user_id and device_attendance_timestamp:
                                duplicate_attendance_ids = zk_attendance.search([('dnk_device_user_id', '=', device_attendance.user_id), ('punching_time', '=', device_attendance_timestamp.strftime('%Y-%m-%d %H:%M:%S'))])
                                if len(duplicate_attendance_ids)> 0:
                                    continue
                                else:
                                    zk_attendance.create({'dnk_device_user_id': device_attendance.user_id,
                                                        'attendance_type': str(device_attendance.status),
                                                        'punch_type': str(device_attendance.punch),
                                                        'punching_time': device_attendance_timestamp,
                                                        'punching_time_utc': device_attendance_timestamp_utc,
                                                        'dnk_device_id': info.id})
                    #hr_attendance.dnk_update_attendance(self)
                else:
                    continue
                    _logger.info("No attendances found in Attendance Device to Download. Device: " + info.name)
                    device_connection.disconnect
                    # raise UserError(_('No attendances found in Attendance Device to Download.'))
                    # device_connection.enable_device() #Enable Device Once Done.
                    # device_connection.disconnect

            else:
                continue
                _logger.info("Unable to connect to Attendance Device. Please use Test Connection button to verify. Device: " + info.name)
        return True
