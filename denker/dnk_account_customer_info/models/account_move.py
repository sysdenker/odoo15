# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools


class AccountMove(models.Model):
    _inherit = "account.move"

    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        res = super(AccountMove, self)._onchange_partner_id()
        payment_way = self.env['l10n_mx_edi.payment.method'].browse(5)
        if self.partner_id:
            self.fiscal_position_id = self.partner_id.commercial_partner_id.property_account_position_id.id or False
            self.l10n_mx_edi_usage = self.partner_id.commercial_partner_id.dnk_l10n_mx_edi_usage or False
            if self.dnk_order_id and self.dnk_order_id.website_id:
                self.l10n_mx_edi_payment_method_id = payment_way
            else:
                self.l10n_mx_edi_payment_method_id = self.partner_id.commercial_partner_id.dnk_l10n_mx_edi_payment_method_id.id or False
        return res
