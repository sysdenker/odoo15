# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.tools.float_utils import float_compare, float_is_zero
from odoo.exceptions import UserError, ValidationError


class StockQuant(models.Model):
    _inherit = "stock.quant"

    def dnk_stock_quant_log(self):
        for rec in self:
            new_sq_log = {}
            new_sq_log['name'] = rec.product_id.name
            new_sq_log['product_id'] = rec.product_id.id
            new_sq_log['dnk_family_id'] = rec.product_id.categ_id.parent_id.id
            new_sq_log['dnk_subfamily_id'] = rec.product_id.categ_id.id
            new_sq_log['product_uom_id'] = rec.product_id.uom_id.id
            new_sq_log['owner_id'] = rec.owner_id.id
            new_sq_log['user_id'] = rec.user_id.id
            new_sq_log['location_id'] = rec.location_id.id
            new_sq_log['quantity'] = rec.quantity
            new_sq_log['standard_price'] = rec.product_id.standard_price
            new_sq_log['inventory_quantity'] = rec.inventory_quantity
            new_sq_log['inventory_diff_quantity'] = rec.inventory_diff_quantity
            sq_log = self.env['dnk.stock.quant.log'].create(new_sq_log)

    def _apply_inventory(self):
        print (self)
        self.dnk_stock_quant_log()
        res = super(StockQuant, self)._apply_inventory()
        return res