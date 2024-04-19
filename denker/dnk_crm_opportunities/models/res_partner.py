# -*- coding: utf-8 -*-
from odoo import api, fields, models


class Partner(models.Model):
    _inherit = "res.partner"

    dnk_is_final_customer = fields.Boolean('- Is Final Customer?')
    dnk_is_dealer = fields.Boolean('- Is a Dealer?')
    # dnk_lead_ids = fields.One2many('crm.lead', 'dnk_lead_partner_id', string='Opportunities', domain=[('type', '=', 'lead')])
