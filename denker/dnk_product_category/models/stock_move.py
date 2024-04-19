# -*- encoding: utf-8 -*-
from odoo import api, fields, models, _


class StockMove(models.Model):
    #  Estos cambios se harán por Odoo Studio.
    _inherit = "stock.move"

    # dnk_subfamily_id = fields.Many2one('product.category', string='- Subfamily', related='product_id.product_tmpl_id.categ_id', tracking=True)
    # dnk_family_id = fields.Many2one('product.category', string='- Family', related='dnk_subfamily_id.parent_id', tracking=True)
    # dnk_color_id = fields.Many2one('product.category', string='- Color', related='dnk_family_id.parent_id', tracking=True)


class StockMoveLine(models.Model):
    #  Estos cambios se harán por Odoo Studio.
    _inherit = "stock.move.line"

    # dnk_subfamily_id = fields.Many2one('product.category', string='- Subfamily', related='product_id.product_tmpl_id.categ_id', tracking=True)
    # dnk_family_id = fields.Many2one('product.category', string='- Family', related='dnk_subfamily_id.parent_id', tracking=True)
    # dnk_color_id = fields.Many2one('product.category', string='- Color', related='dnk_family_id.parent_id', tracking=True)
