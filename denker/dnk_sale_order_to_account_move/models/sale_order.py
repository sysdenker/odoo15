# -*- coding: utf-8 -*-
from odoo import api, fields, models


class SaleOrderToInvoice(models.Model):
    _inherit = "sale.order"

    def _prepare_invoice(self):
        res = super(SaleOrderToInvoice, self)._prepare_invoice()
        res.update({'dnk_order_id': self.id or False, })
        return res


class SaleOrderAdvancePaymentInvoice(models.TransientModel):
    _inherit = "sale.advance.payment.inv"

    def _create_invoice(self, order, so_line, amount):
        res = super(SaleOrderAdvancePaymentInvoice, self)._create_invoice(order, so_line, amount)
        res.update({'dnk_order_id': order.id or False, })
        return res
