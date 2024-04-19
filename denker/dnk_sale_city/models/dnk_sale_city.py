# -*- coding: utf-8 -*-

from odoo import models, fields, api


class DnkSaleCity(models.Model):
    _name = "dnk.sale.city"
    _rec_name = 'dnk_name'
    _description = "Sale City"
    _order = 'dnk_sequence,dnk_name'
    dnk_name = fields.Char('- Name')
    dnk_code = fields.Char('- Code')
    dnk_sequence = fields.Integer('- Sequence')
