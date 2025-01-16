# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import timedelta
from odoo import api, fields, models, _
from odoo.exceptions import Warning, ValidationError
import string

# Custom Exception
# from odoo.addons.custom_exception.models.exception import UserError

"""
 * Get color (black/white) depending on bgColor so it would be clearly seen.
 * @param bgColor
 * @returns {string}
 """

class DnkMRPCure(models.Model):
    _name = "dnk.mrp.cure"
    _description = "MRP Manufacturing Status"
    _rec_name = 'name'
    _order = "sequence, name, id"

    name = fields.Char(string='- CURE', required=True, translate=True, help="Clave Única de Registro Estatec")
    dnk_product_id = fields.Many2one('product.product', string='- Product Variant')
    dnk_mrp_production_id = fields.Many2one('mrp.production', string='- Manufacturing Order')
    # fold = fields.Boolean(
    #    '- Mostrado en Kanban', help='La etapa está plegada cuando no hay registros en la etapa para mostrar.')
    # active = fields.Boolean(string='- Active', default=True)