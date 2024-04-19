# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import datetime, date, timedelta


class StockQuant(models.Model):
    _inherit = "stock.quant"

    dnk_default_code = fields.Char('- Aging Code', help="Se utiliza como código de respaldo para seguimiento de máximos y mínimos", related="product_id.dnk_default_code")
