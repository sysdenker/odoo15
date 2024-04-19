# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    dnk_usd_fixed_rate = fields.Monetary(
        related='company_id.dnk_usd_fixed_rate',
        readonly=False,
        string="- USD Fixed Rate", currency_field='currency_id',
        help="USD Fixed Rate to use on pricelists configured to use it.")
