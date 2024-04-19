# -*- coding: utf-8 -*-

from odoo import models, fields, api


class dnk_account_payment_solution(models.Model):
    _inherit = "res.users"

    dnk_sale_city_ids = fields.Many2many(
        comodel_name='dnk.sale.city',
        relation='dnk_sale_city_rel',
        string="- Sale City",)
