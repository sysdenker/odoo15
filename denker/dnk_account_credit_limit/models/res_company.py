# -*- coding: utf-8 -*-
from odoo import models, fields, api, exceptions, _


class SaleConfigSettings(models.Model):
    _inherit = "res.company"

    dnk_immediate_payment_term = fields.Many2one('account.payment.term', string="- Immediate payment term")


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    dnk_immediate_payment_term = fields.Many2one(
        'account.payment.term',
        string="- Immediate payment term",
        related='company_id.dnk_immediate_payment_term',
        readonly=False,
        config_parameter='sale.dnk_immediate_payment_term',
        help='Término de pago que se compara con cada venta y determina si es inmediato.')
