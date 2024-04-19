# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class AccountInvoiceReport(models.Model):
    _inherit = 'account.invoice.report'

    dnk_subfamily_id = fields.Many2one('product.category', string='- Subfamily', readonly=True)
    dnk_family_id = fields.Many2one('product.category', string='- Family', readonly=True)
    dnk_color_id = fields.Many2one('product.category', string='- Color', readonly=True)

    def _from(self):
        select_add_family = """
            LEFT JOIN
            (SELECT subfamily.id AS dnk_subfamily_id, subfamily.name AS  subfamily,
            family.id AS dnk_family_id, family.name AS family, color.id AS dnk_color_id, color.name AS color
            FROM product_category subfamily
            LEFT JOIN
            (SELECT pc2.id, pc2.name, pc2.parent_id FROM product_category pc2 WHERE pc2.parent_id IN
            (SELECT id FROM product_category WHERE parent_id IS NULL)) family  ON family.id = subfamily.parent_id
            LEFT JOIN
            (SELECT pc3.id,pc3.name FROM product_category pc3 WHERE pc3.parent_id IS NULL) color ON family.parent_id = color.id
            WHERE subfamily.parent_id IS NOT NULL AND subfamily.parent_id NOT IN (SELECT id FROM product_category WHERE parent_id IS NULL))
            AS fam_category ON template.categ_id = fam_category.dnk_subfamily_id
        """
        return super(AccountInvoiceReport, self)._from() + select_add_family

    def _select(self):
        select_family_color = ",fam_category.dnk_color_id,fam_category.dnk_subfamily_id,fam_category.dnk_family_id "
        return super(AccountInvoiceReport, self)._select() + select_family_color

    def _group_by(self):
        select_group = ",fam_category.dnk_color_id,fam_category.dnk_subfamily_id,fam_category.dnk_family_id"
        return super(AccountInvoiceReport, self)._group_by() + select_group
