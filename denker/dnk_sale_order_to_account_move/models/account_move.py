# -*- coding: utf-8 -*-
from odoo import api, fields, models


class InvoiceToSaleOrder(models.Model):
    _inherit = "account.move"

    dnk_order_id = fields.Many2one('sale.order', string='- Sale Order', store=True, copy=True)
