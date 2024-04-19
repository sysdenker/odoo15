# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class DenkerProductCost(models.TransientModel):
    _name = "dnk.product.commercial.cost"
    _description = "Denker Commercial Cost"

    dnk_prev_cost = fields.Float('- Denker Previous Standard Cost', digits='Product Price', required=True, help="Costo Denker anterior para Costeo.")
    dnk_new_cost = fields.Float('- Denker New Standard Cost', digits='Product Price', required=True, help="Costo Denker para Costeo.")
    dnk_product_id = fields.Many2one('product.product', '- Product', ondelete='cascade')
    dnk_update_percent = fields.Integer('- Standar Cost Percent', required=True, help="Costo Denker anterior para Costeo.", default=100)

    def change_dnk_commercial_cost(self):
        for rec in self:
            if rec._context['active_model'] == 'product.product':
                products = self.env['product.product'].browse(rec._context['active_ids'])
                for product in products:
                    if rec.dnk_update_percent and product.dnk_standard_cost:
                        rec.dnk_prev_cost = product.dnk_commercial_cost
                        rec.dnk_new_cost = rec.dnk_update_percent / 100 * product.dnk_standard_cost
                        product.dnk_commercial_cost = rec.dnk_new_cost
                    else:
                        product.dnk_commercial_cost = 0
                        rec.dnk_new_cost = 0
        return {'type': 'ir.actions.act_window_close'}
