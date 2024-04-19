# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class SaleOrder(models.Model):
    _inherit = "sale.order"

    dnk_use_product_configurator = fields.Boolean(string='- Use product configurator?', default=False)
