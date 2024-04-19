from odoo import api, fields, models, _


class ProductTemplate(models.Model):
    _inherit = "product.template"

    dnk_pdev_qty = fields.Integer(compute='_compute_pdev_qty', string="- Dp's Qty")

    def _compute_pdev_qty(self):
        for lead in self:
            lead.dnk_pdev_qty = 0
