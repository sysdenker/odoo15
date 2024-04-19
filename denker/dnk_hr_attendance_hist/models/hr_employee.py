# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions, _, SUPERUSER_ID
from datetime import datetime,date, timedelta
import pytz

class HrEmployee(models.Model):
    _inherit = "hr.employee"

    dnk_homeoffice = fields.Boolean('Home Office Allowed?', default=False)
    dnk_hoffice_att_ids = fields.Many2many(
        'resource.calendar.attendance', string = '- Work days at home',
        copy=True)

    

    def attendance_action_change(self):
        #Voy a tener que rehacer la función, no me interesa el funcionamiento nativo

        if len(self) > 1:
            raise exceptions.UserError(_('Cannot perform check in or check out on multiple employees.'))


        action_date = fields.Datetime.now()
        action_date_obj = datetime.strptime(action_date,'%Y-%m-%d %H:%M:%S')
        ini_datetime = datetime.strptime(action_date,'%Y-%m-%d %H:%M:%S')
        local_tz = pytz.timezone(self.env.user.partner_id.tz or 'GMT')
        local_ini_dt = local_tz.localize(ini_datetime, is_dst=None)
        local_time = ini_datetime.replace(tzinfo=pytz.utc).astimezone(local_tz)
        ini_date = local_time.strftime('%Y-%m-%d')
        #print ("ini_date")
        #print (ini_date)


        ini_datetime = datetime.strptime(ini_date + " 00:00:00",'%Y-%m-%d %H:%M:%S')
        end_datetime = datetime.strptime(ini_date + " 23:59:59",'%Y-%m-%d %H:%M:%S')
        local_tz = pytz.timezone(self.env.user.partner_id.tz or 'GMT')
        local_ini_dt = local_tz.localize(ini_datetime, is_dst=None)
        local_end_dt = local_tz.localize(end_datetime, is_dst=None)
        utc_dt = local_ini_dt.astimezone(pytz.utc)
        utc_dt = utc_dt.strftime("%Y-%m-%d %H:%M:%S")
        ini_date_utc = datetime.strptime(utc_dt, "%Y-%m-%d %H:%M:%S")
        utc_dt = local_end_dt.astimezone(pytz.utc)
        utc_dt = utc_dt.strftime("%Y-%m-%d %H:%M:%S")
        end_date_utc = datetime.strptime(utc_dt, "%Y-%m-%d %H:%M:%S")
        week_day = ini_datetime.weekday()
        #print (self.id)
        # Ya tengo los rangos del día.
        #print ("ini_date_utc y end_date_utc", ini_date_utc,end_date_utc )

        #Checo que tenga horario asignado y que el horario tenga habilitado HO en el día asignado
        calendar_att =  self.env['resource.calendar.attendance'].search([('calendar_id', '=', self.resource_calendar_id.id),('dayofweek', '=',week_day)],limit=1)
        if calendar_att and not calendar_att.dnk_homeoffice:
            raise exceptions.UserError(_('Tu horario asignado no tiene habilitado el registro de asistencia manual.'))
        #Busco si ya tengo registro de cualquier manera, el automático u otro manual

        search_att = self.env['hr.attendance'].search([('employee_id', '=', self.id),('check_in', '>=', ini_date_utc.strftime("%Y-%m-%d %H:%M:%S")),('check_in', '<=', end_date_utc.strftime("%Y-%m-%d %H:%M:%S"))], limit=1)
        if search_att:
            att_stat = search_att.dnk_attendance_stat
            #Quiere decir que ya había registrado entrada, entonces actualizo salida.
            if search_att.check_in == action_date_obj.strftime("%Y-%m-%d %H:%M:%S"):
                search_att.write({
                    'check_out':action_date,
                    })
            else:
                if search_att.dnk_attendance_stat and search_att.dnk_attendance_stat.find('-Sin Salida') != -1:
                    att_stat=att_stat[0:att_stat.find('-Sin Salida')]
                else :
                    att_stat= search_att.dnk_attendance_stat
                search_att.write({
                    'check_out':action_date,
                    'dnk_attendance_stat':att_stat
                    })
            return search_att
        else:
            #No encontré asisrtencia, debo generarla
            att_stat = ""
            if calendar_att and calendar_att.dnk_homeoffice:
                    calendar_hour_in = ini_date_utc + timedelta(hours=calendar_att.hour_from)
                    calendar_hour_in = calendar_hour_in + timedelta(minutes=1)
                    #print ("calendar_hour_in y action_date_obj ")
                    #print (calendar_hour_in)
                    #print (action_date_obj)
                    if calendar_hour_in >= action_date_obj:
                        att_stat = "A tiempo"
                    elif calendar_hour_in + timedelta(minutes=10) >= action_date_obj:
                        att_stat = "Tolerancia"
                    else:
                        att_stat = "Retardo"
                    vals = {
                        'employee_id': self.id,
                        'check_in': action_date,
                        'check_out': action_date,
                        'dnk_attendance_stat': att_stat+ "-Sin Salida"
                    }
                    return self.env['hr.attendance'].create(vals)


        #attendance = self.env['hr.attendance'].search([('employee_id', '=', self.id), ('check_out', '=', False)], limit=1)
        #    if attendance:
        #        attendance.check_out = action_date
        #print ("Entré bien a attendance_action_change")
        #print (self)
        #att = super(HrEmployee, self).attendance_action_change()
        #if att:
        #    values = {
        #        'check_out' :  att.check_in
        #    }
        #    att.write(values)
        return False
