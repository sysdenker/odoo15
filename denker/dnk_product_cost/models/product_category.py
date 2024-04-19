# -*- coding: utf-8 -*-

from odoo import api, fields, models, tools, _


class ProductCategory(models.Model):
    _inherit = 'product.category'

    dnk_alow_cost_diff = fields.Float('- Porcentaje', digits=(3, 2), help='In Manufacturing Orders, Percentage Allowed')
