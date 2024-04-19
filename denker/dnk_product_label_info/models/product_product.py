# -*- coding: utf-8 -*-
from odoo import fields, models


class ProductProduct(models.Model):
    _inherit = 'product.product'

    # Campo para limitar por producto, cuales etiquetas visualizar
    dnk_ir_ui_view_ids = fields.Many2many(
        comodel_name='ir.ui.view',
        relation='dnk_product_ui_view_rel',
        column1='product_id',
        column2='ir_ui_view_id',
        domain="[('dnk_label_flag', '=', True),('dnk_label_group_id', '!=', False),('model', '=', 'mrp.production')]",
        string='- MO Labels')
