# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools


class AccountMove(models.Model):
    _inherit = "account.move"

    def _compute_amount(self):
        res = super(AccountMove, self)._compute_amount()
        for rec in self:
            if rec.currency_id.name == 'USD':
                rec.dnk_usd_amount = rec.amount_untaxed
                rec.dnk_usd_residual = rec.amount_residual
                rec.dnk_usd_amount_total = rec.amount_total
                for line in rec.line_ids:
                    line.dnk_usd_subtotal = line.price_subtotal
            elif rec.currency_id.name == 'MXN':
                res_currency_rate = self.env['res.currency.rate']
                # date = self._context.get('date') or fields.Datetime.now()
                date = rec.invoice_date or fields.Datetime.now()
                res_currency_usd_id = self.env['res.currency'].search([('name', '=', 'USD')]).id
                exchange_rate = res_currency_rate.search([('currency_id', '=', res_currency_usd_id), ('name', '<=', date),  ('company_id', '=', rec.company_id.id)], limit=1, order="name desc").rate
                rec.dnk_usd_amount = rec.amount_untaxed * exchange_rate
                rec.dnk_usd_residual = rec.amount_residual * exchange_rate
                rec.dnk_usd_amount_total = rec.amount_total * exchange_rate
                for line in rec.line_ids:
                    line.dnk_usd_subtotal = line.price_subtotal * exchange_rate

        return res

    dnk_usd_amount = fields.Float('- Subtotal USD', help='Untaxed USD Amount', store=True)
    dnk_usd_amount_total = fields.Float('- Total USD', help='Total USD Amount', store=True)
    dnk_usd_residual = fields.Float('- USD Residual', help='USD Residual Amount', store=True)


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    dnk_usd_subtotal = fields.Float('- USD Subtotal', help='Untaxed USD Amount', store=True)
