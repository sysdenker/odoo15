# -*- coding: utf-8 -*-
from odoo import models, fields, api


class ProductTemplate(models.Model):
    _inherit = "product.template"

    @api.model
    def _default_currency(self):
        for rec in self:
            rec.dnk_cost_currency_id = self.env['res.currency'].search([('name', '=', 'USD')], limit=1).id

    dnk_cost_currency_id = fields.Many2one('res.currency', string='- Denker Cost Currency', compute=_default_currency)

    dnk_imc_ids = fields.Many2many('dnk.indirect.manufacturing.cost', string="- Indirect Manufacturing Costs")
    dnk_lc_ids = fields.One2many('dnk.product.labour.cost.min', inverse_name="dnk_product_tmpl_id", string="- Labour Cost Per Minute")
    dnk_product_op_ids = fields.One2many('dnk.product.op', inverse_name="dnk_product_tmpl_id", string="- Manufacturing Operations")
    dnk_product_op_time = fields.Float(string="- Minutes", help="Minutes", store=True, compute="get_product_op_time")

    @api.depends('dnk_product_op_ids')
    def get_product_op_time(self):
        for rec in self:
            time=0
            for product_op_id in rec.dnk_product_op_ids:
                time= time + product_op_id.dnk_time
            if time:
                rec.dnk_product_op_time = time/60