# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class ProductAttributeValue(models.Model):
    _inherit = 'product.attribute.value'

    dnk_reference_code_part = fields.Char(string='- Code Part', help="Se agregará en Dps al código del producto", size=1, copy=True)
    dnk_att_price = fields.Float(string='- Attribute Price',  help="Attribute Price, precio utilizado para sumar al precio en la DP", copy=True)
