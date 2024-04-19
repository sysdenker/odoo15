# -*- coding: utf-8 -*-
from odoo import models, fields, api, exceptions, _
from datetime import datetime, date, time, timedelta


class CreditLimitAlertSaleOrder(models.Model):
    _name = 'sale.order'
    _inherit = 'sale.order'

    dnk_permitted_limit_exceeded = fields.Boolean(string='- Allow with limit exceeded?', default=False)
    dnk_paid_sale_order = fields.Boolean(string='- Paid Order?', default=False)

    def action_confirm(self):

        for rec in self:
            # Validación de producto archivado.
            for line in self.order_line:
                if not line.product_id.active:
                    raise exceptions.ValidationError("All products must be active to Confirm")
            # Bloqueo directo del Cliente:
            if not rec.website_id and rec.partner_id.parent_id and rec.partner_id.parent_id.dnk_blocked_sales is True:
                raise exceptions.ValidationError("Customer company sales are blocked")
            if not rec.website_id and not rec.partner_id.parent_id and rec.partner_id.dnk_blocked_sales is True:
                raise exceptions.ValidationError('Customer sales are blocked')
            # Se supone que el campo es requerido, pero igual lo pongo.
            if not rec.payment_term_id:
                raise exceptions.ValidationError('Payment terms are required')
            # Término de pago inmediato
            immediate_payment = rec.company_id.dnk_immediate_payment_term
            if not rec.website_id and rec.payment_term_id.id == immediate_payment.id and not rec.dnk_paid_sale_order:
                raise exceptions.ValidationError('If Payment Term is Immediate, you need to validate that this order is paid')

            companies = self.env['res.company'].sudo().search([]).partner_id
            if not rec.website_id and rec.partner_id not in companies or (rec.partner_id.parent_id and rec.partner_id.parent_id not in companies):
                if not(rec.partner_id.parent_id and rec.partner_id.parent_id.dnk_credit_policy) and not rec.partner_id.dnk_credit_policy:
                    current_date = date.today() - timedelta(days=15)
                    params = []
                    partner_ids = ()
                    if rec.partner_id.parent_id:
                        partner_ids = partner_ids + (rec.partner_id.parent_id.id,)
                        for child in rec.partner_id.parent_id.child_ids:
                            partner_ids = partner_ids + (child.id,)
                        params.append(('partner_id', 'in', partner_ids))
                    else:
                        partner_ids = partner_ids + (rec.partner_id.id,)
                        for child in rec.partner_id.child_ids:
                            partner_ids = partner_ids + (child.id,)
                        params.append(('partner_id', 'in', partner_ids))
                    params.append(('move_type', '=', 'out_invoice'))
                    params.append(('state', '=', 'posted'))
                    params.append(('invoice_date_due', '<=', str(current_date)))
                    Invoices = self.env['account.move'].sudo().search(params)
                    # Si el campo de permitir con límite excedido o vencido, pues ya no importa nada.

                    if not rec.dnk_permitted_limit_exceeded:
                        # Si tiene facturas vencidas
                        if Invoices:
                            raise exceptions.ValidationError('Customer has overdue invoices.')
                        # Si no hay facturas vencidas, se valida límite de crédito
                        credit = rec.env['res.currency']._compute(rec.company_id.currency_id, rec.currency_id, rec.partner_id.credit)
                        credit_limit = self.env['res.currency']._compute(rec.company_id.currency_id, rec.currency_id, rec.partner_id.credit_limit)
                        available_credit = self.env['res.currency']._compute(rec.company_id.currency_id, rec.currency_id, rec.partner_id.dnk_available_credit)
                        parent_credit = parent_credit_limit = parent_available_credit = 0
                        if rec.partner_id.parent_id:
                            parent_credit = self.env['res.currency']._compute(rec.company_id.currency_id, rec.currency_id, rec.partner_id.parent_id.credit)
                            parent_credit_limit = self.env['res.currency']._compute(rec.company_id.currency_id, rec.currency_id, rec.partner_id.credit_limit)
                            parent_available_credit = self.env['res.currency']._compute(rec.company_id.currency_id, rec.currency_id, rec.partner_id.parent_id.dnk_available_credit)
                            # Si tengo límite de crédito mayor a 0
                            if parent_credit_limit > 0 and (parent_credit + rec.amount_total) > parent_credit_limit:
                                raise exceptions.ValidationError(
                                    "Exceeded Credit Limit by $%s (%s). \nCompany Credit Limit: $%s (%s),\nCredit: $%s (%s). Available Credit: $%s (%s)"
                                    % (str(round((parent_credit + rec.amount_total - parent_credit_limit), 2)), rec.currency_id.name,
                                        str(round(parent_credit_limit, 2)), rec.currency_id.name,
                                        str(round(parent_credit, 2)), rec.currency_id.name,
                                        str(round(parent_available_credit, 2)), rec.currency_id.name))
                        if credit_limit > 0 and credit + rec.amount_total > credit_limit:
                            raise exceptions.ValidationError(
                                "Exceeded Credit Limit by $%s (%s). \nCredit Limit: $%s (%s),\nCredit: $%s (%s). Available Credit: $%s (%s)"
                                % (str(round((credit + rec.amount_total - credit_limit), 2)), rec.currency_id.name,
                                    str(round(credit_limit, 2)), rec.currency_id.name,
                                    str(round(credit, 2)), rec.currency_id.name,
                                    str(round(available_credit, 2)), rec.currency_id.name))
            res = super(CreditLimitAlertSaleOrder, self).action_confirm()
            return res

    @api.onchange('dnk_permitted_limit_exceeded')
    def udpate_stock_moves(self):
        for sale in self._origin:
            if sale.dnk_permitted_limit_exceeded:
                for stock_picking in sale.picking_ids:
                    stock_picking.write({'dnk_allow_delivery': False})
            else:
                for stock_picking in sale.picking_ids:
                    stock_picking.write({'dnk_allow_delivery': True})
