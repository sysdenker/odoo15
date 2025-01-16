# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _, SUPERUSER_ID
from odoo.exceptions import UserError
from odoo.osv.expression import OR


class QualityCheck(models.Model):
    _inherit = "quality.check"

    dnk_subfamily_id = fields.Many2one('product.category', string='- Subfamily', related='product_id.categ_id' , store=True)
    dnk_family_id = fields.Many2one('product.category', string='- Family', related='product_id.categ_id.parent_id',  store=True)


    # Campo temporal relacionado a un campo de Studio
    # dnk_workcenter_id  = fields.Many2one('mrp.workcenter', string='- Work Center', related="production_id.x_studio_field_wGB7m")
    