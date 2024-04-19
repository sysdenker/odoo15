# -*- encoding: utf-8 -*-
from odoo import api, fields, models, _


class ProductProduct(models.Model):
    _inherit = "product.product"

    sale_delay = fields.Float(
        'Customer Lead Time', default=0,
        help="Delivery lead time, in days. It's the number of days, promised to the customer, between the confirmation of the sales order and the delivery.")


class Product(models.Model):
    _inherit = "product.template"

    def _create_variant_ids(self):
        res = super(Product, self)._create_variant_ids()
        for rec in self:
            for var in rec.product_variant_ids:
                var.sale_delay = rec.sale_delay
        return res
