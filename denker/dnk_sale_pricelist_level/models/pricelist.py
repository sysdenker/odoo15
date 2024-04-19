# -*- coding: utf-8 -*-
from odoo import models, fields, api, tools, _


class Pricelist(models.Model):
    _inherit = "product.pricelist"

    dnk_pricelist_level = fields.Integer(
        string='Pricelist Level',
        help='Lower level is cheaper and higher is more expensive',
        default=1)
