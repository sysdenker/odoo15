# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools


class account_payment(models.Model):
    _inherit = "account.payment"

    def _compute_payment_difference(self):
        res = super(account_payment, self)._compute_payment_difference()
        for rec in self:
            if rec.currency_id.name == 'USD':
                rec.dnk_usd_amount = rec.amount
            elif rec.currency_id.name == 'MXN':
                res_currency_rate = self.env['res.currency.rate']
                date = self._context.get('date') or fields.Datetime.now()
                res_currency_usd_id = self.env['res.currency'].search([('name', '=', 'USD')]).id
                exchange_rate = res_currency_rate.search([('currency_id', '=', res_currency_usd_id), ('name', '<=', date)], limit=1, order="name desc").rate
                rec.dnk_usd_amount = rec.amount * exchange_rate
        return res

    dnk_usd_amount = fields.Float('- USD Amount', store=True)
