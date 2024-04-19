# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools, _, SUPERUSER_ID
from odoo.exceptions import UserError, AccessError, ValidationError

class DnkProductModel(models.Model):
    _name = "dnk.product.model"
    _description = "Denker Product Model"
    _rec_name = 'name'
    _order = "name"

    name = fields.Char(string='- Name', required=True, translate=True)
    dnk_description = fields.Text(string=' - Description', translate=True)
    fold = fields.Boolean(
        '- Mostrado en Kanban', help='La etapa está plegada cuando no hay registros en la etapa para mostrar.')
    active = fields.Boolean(string='- Activo', default=True)


    dnk_partner_id = fields.Many2one('res.partner', string='- Delivery Address', ondelete='cascade', tracking=True, copy=True)
    dnk_sequence_id = fields.Many2one('ir.sequence', string='- Sequence', ondelete='cascade', tracking=True, copy=True)
    dnk_prefix = fields.Char(string='- Sequence Prefix', related="dnk_sequence_id.prefix")
    dnk_code = fields.Char(string='- Sequence Code', related="dnk_sequence_id.code")


    
