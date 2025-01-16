# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools, _


class DnkStockQuantLog(models.Model):
    _name = 'dnk.stock.quant.log'
    _description = 'Inventory Adjustments Log'
    _rec_name = 'name'
    _order = 'name, sequence'

    name = fields.Char('- Name', index=True, required=True)
    sequence = fields.Integer('- Sequence')
    description = fields.Text(
        '- Description', translate=True)
    product_id = fields.Many2one('product.product', '- Product', ondelete='restrict')
    quantity = fields.Float(string="- Quantity")
    user_id = fields.Many2one('res.users', '- User', ondelete='restrict',)
    owner_id = fields.Many2one('res.users', '- Owner', ondelete='restrict',)
    inventory_quantity = fields.Float(string="- Counted Quantity")
    inventory_diff_quantity = fields.Float(string="- Difference")
    dnk_family_id = fields.Many2one('product.category', "- Family")
    dnk_subfamily_id = fields.Many2one('product.category', "- Subfamily")
    location_id =  fields.Many2one('stock.location',  "- Location", ondelete='restrict')
    product_uom_id = fields.Many2one('uom.uom',  "- Location", ondelete='restrict', )
    standard_price =  fields.Float(string="- Cost")