# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class SaleReport(models.Model):
    _inherit = 'sale.report'

    dnk_usd_subtotal = fields.Float('- USD Subtotal', help='Untaxed USD Amount', readonly=True)

    def _query(self, with_clause='', fields={}, groupby='', from_clause=''):
        fields['dnk_usd_subtotal'] = ",sum(l.dnk_usd_subtotal) as dnk_usd_subtotal "
        return super(SaleReport, self)._query(with_clause, fields, groupby, from_clause)
