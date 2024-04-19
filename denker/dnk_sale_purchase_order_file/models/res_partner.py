# -*- coding: utf-8 -*-
from odoo import api, fields, models


class PurchaseOrderFile(models.Model):
    _inherit = ['res.partner']

    dnk_purchase_order_required = fields.Boolean('- Is Purchase Order File required?', help='Check this box if Purchase Order File is required', default=True)
    dnk_attach_purchase_order = fields.Boolean('- Attach Purchase Order File?', help='Check this box to attach the Purchase Order on invoice Mail', default=True)
