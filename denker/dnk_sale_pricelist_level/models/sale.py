# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class SaleOrder(models.Model):
    _inherit = "sale.order"
    

    @api.onchange('partner_id')
    def _get_available_price_list(self):
        res = {'domain': {'pricelist_id': []}}
        if not self.env.user.has_group('dnk_sale_pricelist_level.dnk_group_pricelist_manager'):
            if self.partner_id.property_product_pricelist:
                pricelist_search = self.env['product.pricelist'].search(
                    [('dnk_pricelist_level', '>=', self.partner_id.property_product_pricelist.dnk_pricelist_level)])
                res['domain']['pricelist_id'] = [('id', 'in', pricelist_search.ids)]
            else:
                res['domain']['pricelist_id'] = [('id', 'in', (0))]
                warning = {
                    'title': 'Invalid Customer !',
                    'message': 'This customer does not have a defined price list, please assign it one!',
                }
                return {'warning': warning}
        return res
