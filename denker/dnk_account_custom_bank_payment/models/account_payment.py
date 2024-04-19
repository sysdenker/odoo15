
# -*- coding: utf-8 -*-
from odoo import api, models, fields


class account_payment(models.Model):
    _inherit = "account.payment"

    # Agregar el código del Diario para generar el nombre del PDF con el formato del la localización mexicana (l10n_mx_edi)
    # report_name = ''${object.dnk_journal_code}-${(object.name or '').replace('/','-')}-MX-Payment-10'
    dnk_journal_code = fields.Char(string='- Journal Code', size=5, related='journal_id.code', help="The journal entries of this journal will be named using this prefix.")

    # Soluciona el problema de que cuando realizar un conciliación bancaria se registra un pago con nombre pero con nombre
    # en 'hard coded' como 'Bank Statement Date' en vez de usar la secuencia adecuada:
    # account/models/account_bank_statement.py
    # Línea 953: 'name': self.statement_id.name or _("Bank Statement %s") %  self.date,
    @api.model
    def create(self, vals):
        if 'name' in vals and vals['name'] is not False and (vals['name'][:15] == 'Bank Statement ' or vals['name'][:18] == 'Extracto bancario '):
            payment_type = vals['payment_type']
            partner_type = vals['partner_type']

            # Use the right sequence to set the name
            sequence_code = False
            if payment_type == 'transfer':
                sequence_code = 'account.payment.transfer'
            else:
                if partner_type == 'customer':
                    if payment_type == 'inbound':
                        sequence_code = 'account.payment.customer.invoice'
                    if payment_type == 'outbound':
                        sequence_code = 'account.payment.customer.refund'
                if partner_type == 'supplier':
                    if payment_type == 'inbound':
                        sequence_code = 'account.payment.supplier.refund'
                    if payment_type == 'outbound':
                        sequence_code = 'account.payment.supplier.invoice'

            if sequence_code:
                vals.update({'name': self.env['ir.sequence'].next_by_code(sequence_code)})

        res = super(account_payment, self).create(vals)
        return res
