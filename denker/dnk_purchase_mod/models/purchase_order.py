# -*- coding: utf-8 -*-

from odoo import api, models, fields, exceptions, _


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    dnk_vendor_status_id = fields.Many2one('dnk.vendor.status', related="partner_id.dnk_vendor_status_id")