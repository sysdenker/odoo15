# -*- coding: utf-8 -*-

from odoo import fields, models


class IrView(models.Model):
    _inherit = 'ir.ui.view'

    dnk_label_flag = fields.Boolean(
        string='- Is a label to print?',
        help='If True, the view is a label to print.',
        default=False)
    dnk_label_group_id = fields.Many2one(
        comodel_name='dnk.printing.label.group', string='- Label Group',
        help='Label group used to print this label.')
