# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.osv import expression


class XDP(models.Model):
    _name = "x_dp"
    _inherit = ['mail.thread', 'mail.activity.mixin', 'utm.mixin']
    # _inherit = "x_dp"
    # _rec_name = 'id,x_name'

    dnk_task_count = fields.Integer(string='Project Task Count', compute='_compute_project_task_count')


    def _compute_project_task_count(self):
        for rec in self:
            rec.dnk_task_count = self.env['project.task'].search_count([('x_studio_dp_ids', '=', rec.id)])


    def dnk_project_task_action(self):
        Task = self.env['project.task'].search([('x_studio_dp_ids', '=', self.id)])
        res = [line.id for line in Task]
        return {
            'domain': "[('id','in',[" + ','.join(map(str, list(res))) + "])]",
            'name': _('Project Task'),
            'view_mode': 'tree,form',
            'view_type': 'form',
            'res_model': 'project.task',
            'type': 'ir.actions.act_window', }


    @api.depends_context('id', 'x_name')
    def _compute_display_name(self):
        for pdev in self:
            pdev.display_name = '[%s] %s' % (pdev.id, pdev.x_name)


    def name_get(self):
        result = []
        for rec in self:
            result.append((rec.id, '[%s] - %s' % (rec.id,rec.x_name)))
        return result

    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
        if operator in ('ilike', 'like', '=', '=like', '=ilike'):
            args = expression.AND([
                args or [],
                ['|', ('id', operator, name), ('x_name', operator, name)]
            ])
            return self._search(args, limit=limit, access_rights_uid=name_get_uid)
        return super(XDP, self)._name_search(name, args=args, operator=operator, limit=limit, name_get_uid=name_get_uid)
