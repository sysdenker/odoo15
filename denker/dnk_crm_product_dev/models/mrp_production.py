# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools, _

class MrpProduction(models.Model):
    _inherit = "mrp.production"

    dnk_pd_id = fields.Many2one('dnk.crm.product.dev', string='- DP')
