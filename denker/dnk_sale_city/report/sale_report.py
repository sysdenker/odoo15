# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class SaleReport(models.Model):
    _inherit = 'sale.report'

    dnk_sale_city_id = fields.Many2one('dnk.sale.city', string='- City', readonly=True)

    def _query(self, with_clause='', fields={}, groupby='', from_clause=''):
        fields['dnk_sale_city_id'] = ",s.dnk_sale_city_id as dnk_sale_city_id"
        groupby += ", s.dnk_sale_city_id"
        return super(SaleReport, self)._query(with_clause, fields, groupby, from_clause)
