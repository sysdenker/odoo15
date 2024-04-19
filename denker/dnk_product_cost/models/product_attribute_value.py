# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class ProductAttributeValue(models.Model):
    _inherit = 'product.attribute.value'

    dnk_product_labour_cost_id = fields.Many2one(
        'dnk.labour.cost', string='- Labour Cost',
        store=True)
    dnk_product_labour_minutes_qty = fields.Float(
        string="- Minutes", default=1.00)
    dnk_unit_price_usd = fields.Float(
        '- Unit Price per minute (USD)',
        digits='Product Price',
        help="This is the unit price of the Labor Cost per minute")

    @api.onchange('dnk_product_labour_cost_id')
    def onchange_product_labour_cost(self):
        for lc in self:
            lc.dnk_unit_price_usd = lc.dnk_product_labour_cost_id.dnk_unit_price_usd
