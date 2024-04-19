# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def _amount_all(self):
        res = super(SaleOrder, self)._amount_all()
        for rec in self:
            if rec.pricelist_id.currency_id.name == 'USD':
                rec.dnk_usd_amount = rec.amount_untaxed
                for line in rec.order_line:
                    line.dnk_usd_subtotal = line.price_subtotal
            elif rec.pricelist_id.currency_id.name == 'MXN':
                res_currency_rate = self.env['res.currency.rate']
                date = self._context.get('date') or fields.Datetime.now()
                res_currency_usd_id = self.env['res.currency'].search([('name', '=', 'USD')]).id
                exchange_rate = res_currency_rate.search([('currency_id', '=', res_currency_usd_id), ('name', '<=', date)], limit=1, order="name desc").rate
                rec.dnk_usd_amount = rec.amount_untaxed * exchange_rate
                for line in rec.order_line:
                    line.dnk_usd_subtotal = line.price_subtotal * exchange_rate

        return res

    dnk_usd_amount = fields.Float('- USD Amount', help='Untaxed USD Amount', store=True)


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    dnk_usd_subtotal = fields.Float('- USD Subtotal', help='Untaxed USD Amount', store=True)
