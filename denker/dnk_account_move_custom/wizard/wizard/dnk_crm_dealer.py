# -*- coding: utf-8 -*-

from odoo import fields, models, _
from odoo.exceptions import UserError


class DnkCRMDealer(models.TransientModel):
    _name = 'dnk.crm.dealer.assigned'
    _description = 'Dnk Daler Assigned'

    dnk_crm_lead_id = fields.Many2one('crm.lead', '- Lead')
    dnk_dealer_id = fields.Many2one('res.partner', '- Dealer')

    def button_assign_dealer(self):
        for rec in self:
            rec.dnk_crm_lead_id.dnk_dealer_id = rec.dnk_dealer_id
