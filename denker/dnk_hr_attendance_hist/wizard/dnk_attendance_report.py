# -*- coding: utf-8 -*-

import time
from datetime import datetime,date, timedelta
from odoo import api, models
from dateutil.parser import parse
from odoo.exceptions import UserError
import pytz


class AttendanceReport(models.AbstractModel):
    _name = 'report.dnk_hr_attendance_hist.dnk_attendance_report'
    _description = "Attendance Report"

    def _get_data_from_report(self, data, employee_ids):
        res = []
        Attendance = self.env['hr.attendance']
        if employee_ids and 'dnk_date_from' in data and 'dnk_date_to' in data:
            for employee in self.env['hr.employee'].browse(employee_ids):
                colores_comp = ['#cccccc', '#00467f','#cccccc','#cccccc','#c81f3f','#ffd204',];
                #colores_comp = ['0-Default', '1-ESTATEC', '2-Vacio', '3-SCD', '4-EXTRUPAC', '5-Tecnogoma'];
                colores_font = ['#000000', '#ffffff','#000000','#000000','#ffffff','#000000',];
                att_inc = 0
                att_aus = 0
                att_ret = 0
                total_hours = 0
                res.append({
                    'employee_id' : employee,
                    'employee_name': employee.name,
                    'department': employee.department_id.name,
                    'company': employee.company_id,
                    'company_logo': employee.company_id.logo,
                    'company_name': employee.company_id.name,
                    'company_color': colores_comp[employee.company_id.id],
                    'company_color_fnt': colores_font[employee.company_id.id],
                    'data':[],
                    'total':[],
                    'total_hrs':[],
                    'total_aus':[],
                    'total_ret':[]
                    })
                dias_sem_esp = ['Lunes', 'Martes','Miércoles','Jueves','Viernes','Sábado','Domingo'];
                for att in Attendance.search([('employee_id', '=', employee.id),
                    ('check_in', '>=', data['dnk_date_from']),
                    ('check_out', '<=', data['dnk_date_to'])], order="check_in asc"):

                        # check_in_utc = datetime.strptime(att.check_in, '%Y-%m-%d %H:%M:%S')
                        # check_out_utc = datetime.strptime(att.check_out, '%Y-%m-%d %H:%M:%S')

                        check_in_utc = att.check_in
                        check_out_utc = att.check_out

                        local_tz = pytz.timezone(self.env.user.partner_id.tz or 'GMT')
                        local_dt = check_in_utc.replace(tzinfo=pytz.utc).astimezone(local_tz)
                        local_tz.normalize(local_dt)
                        check_in = local_tz.normalize(local_dt)

                        local_dt = check_out_utc.replace(tzinfo=pytz.utc).astimezone(local_tz)
                        local_tz.normalize(local_dt)
                        check_out = local_tz.normalize(local_dt)

                        date_in = check_in.strftime("%Y-%m-%d %H:%M:%S")[0:10]
                        check_in_str = check_in.strftime("%H:%M:%S")
                        check_out_str = check_out.strftime("%H:%M:%S")
                        color = "#808080" #Grisecito
                        if att.dnk_attendance_stat:
                            if att.dnk_attendance_stat == 'Ausencia':
                                color = "#800000" #Rojito
                                att_inc += 1
                                att_aus += 1
                            elif att.dnk_attendance_stat.find('Retardo') != -1:
                                color = "#800000" #Rojito
                                att_inc += 1
                                att_ret += 1
                            elif att.dnk_attendance_stat.find('Tolerancia') != -1:
                                color = "#ff9900" #Amarillito
                            elif att.dnk_attendance_stat.find('A tiempo') != -1:
                                color = "#009933" #Verdecito
                            elif att.dnk_attendance_stat.find('Cumpleaños') != -1:
                                color = "#009933" #Verdecito
                            else :
                                color = "#808080" #Grisecito
                        if att.worked_hours and att.worked_hours > 0:
                            worked_hours = str(timedelta(seconds=att.worked_hours*3600))
                            worked_hours = "0"+worked_hours if len(worked_hours) == 7 else worked_hours
                            total_hours = total_hours + att.worked_hours
                        else :
                            worked_hours = "00:00:00"
                        res[len(res)-1]['data'].append({
                            'date_in':  date_in,
                            'dia_sem': dias_sem_esp[check_in.weekday()],
                            'check_in': check_in_str,
                            'check_out': check_out_str,
                            'dnk_attendance_stat':att.dnk_attendance_stat,
                            'dnk_device_name': att.dnk_device_id.name if att.dnk_device_id.name else '',
                            'worked_hours': worked_hours[0:-3],
                            'color_stat': color,
                        })
                total_hours_str = str(timedelta(seconds=total_hours*3600))[0:-3]
                total_hours_str =  "0"+total_hours_str if len(total_hours_str) == 7 else total_hours_str
                res[len(res)-1]['total_hrs'] = "0"+ str(timedelta(seconds=total_hours*3600))[0:-3]
                res[len(res)-1]['total'] = att_inc
                res[len(res)-1]['total_aus'] = att_aus
                res[len(res)-1]['total_ret'] = att_ret
        return res

    @api.model
    def _get_report_values(self, docids, data=None):
        if not data.get('form'):
            raise UserError(_("Form content is missing, this report cannot be printed."))


        attendance_report = self.env['ir.actions.report']._get_report_from_name('dnk_hr_attendance_hist.dnk_attendance_report')
        employees = data['context']['active_ids']
        form =  data['form']
        return {
            'doc_ids': self.ids,
            'dnk_date_from': data['form']['dnk_date_from'],
            'dnk_date_to': data['form']['dnk_date_to'],
            'get_data_from_report': self._get_data_from_report(form, employees),
        }
