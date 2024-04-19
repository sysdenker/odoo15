# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class CRMLead(models.Model):
    _inherit = "crm.lead"

    dnk_pd_quantity = fields.Integer(compute='_compute_pd_quantity', string="- Cantidad Dp's")
    dnk_pd_ids = fields.One2many('dnk.crm.product.dev', 'dnk_lead_id', string='- Órdenes')

    @api.depends('dnk_pd_ids')
    def _compute_pd_quantity(self):
        for lead in self:
            lead.dnk_pd_quantity = len(lead.dnk_pd_ids)
