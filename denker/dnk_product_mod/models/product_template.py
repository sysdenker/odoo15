# -*- coding: utf-8 -*-
from odoo import models, fields, api


class ProductTemplate(models.Model):
    _inherit = "product.template"


    dnk_printed_substrate_id = fields.Many2one('dnk.bag.printed.substrate', '- Printed Substrate', ondelete='cascade')
    dnk_bag_lamination_id = fields.Many2one('dnk.bag.lamination', '- Lamination', ondelete='cascade')
    dnk_bag_thickness_id = fields.Many2one('dnk.bag.thickness', '- Bag Thickness', ondelete='cascade')

    dnk_family_id = fields.Many2one(comodel_name='product.category', string='- Family', related="categ_id.parent_id", store=True)