
# -*- coding: utf-8 -*-

from odoo import fields, models


class Company(models.Model):
    _inherit = 'res.company'

    dnk_usd_fixed_rate = fields.Monetary(
        string="- USD Fixed Rate", currency_field='currency_id',
        help="USD Fixed Rate to use on pricelists configured to use it.", default=25.0)
