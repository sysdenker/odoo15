# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class DnkCRMSaleOrder(models.Model):
    _inherit = "sale.order"

    def get_dnk_final_customer_id(self):
        for rec in self:
            rec.dnk_final_customer_id = rec.opportunity_id.dnk_final_customer_id or False

    dnk_final_customer_id = fields.Many2one("res.partner", compute="get_dnk_final_customer_id", string='- Final Customer')
