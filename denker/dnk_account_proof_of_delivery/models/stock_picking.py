# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools
from PIL import Image
import base64


class StockPicking(models.Model):
    _inherit = "stock.picking"

    dnk_img_proof_of_delivery_datetime = fields.Datetime(
        '- Proof Of Delivery Date', copy=False, readonly=True, store=True)
    dnk_proof_days = fields.Integer(
        '- Proof Days', copy=False, readonly=True, store=True)
