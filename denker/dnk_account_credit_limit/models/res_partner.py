# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class CreditLimitAlertResPartner(models.Model):
    _name = 'res.partner'
    _inherit = 'res.partner'

    dnk_available_credit = fields.Monetary('- Available Credit', compute='_compute_amount_credit_available')
    dnk_blocked_sales = fields.Boolean('- Sales blocked by default?', default=True)
    dnk_credit_policy = fields.Boolean('- Allow Credit Policy?', default=False, help="If checked, it allows you to confirm sales orders and stock moves")

    @api.model
    def create(self, vals):
        res = super(CreditLimitAlertResPartner, self).create(vals)
        if res.parent_id:
            res.update({'dnk_blocked_sales': False})
        return res

    @api.depends('credit_limit', 'credit')
    def _compute_amount_credit_available(self):
        self.dnk_available_credit = self.credit_limit - self.credit
        pass
