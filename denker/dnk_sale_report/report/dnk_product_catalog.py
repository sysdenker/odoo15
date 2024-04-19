# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import tools
from odoo import api, fields, models


class DnkProductCatalog(models.Model):
    _name = "dnk.product.catalog"
    _description = "Denker Product Catalog"
    _auto = False
    _rec_name = 'product_id'
    _order = 'product_id desc'

    id = fields.Many2one('product.product', 'Product', readonly=True)
    product_id = fields.Many2one('product.product', 'Product', readonly=True)
    product_tmpl_id = fields.Many2one('product.template', 'Template', readonly=True)
    dnk_subfamily_id = fields.Many2one('product.category', string='- Subfamily', readonly=True)
    dnk_family_id = fields.Many2one('product.category', string='- Family', readonly=True)
    dnk_color_id = fields.Many2one('product.category', string='- Color', readonly=True)
    brand_id = fields.Many2one('product.brand', 'Brand', readonly=True)
    can_be_expensed = fields.Boolean('Can be Expensed', readonly=True)
    company_id = fields.Many2one('res.company', 'Company', readonly=True)
    default_code = fields.Char('Internal Reference', readonly=True)
    create_date = fields.Datetime('Created on', readonly=True)
    create_uid = fields.Many2one('res.users', 'Created by', readonly=True)
    product_tmpl_name = fields.Char('Template Name', readonly=True)
    product_tmpl_description = fields.Char('Template Description', readonly=True)
    uom_id = fields.Many2one('uom.uom', 'Unit of Measure', readonly=True)

    description_picking = fields.Char('Description on Picking', readonly=True)
    description_pickingin = fields.Char('Description on Receptions', readonly=True)
    description_pickingout = fields.Char('Description on Delivery Orders', readonly=True)
    description_purchase = fields.Char('Purchase Descriptions', readonly=True)
    description_sale = fields.Char('Sales Description', readonly=True)
    is_published = fields.Boolean('Is Published', readonly=True)
    produce_delay = fields.Float('Manufacturing Lead Time', readonly=True)
    sale_delay = fields.Float('Customer Lead Time', readonly=True)
    type = fields.Char('Product Type', readonly=True)
    # --mrp_bom.id AS mrp_bom_id,
    active = fields.Boolean('Active', readonly=True)

    def _query(self, with_clause='', fields={}, groupby='', from_clause='', where=''):
        with_ = ("WITH %s" % with_clause) if with_clause else ""

        select_ = """
            p.id,
            p.id AS product_id,
            t.id AS product_tmpl_id,
            pc.dnk_color_id,
            pc.dnk_family_id,
            pc.dnk_subfamily_id,
            t.brand_id,
            t.can_be_expensed,
            t.company_id,
            p.default_code,
            p.create_date,
            p.create_uid,
            t.name AS product_tmpl_name,
            t.description AS product_tmpl_description,
            t.uom_id,
            t.description_picking,
            t.description_pickingin,
            t.description_pickingout,
            t.description_purchase,
            t.description_sale,
            t.is_published,
            t.produce_delay,
            t.sale_delay,
            t.type,
            --mrp_bom.id AS mrp_bom_id,
            p.active
        """

        for field in fields.values():
            select_ += field

        from_ = """
                product_product p
                LEFT JOIN product_template t ON p.product_tmpl_id = t.id
                --LEFT JOIN mrp_bom ON mrp_bom.product_tmpl_id = p.product_tmpl_id AND mrp_bom.active = true
                LEFT JOIN (
                    SELECT subfamily.id AS dnk_subfamily_id,
                        subfamily.name AS subfamily,
                        family.id AS dnk_family_id,
                        family.name AS family,
                        color.id AS dnk_color_id,
                        color.name AS color
                    FROM product_category subfamily
                        LEFT JOIN (
                            SELECT
                                pc2.id,
                                pc2.name,
                                pc2.parent_id
                            FROM product_category pc2
                            WHERE (pc2.parent_id IN (
                                    SELECT product_category.id
                                    FROM product_category
                                    WHERE product_category.parent_id IS NULL))) family ON family.id = subfamily.parent_id
                        LEFT JOIN (
                            SELECT pc3.id, pc3.name
                            FROM product_category pc3
                            WHERE pc3.parent_id IS NULL) color ON family.parent_id = color.id
                WHERE subfamily.parent_id IS NOT NULL AND NOT (subfamily.parent_id IN (
                    SELECT product_category.id
                    FROM product_category
                    WHERE product_category.parent_id IS NULL))) pc ON pc.dnk_subfamily_id = t.categ_id
                %s
        """ % from_clause

        groupby_ = """
            p.id, t.id, pc.dnk_subfamily_id, pc.dnk_color_id, pc.dnk_family_id, t.brand_id,
            t.can_be_expensed, t.company_id, p.default_code, p.create_date, p.create_uid, t.name,
            t.description --, mrp_bom.id
            %s
        """ % (groupby)

        where_ = """
            p.id IS NOT NULL --and p.id = 15093
        """

        return '%s (SELECT %s FROM %s WHERE %s GROUP BY %s)' % (with_, select_, from_, where_, groupby_)

    def init(self):
        self._table = "dnk_product_catalog"
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute("""CREATE or REPLACE VIEW %s as (%s)""" % (self._table, self._query()))


class DnkProductCatalogProforma(models.AbstractModel):
    _name = 'dnk.product.catalog.proforma'
    _description = 'Denker Product Catalog Report'

    def _get_report_values(self, docids, data=None):
        docs = self.env['dnk.product.catalog.proforma'].browse(docids)
        return {
                'doc_ids': docs.ids,
                'doc_model': 'dnk.product.catalog',
                'docs': docs,
                'proforma': True
            }
