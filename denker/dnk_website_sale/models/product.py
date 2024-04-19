# -*- encoding: utf-8 -*-
from odoo import api, fields, http, models, _


class ProductTemplate(models.Model):
    _inherit = ["product.template"]

    dnk_website_ids = fields.Many2many('website', 'product_tmpl_website_rel', 'product_tmpl_id', 'website_id', string='- Websites')
