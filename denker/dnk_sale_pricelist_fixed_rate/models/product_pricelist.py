# -*- coding: utf-8 -*-

from odoo import models, fields, api, tools, _
from odoo.exceptions import UserError, RedirectWarning
import odoo.addons.decimal_precision as dp
from odoo.api import Environment


class Pricelist(models.Model):
    _inherit = "product.pricelist"

    dnk_use_usd_fixed_rate = fields.Boolean(
        string='- Use USD Fixed Rate',
        help='If checked, the price list use de USD Fixed Rate to convert prices',
        default=False)

    def _compute_price_rule(self, products_qty_partner, date=False, uom_id=False):
        results = super(Pricelist, self)._compute_price_rule(products_qty_partner, date=False, uom_id=False)
        usd_currency_id = self.env.ref("base.USD")

        if self.dnk_use_usd_fixed_rate and usd_currency_id != self.currency_id:
            usd_fixed_rate = self.company_id.dnk_usd_fixed_rate
            # Calcular el precio basado en la Tasa Fija de USD configurada en la compañía
            unit_price, rule_id = results[next(iter(results))]
            results[next(iter(results))] = (round((unit_price * usd_fixed_rate) * usd_currency_id.rate, 4), rule_id)
        return results
