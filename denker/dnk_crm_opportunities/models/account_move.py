# -*- coding: utf-8 -*-
from odoo import api, fields, models


class AccountMove(models.Model):
    _inherit = "account.move"

    dnk_crm_lead_id = fields.Many2one('crm.lead', string='- Opportunity', related='dnk_order_id.opportunity_id', readonly=True)
