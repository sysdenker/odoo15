# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools, _


class DnkVendorStatus(models.Model):
    _name = 'dnk.vendor.status'
    _description = 'Vendor Status'
    _rec_name = 'name'
    _order = 'sequence, name'

    name = fields.Char('- Name', index=True, required=True, translate=True)
    sequence = fields.Integer('- Sequence')
    description = fields.Text(
        '- Description', translate=True)