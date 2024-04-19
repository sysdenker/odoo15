# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools, _


class AccountInvoiceLine(models.Model):
    _inherit = "account.move.line"

    dnk_profit_margin_html = fields.Char('- Color', help="Margin Color")
    dnk_profit_margin_ratio = fields.Float('- Margin Ratio')

    def dnk_get_color(self, margin=0):
        if margin:
            if margin >= 0.5:
                return "#0040FF"  # Azul
            elif margin >= 0.4:
                return "#04B404"  # Verde
            elif margin >= 0.3:
                return "#FFFF00"  # Yellow
            elif margin >= 0.2:
                return "#A4A4A4"  # Gris
            elif margin >= 0.0:
                return "#000000"  # Negro
            elif margin < 0:
                return "#9900cc"
        return False

    def dnk_get_margin_profit(self):
        if self.price_unit and self.price_unit > 0:
            dnk_price = self.price_unit
        else:
            dnk_price = self.product_id.price
        dnk_cost = self.product_id.dnk_total_cost
        if not dnk_cost and self.product_id.purchase_ok:
            dnk_cost = self.product_id.standard_price
            # Se supone que el costo estándar es el de la compañía, tons es MXN.
            dnk_cost = dnk_cost / self.move_id.company_id.dnk_usd_cost_fixed_rate
        if dnk_price > 0 and dnk_cost > 0:
            # Primero checar la moneda de sale order
            # El precio del producto es peso, por lo tanto si la SO tiene peso, son iguales
            if self.move_id.currency_id == self.product_id.dnk_cost_currency_id:
                # el costo del costeador siempre está en USD
                return (dnk_price - (dnk_cost * self.move_id.company_id.dnk_usd_cost_fixed_rate)) / dnk_price
            else:
                return ((dnk_price - dnk_cost) / dnk_price)

    @api.onchange('quantity', 'discount', 'price_unit', 'tax_ids')
    def _onchange_price_subtotal(self):
        res = super(AccountInvoiceLine, self)._onchange_price_subtotal()
        return res

    def write(self, vals):
        for rec in self:
            margin = rec.dnk_get_margin_profit()
            if margin:
                vals['dnk_profit_margin_ratio'] = margin
                vals['dnk_profit_margin_html'] = rec.dnk_get_color(margin)
        result = super(AccountInvoiceLine, self).write(vals)
        return result
