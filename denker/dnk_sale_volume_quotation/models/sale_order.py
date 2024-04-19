# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
import odoo.addons.decimal_precision as dp
# from openerp.exceptions import UserError, RedirectWarning, ValidationError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    # dnk_customer_service_rep_id = fields.Many2one('res.users', string='- Customer Service Rep', tracking=True)
    dnk_order_has_volume_prices = fields.Boolean(string='- Has Volume Prices?', compute='_get_has_volume_prices', default=False)

    @api.depends('order_line')
    def _get_has_volume_prices(self):
        for order in self:
            has_volume_prices_lines = order.order_line.filtered(lambda r: r.dnk_has_volume_prices is True)
            # print(has_volume_prices_lines)
            if has_volume_prices_lines:
                order.dnk_order_has_volume_prices = True
            else:
                order.dnk_order_has_volume_prices = False
