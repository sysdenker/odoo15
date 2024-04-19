# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class DenkerProductCost(models.TransientModel):
    _name = "dnk.product.standard.cost"
    _description = "Denker Standard Cost"

    dnk_prev_cost = fields.Float('- Denker Previous Standard Cost', digits='Product Price', required=True, help="Costo Denker anterior para Costeo.")
    dnk_new_cost = fields.Float('- Denker New Standard Cost', digits='Product Price', required=True, help="Costo Denker para Costeo.")
    dnk_product_id = fields.Many2one('product.product', '- Product', ondelete='cascade')
    dnk_update_option = fields.Selection([('std_price', 'Standar Price'), ('dnk_cost', 'Costo Estándar Dnk')], string="- Opción de Costo", default='dnk_cost')

    def change_dnk_std_cost(self):
        for rec in self:
            if rec._context['active_model'] == 'product.product':
                products = self.env['product.product'].browse(rec._context['active_ids'])
                for product in products:
                    product.dnk_standard_cost = rec.dnk_new_cost
        return {'type': 'ir.actions.act_window_close'}

    def update_dnk_std_cost(self):
        for rec in self:
            if rec._context['active_model'] == 'product.product':
                products = self.env['product.product'].browse(rec._context['active_ids'])
                for product in products:
                    if rec.dnk_update_option == 'dnk_cost':
                        if product and product.dnk_total_cost > 0 and product.dnk_standard_cost != product.dnk_total_cost:
                            product.dnk_standard_cost = product.dnk_total_cost
                    if rec.dnk_update_option == 'std_price':
                        usd_fixed_rate = product.product_tmpl_id.company_id.dnk_usd_cost_fixed_rate or self.env.user.company_id.dnk_usd_cost_fixed_rate
                        if product and product.standard_price > 0 and product.dnk_standard_cost != product.standard_price:
                            product.dnk_standard_cost = product.standard_price / usd_fixed_rate
        return {'type': 'ir.actions.act_window_close'}
