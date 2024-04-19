# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class AccountInvoiceReport(models.Model):
    _inherit = 'account.invoice.report'

    dnk_sale_city_id = fields.Many2one('dnk.sale.city', string='- City', readonly=True)

    def _select(self):
        select_sale_city = ", move.dnk_sale_city_id AS dnk_sale_city_id"

        return super(AccountInvoiceReport, self)._select() + select_sale_city

    def _group_by(self):
        select_group = ", move.dnk_sale_city_id"
        return super(AccountInvoiceReport, self)._group_by() + select_group
