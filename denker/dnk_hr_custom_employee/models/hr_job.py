
# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class HrJob(models.Model):
    _inherit = 'hr.job'

    # register/deregister an employee
    dnk_plantilla_autorizada = fields.Integer('- Plantilla Autorizada')
    dnk_vacantes_abiertas = fields.Integer(
        '- Plantilla Faltante', compute='_compute_vacantes_abiertas', store=True, readonly=True)
    employee_register_ids = fields.One2many(
        comodel_name='hr.employee.register', inverse_name='job_id',
        string='- Employee register', help='Employee register history for statistic use.')

    employee_deregister_ids = fields.One2many(
        comodel_name='hr.employee.register', inverse_name='job_id',
        string='- Employee deregister', help='Employee deregister history for statistic use.')
    sequence = fields.Integer('- Sequence', help="Job Order")

    @api.onchange('dnk_plantilla_autorizada')
    @api.depends('dnk_plantilla_autorizada', 'no_of_employee')
    def _compute_vacantes_abiertas(self):
        for rec in self:
            rec.dnk_vacantes_abiertas = rec.dnk_plantilla_autorizada - rec.no_of_employee

    def _cron_update_plantilla_aut(self):
        jobs = self.env['hr.job'].search([])
        for job in jobs:
            job._compute_vacantes_abiertas()




class EmployeeRecruitmentHistory(models.Model):
    _name = 'hr.employee.register'
    _description = 'Employee register'
    _order = 'register_date'

    name = fields.Char(string='Employee', required=True, size=32)
    job_id = fields.Many2one('hr.job', 'Job', required=True)
    company_id = fields.Many2one('res.company', string='Company', required=True)
    register_date = fields.Date(string='Fecha', required=True)
    leave_cause_id = fields.Many2one(
        'hr.employee.leave.cause',
        string='Motivo de Baja',
        required=False)


class EmployeeLeaveCause(models.Model):
    _name = 'hr.employee.leave.cause'
    _description = 'Employee leave cause'

    name = fields.Char(string='Leave Cause', required=True, size=32)
