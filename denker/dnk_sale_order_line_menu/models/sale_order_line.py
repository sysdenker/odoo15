# -*- coding: utf-8 -*-
from odoo import api, fields, models
from datetime import timedelta


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    team_id = fields.Many2one(
        'crm.team', 'Sales Team',
        change_default=True, related="order_id.team_id", check_company=True,  # Unrequired company
        domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]")

    order_warehouse_id = fields.Many2one(
        'stock.warehouse',
        string='Warehouse',
        related='order_id.warehouse_id',
        store=True,
        required=False,
        readonly=True,
        states={'draft': [('readonly', False)], 'sent': [('readonly', False)]})

    dnk_subfamily_id = fields.Many2one(
        'product.category', '- Subfamily',
        required=False,
        store=True,
        readonly=False,
        related='product_id.categ_id')
    dnk_family_id = fields.Many2one(
        'product.category', '- Family',
        required=False,
        store=True,
        readonly=False,
        related='product_id.categ_id.parent_id')
    dnk_color_id = fields.Many2one(
        'product.category', '- Color',
        required=False,
        store=True,
        readonly=False,
        related='product_id.categ_id.parent_id.parent_id')
