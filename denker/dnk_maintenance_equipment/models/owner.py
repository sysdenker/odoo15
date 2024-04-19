# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools, _, SUPERUSER_ID
from odoo.exceptions import UserError, AccessError, ValidationError

class DnkMaintenanceAssetOwner(models.Model):
    _name = "dnk.asset.owner"
    _description = "Asset Owner Type"
    _rec_name = 'name'
    _order = "sequence, name, id"

    name = fields.Char(string='- Name', required=True, translate=True)
    description = fields.Text(string=' - Description', translate=True)
    sequence = fields.Integer(string='- Sequence', default=1, help="Orden de las etapas.")
    fold = fields.Boolean(
        '- Mostrado en Kanban', help='La etapa está plegada cuando no hay registros en la etapa para mostrar.')

    active = fields.Boolean(string='- Activo', default=True)
