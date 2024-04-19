# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class SaleReport(models.Model):
    _inherit = 'sale.report'

    dnk_subfamily_id = fields.Many2one('product.category', string='- Subfamily', readonly=True)
    dnk_family_id = fields.Many2one('product.category', string='- Family', readonly=True)
    dnk_color_id = fields.Many2one('product.category', string='- Color', readonly=True)

    def _query(self, with_clause='', fields={}, groupby='', from_clause=''):
        fields['select_family_color'] = ",pc.dnk_subfamily_id as dnk_subfamily_id, pc.dnk_color_id as dnk_color_id, pc.dnk_family_id as dnk_family_id"
        groupby += ",pc.dnk_subfamily_id, pc.dnk_color_id, pc.dnk_family_id"
        from_clause += """
            LEFT JOIN
                (SELECT subfamily.id AS dnk_subfamily_id, subfamily.name AS  subfamily, family.id AS dnk_family_id,
                family.name AS family, color.id AS dnk_color_id, color.name AS color FROM product_category subfamily
                LEFT JOIN
                (SELECT pc2.id, pc2.name, pc2.parent_id FROM product_category pc2 WHERE pc2.parent_id IN
                (SELECT id FROM product_category WHERE parent_id IS NULL)) family  ON family.id = subfamily.parent_id
                LEFT JOIN
                (SELECT pc3.id,pc3.name FROM product_category pc3 WHERE pc3.parent_id IS NULL) color ON family.parent_id = color.id
                WHERE subfamily.parent_id IS NOT NULL AND subfamily.parent_id NOT IN (SELECT id FROM product_category WHERE parent_id IS NULL))
                AS pc ON pc.dnk_subfamily_id = t.categ_id
        """
        return super(SaleReport, self)._query(with_clause, fields, groupby, from_clause)
