# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools, _

class MrpEco(models.Model):
    _inherit = "mrp.eco"

    dnk_pd_id = fields.Many2one('dnk.crm.product.dev', string='- DP')


    
