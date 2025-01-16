# -*- coding: utf-8 -*-

from odoo import api, models, fields, exceptions, _


class ResPartner(models.Model):
    _inherit = 'res.partner'

    dnk_vendor_status_id = fields.Many2one('dnk.vendor.status', string='- Vendor Status')