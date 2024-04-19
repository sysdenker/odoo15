# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools, _


class LabourCost(models.Model):
    _name = 'dnk.labour.cost'
    _description = 'Labour Cost (Costo de Mano de Obra)'
    _rec_name = 'dnk_name'
    _order = 'dnk_name, id'

    dnk_name = fields.Char('- Name', index=True, required=True, translate=True)
    sequence = fields.Integer('- Sequence')
    dnk_description = fields.Text(
        '- Description', translate=True)
    dnk_unit_price_usd = fields.Float(
        '- Unit Price per minute (USD)',
        digits='Product Price',
        help="This is the unit price of the Labor Cost per minute")


class ProductLabourCostPMin(models.Model):
    _name = 'dnk.product.labour.cost.min'
    _description = 'Product Labour Cost Per Minute(Costo de Mano de Obra por Minuto)'
    _order = 'dnk_name, id'
    _rec_name = 'dnk_product_labour_minutes_qty'

    @api.model
    def _get_dnk_product_tmpl_id(self):
        if 'active_model' in self._context and self._context['active_model'] == 'product.template':
            return self._context['active_id']

    dnk_name = fields.Char(string='- Name', index=True)
    dnk_product_tmpl_id = fields.Many2one('product.template', '- Product Template', default=lambda self: self._get_dnk_product_tmpl_id())
    dnk_product_labour_cost_id = fields.Many2one(
        'dnk.labour.cost', string='- Labour Cost',
        store=True)
    dnk_unit_price_usd = fields.Float(string='- Unit Price (USD) per minute', related="dnk_product_labour_cost_id.dnk_unit_price_usd")
    dnk_product_labour_minutes_qty = fields.Float(
        string="- Labour Minutes", default=1.00)
