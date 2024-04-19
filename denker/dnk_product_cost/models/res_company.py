# -*- coding: utf-8 -*-
from odoo import fields, models


class Company(models.Model):
    _inherit = 'res.company'

    dnk_usd_cost_fixed_rate = fields.Monetary(
        string="- USD Cost Fixed Rate", currency_field='currency_id',
        help="USD Cost Fixed Rate to use on Margin.", default=20.0)
