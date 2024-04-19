# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import api, models, fields


class AccountBankStatementLine(models.Model):
    _inherit = 'account.bank.statement.line'

    # @api.onchange('partner_id')
    # def _onchange_partner_id(self):
        # print("MI FUNCUÖN DE BS")
        # payment_way = self.env['l10n_mx_edi.payment.method'].browse(5)
        # for rec in self:
        #    if rec.partner_id:
        #            rec.l10n_mx_edi_payment_method_id = rec.partner_id.commercial_partner_id.dnk_l10n_mx_edi_payment_method_id.id or False
