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
from odoo import tools
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

class HrEmployee(models.Model):
    _inherit = 'hr.employee'
    dnk_device_user_id = fields.Integer(string='Biometric Device ID')

    @api.constrains('dnk_device_user_id')
    def check_unique_deviceid(self):
        records = self.env['hr.employee'].search([('dnk_device_user_id', '=', self.dnk_device_user_id),('dnk_device_user_id', '!=', False ),('id', '!=', self.id)])
        if records:
            raise UserError(_('Another User with same Biometric Device ID already exists.'))


class ZkMachine(models.Model):
    _name = 'dnk.machine.attendance'
    _description = "Machine Attendance"

    #_inherit = 'hr.attendance'

    #@api.constrains('check_in', 'check_out')
    #def _check_validity(self):
    #    """overriding the __check_validity function for employee attendance."""
    #    pass

    dnk_device_user_id = fields.Integer(string='Biometric User ID', index=True)
    punch_type = fields.Selection([('0', 'Check In'),
                                   ('1', 'Check Out'),
                                   ('2', 'Break Out'),
                                   ('3', 'Break In'),
                                   ('4', 'Overtime In'),
                                   ('5', 'Overtime Out')],
                                  string='Punching Type')

    attendance_type = fields.Selection([('1', 'Finger'),
                                        ('15', 'Face'),
                                        ('2','Type_2'),
                                        ('3','Password'),
                                        ('4','Card')], string='Category')
    punching_time = fields.Datetime(string='Punching Time', index=True)
    punching_time_utc = fields.Datetime(string='Punching Time UTC')
    dnk_device_id = fields.Integer(string='Device ID', index=True)
    dnk_is_sync = fields.Integer(string='Sync', default=0)


class ReportZkDevice(models.Model):
    _name = 'dnk.report.daily.attendance'
    _description = "Daily Atte Report"
    _auto = False
    _order = 'punching_day desc'

    name = fields.Many2one('hr.employee', string='Employee')
    punching_day = fields.Date(string='Date')
    attendance_type = fields.Selection([('1', 'Finger'),
                                        ('15', 'Face'),
                                        ('2','Type_2'),
                                        ('3','Password'),
                                        ('4','Card')],
                                       string='Category')
    punch_type = fields.Selection([('0', 'Check In'),
                                   ('1', 'Check Out'),
                                   ('2', 'Break Out'),
                                   ('3', 'Break In'),
                                   ('4', 'Overtime In'),
                                   ('5', 'Overtime Out')], string='Punching Type')
    punching_time = fields.Datetime(string='Punching Time')

    def init(self):
        tools.drop_view_if_exists(self._cr, 'dnk_report_daily_attendance')
        self._cr.execute("""
            CREATE OR REPLACE VIEW dnk_report_daily_attendance AS (
                SELECT
                    min(z.id) AS id,
                    z.dnk_device_user_id AS name,
                    z.write_date AS punching_day,
                    z.attendance_type AS attendance_type,
                    z.punching_time AS punching_time,
                    z.punch_type AS punch_type
                FROM dnk_machine_attendance z
                    LEFT JOIN hr_employee e ON (z.dnk_device_user_id=e.dnk_device_user_id)
                GROUP BY
                    z.dnk_device_user_id,
                    z.write_date,
                    z.attendance_type,
                    z.punch_type,
                    z.punching_time
            )
        """)
