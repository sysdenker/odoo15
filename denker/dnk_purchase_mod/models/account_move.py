# -*- coding: utf-8 -*-

from odoo import api, models, fields, exceptions, _


class AccountMove(models.Model):
    _inherit = 'account.move'

    dnk_vendor_status_id = fields.Many2one('dnk.vendor.status', related="commercial_partner_id.dnk_vendor_status_id")