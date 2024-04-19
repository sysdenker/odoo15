# -*- coding: utf-8 -*-
from odoo import models, fields, api, tools, _
from odoo.api import Environment


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    """
    @api.onchange('product_uom', 'product_uom_qty')
    def product_uom_change(self):
        result = super(SaleOrderLine, self).product_uom_change()
        if self.order_id.pricelist_id and self.order_id.partner_id:
            if self.order_id.pricelist_id.dnk_use_usd_fixed_rate:
                usd_current_exchange_rate = self.env.ref("base.USD").rate
                usd_fixed_rate = self.order_id.company_id.dnk_usd_fixed_rate

                # Calcular el precio basado en la Tasa Fija de USD configurada en la compañía
                self.price_unit = round(self.price_unit * usd_current_exchange_rate * usd_fixed_rate, 4)
        return result
    """
