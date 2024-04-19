# -*- coding: utf-8 -*-
from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    # Redefino estos campos para que me filtre los resultados.
    seller_ids = fields.One2many(
        'product.supplierinfo', 'product_tmpl_id', 'Vendors',
        help="Define vendor pricelists.",
        domain=[('dnk_only_code', '=', False)])
    variant_seller_ids = fields.One2many(
        'product.supplierinfo', 'product_tmpl_id', domain=[('dnk_only_code', '=', False)])


class ProductProduct(models.Model):
    _inherit = "product.product"

    dnk_customer_ids = fields.One2many(
        'product.supplierinfo', 'product_id', domain=[('dnk_only_code', '=', True)],
        string='- Customer', help="Define Customer Product Code")

    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
        # Voy a buscar primero el customer product code, si encuentro, solo devuelvo eso, si no
        # Entonces regreso la búsqueda original
        # A parte de buscar en el partner, busco en parent y child_ids
        partner_id = self._context.get('partner_id')
        if partner_id and name:
            partner = self.env['res.partner'].search([('id', '=', partner_id)])
            if partner:
                if partner.parent_id:
                    parent_child_ids = partner.parent_id.child_ids.ids
                    parent_child_ids.append(partner.parent_id.id)
                else:
                    parent_child_ids = [partner_id]
                code_ids = self.env['product.supplierinfo']._search([
                    ('dnk_only_code', '=', True), ('name', 'in', parent_child_ids),
                    ('product_code', operator, name), ], limit=limit)
                if code_ids:
                    product_ids = self._search([('dnk_customer_ids', 'in', code_ids)], limit=limit, access_rights_uid=name_get_uid)
                    return product_ids
        return super(ProductProduct, self)._name_search(name=name, args=args, operator=operator, limit=limit, name_get_uid=name_get_uid)


class SupplierInfo(models.Model):
    _inherit = "product.supplierinfo"

    dnk_only_code = fields.Boolean("- Only Customer Code", default=False)
