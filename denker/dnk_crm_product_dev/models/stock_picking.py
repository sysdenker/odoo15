# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools, _

class Picking(models.Model):
    _inherit = "stock.picking"

    dnk_pd_id = fields.Many2one('dnk.crm.product.dev', string='- DP')
