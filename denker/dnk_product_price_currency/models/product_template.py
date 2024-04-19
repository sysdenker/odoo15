#!/usr/bin/python
# -*- coding: utf-8 -*-
from odoo import models, fields, api


class ProductTemplate(models.Model):

    _inherit = "product.template"

    dnk_force_currency_id = fields.Many2one(
        'res.currency',
        '- Force Currency',
        help='Use this currency instead of the product company currency',
    )
    dnk_company_currency_id = fields.Many2one(
        string='- Company Currency',
        related='company_id.currency_id',
    )

    @api.depends(
        'dnk_force_currency_id',
        'company_id',
        'company_id.currency_id')
    def _compute_currency_id(self):
        forced_products = self.filtered('dnk_force_currency_id')
        for rec in forced_products:
            rec.currency_id = rec.dnk_force_currency_id
        super(ProductTemplate, self - forced_products)._compute_currency_id()
