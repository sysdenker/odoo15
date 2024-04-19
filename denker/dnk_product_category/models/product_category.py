# -*- coding: utf-8 -*-

from odoo import api, fields, models, tools, _


class ProductCategory(models.Model):
    _inherit = 'product.category'

    _rec_name = 'name'

    dnk_abbreviation = fields.Char('- Abbreviation', help='A shortened form of Product Category.')
