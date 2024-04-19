# -*- coding: utf-8 -*-
from odoo import api, models


class ProductAttribute(models.Model):
    _inherit = "product.attribute"

    @api.depends('product_tmpl_ids')
    def _compute_is_used_on_products(self):
        for pa in self:
            # pa.is_used_on_products = bool(pa.product_tmpl_ids)
            pa.is_used_on_products = False
