# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools, _
from odoo.osv import expression
import re


class ProductMaterialComposition(models.Model):
    _name = 'dnk.product.material.composition'
    _description = 'Material Composition'
    _rec_name = 'dnk_name'

    dnk_name = fields.Char(string='- Composition', required=True, size=32)
    dnk_name_es_mx = fields.Char(string='- Composition ES_Mx', required=True, size=32)
    dnk_percent = fields.Char(string='- Percent', required=True, size=3)
    dnk_sequence = fields.Integer('- Sequence')
    dnk_product_material_id = fields.Many2one('dnk.product.material', '- Product Material', ondelete='cascade')


class ProductMaterial(models.Model):
    _name = 'dnk.product.material'
    _description = 'product Material Composition'
    _rec_name = 'dnk_name'

    dnk_name = fields.Char('- Material', required=True, size=16)
    dnk_composition_ids = fields.One2many(comodel_name='dnk.product.material.composition', inverse_name='dnk_product_material_id', string='- Compositions')


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    dnk_material_id = fields.Many2one('dnk.product.material', string='- Product Material')
