# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class AccountInvoiceReport(models.Model):
    _inherit = 'account.invoice.report'

    dnk_usd_subtotal = fields.Float('- USD Subtotal', readonly=True, help='Untaxed USD Amount')
    dnk_usd_residual = fields.Float('- USD Residual', readonly=True, help='USD Residual Amount')
    dnk_invoice_origin = fields.Char('- Invoice Origin', readonly=True)

    def _select(self):
        select_usd_subtotal = ",line.dnk_usd_subtotal * (CASE WHEN line.balance < 0 THEN 1 ELSE -1 END) AS dnk_usd_subtotal"
        select_usd_residual = ",move.dnk_usd_residual * (CASE WHEN line.balance < 0 THEN 1 ELSE -1 END) AS dnk_usd_residual"
        select_invoice_origin = ",move.invoice_origin AS dnk_invoice_origin"

        return super(AccountInvoiceReport, self)._select() + select_usd_subtotal + select_usd_residual + select_invoice_origin

    def _group_by(self):
        select_group = ",move.dnk_usd_residual,move.invoice_origin"
        return super(AccountInvoiceReport, self)._group_by() + select_group
