# -*- coding: utf-8 -*-

from odoo import api, fields, models, _

class Task(models.Model):
    _inherit = "project.task"

    @api.depends_context('id', 'name')
    def _compute_display_name(self):
        for task in self:
            task.display_name = '[%s] %s' % (task.id, task.name)

    @api.onchange('x_studio_dp_ids')
    @api.depends('x_studio_dp_ids')
    def _update_lead_id(self):
        for rec in self:
            rec.x_studio_lead_ids = rec.x_studio_dp_ids.x_studio_field_o8n8o
