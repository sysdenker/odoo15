# -*- coding: utf-8 -*-
import time
from odoo import models, api, fields, _
from dateutil.parser import parse

class PrintAttendanceReport(models.TransientModel):

    _name = 'dnk.wizard.atendance.report'
    _description = 'Attendance Report'

    dnk_date_from = fields.Date(string='- Start Date')
    dnk_date_to = fields.Date(string='- End Date')

    def check_report(self):
        self.ensure_one()
        [data] = self.read()
        data['employees'] = self.env.context.get('active_ids', [])
        employees = self.env['hr.employee'].browse(data['employees'])
        datas = {
            'ids': [],
            'model': 'hr.employee',
            'form': data
        }
        return self.env.ref('dnk_hr_attendance_hist.dnk_attendance_report_reg').with_context(from_transient_model=True).report_action(employees, data=datas)

    def print_report(self, data):
        data['form'].update(self.read(['dnk_date_from', 'dnk_date_to'])[0])
        return self.env.ref('dnk_hr_attendance_hist.dnk_attendance_report_reg').report_action(self, data=data)
