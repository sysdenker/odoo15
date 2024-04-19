# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import pytz
from datetime import datetime, timedelta, date
from dateutil.relativedelta import relativedelta

from odoo import models, fields, api, exceptions, _, SUPERUSER_ID

class HrEmployeeBase(models.AbstractModel):
    _inherit = "hr.employee.base"

    def _attendance_action_change(self):
        self.ensure_one()
        action_date = fields.Datetime.now()

        now = fields.Datetime.now()
        now_utc = pytz.utc.localize(now)
        tz = pytz.timezone(self.tz)
        now_tz = now_utc.astimezone(tz)
        ini_date = now.date()
        ini_date_tz = now_tz.date()

        str_date_tz = ini_date_tz.strftime('%Y-%m-%d')
        str_ini_date_tz_1 = str_date_tz + " 00:00:00"
        str_ini_date_tz_2 = str_date_tz + " 00:00:01"
        str_fin_date_tz = str_date_tz + " 23:59:59"

        check_ini_datetime = datetime.strptime (str_ini_date_tz_1, "%Y-%m-%d %H:%M:%S")
        check_ini_datetime2 = datetime.strptime (str_ini_date_tz_2, "%Y-%m-%d %H:%M:%S")
        check_fin_datetime = datetime.strptime (str_fin_date_tz, "%Y-%m-%d %H:%M:%S")

        local_check_ini = tz.localize(check_ini_datetime, is_dst=None)
        local_check_ini2 = tz.localize(check_ini_datetime2, is_dst=None)
        local_check_fin = tz.localize(check_fin_datetime, is_dst=None)
        utc_check_ini = local_check_ini.astimezone(pytz.utc)
        utc_check_ini2 = local_check_ini2.astimezone(pytz.utc)
        utc_check_fin = local_check_fin.astimezone(pytz.utc)

        att_stat = ""
        week_day = now_tz.weekday()
        calendar_att =  self.env['resource.calendar.attendance'].search(
            [('calendar_id', '=', self.resource_calendar_id.id),('dayofweek', '=',week_day)],limit=1)
        if calendar_att:
            hour_in = utc_check_ini + timedelta(hours=calendar_att.hour_from)
            if hour_in >= now_utc:
                att_stat = "A tiempo-Sin Salida"
            elif hour_in + timedelta(minutes=10) >= now_utc:
                att_stat = "Tolerancia-Sin Salida"
            else:
                att_stat = "Retardo-Sin Salida"

        # Primero voy a buscar registro automático de asistencia
        attendance = self.env['hr.attendance'].search(
            [('employee_id', '=', self.id), ('check_in', '=', utc_check_ini2),
            ('dnk_attendance_stat', '=', 'Ausencia')], limit=1)
        if attendance:
            # Es registro automático, es como  no tener entrada
            attendance.check_out = now
            attendance.check_in = now
            attendance.dnk_attendance_stat = att_stat
            return attendance
        else:
            # Ya no hay registro automático, voy a buscar registro del día
            # Para actualizar salida
            attendance = self.env['hr.attendance'].search(
                [('employee_id', '=', self.id), ('check_in', '>=', utc_check_ini2),
                ('check_out', '<=', utc_check_fin)], limit=1)
            if attendance:
                attendance.check_out = now
                attendance.dnk_attendance_stat = attendance.dnk_attendance_stat.replace("-Sin Salida", "")
                return attendance

            else:
                # No hay registro automático, tendría que crearlo, se supone que no debería entrar aquí-
                vals = {
                    'employee_id': self.id,
                    'check_in': now,
                    'check_out': now,
                    'dnk_attendance_stat': att_stat,
                }
                return self.env['hr.attendance'].create(vals)



    def _attendance_action(self, next_action):
        self.ensure_one()
        employee = self.sudo()
        if not employee.dnk_homeoffice:
            return {'warning': _('Web attendance registration not allowed. Please contact your administrator')}
        else:
            # Validar qué días se tiene permitido
            if not employee.dnk_hoffice_att_ids:
                return {'warning': _('Web attendance registration not allowed Today. Please contact your administrator')}
            else:
                print(employee.dnk_hoffice_att_ids)
                days_allowed = []
                for dweek in employee.dnk_hoffice_att_ids:
                    days_allowed.append(dweek.dayofweek)

                now = fields.Datetime.now()
                now_utc = pytz.utc.localize(now)
                tz = pytz.timezone(self.tz)
                now_tz = now_utc.astimezone(tz)
                now_weekday = now_tz.weekday()

                if str(now_weekday) not in days_allowed:
                    return {'warning': _('Web attendance registration not allowed Today. Please contact your administrator')}


        # print("Next Action", next_action)
        res = super(HrEmployeeBase, self)._attendance_action(next_action)
        return res
