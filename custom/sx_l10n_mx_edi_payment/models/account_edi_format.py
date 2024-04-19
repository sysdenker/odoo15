from odoo import api, models, fields, tools, _
from odoo.tools.xml_utils import _check_with_xsd
from odoo.tools.float_utils import float_round, float_is_zero

import logging
import re
import base64
import json
import requests
import random
import string

from lxml import etree
from lxml.objectify import fromstring
from math import copysign
from datetime import datetime
from io import BytesIO
from zeep import Client
from zeep.transports import Transport
from json.decoder import JSONDecodeError

_logger = logging.getLogger(__name__)
EQUIVALENCIADR_PRECISION_DIGITS = 10


from pudb.remote import set_trace

DEBUG = False


class AccountEdiFormat(models.Model):
    _inherit = 'account.edi.format'

    @api.model
    def _l10n_mx_edi_check_configuration(self, move):
        res = super(AccountEdiFormat, self)._l10n_mx_edi_check_configuration(move)

        company = move.company_id
        pac_name = company.l10n_mx_edi_pac

        errors = []

        # == Check the certificate ==
        certificate = company.l10n_mx_edi_certificate_ids.sudo().get_valid_certificate()
        if not certificate:
            errors.append(_('No valid certificate found'))

        # == Check the credentials to call the PAC web-service ==
        if pac_name:
            pac_test_env = company.l10n_mx_edi_pac_test_env
            pac_password = company.sudo().l10n_mx_edi_pac_password
            if not pac_test_env and not pac_password:
                errors.append(_('No PAC credentials specified.'))
        else:
            errors.append(_('No PAC specified.'))

        # == Check the 'l10n_mx_edi_decimal_places' field set on the currency  ==
        #  currency_precision = move.currency_id.l10n_mx_edi_decimal_places
        currency_precision = 2
        if currency_precision is False:
            errors.append(_(
                "The SAT does not provide information for the currency %s.\n"
                "You must get manually a key from the PAC to confirm the "
                "currency rate is accurate enough.") % move.currency_id)

        # == Check the invoice ==
        if move.l10n_mx_edi_cfdi_request in ('on_invoice', 'on_refund'):
            negative_lines = move.invoice_line_ids.filtered(lambda line: line.price_subtotal < 0)
            if negative_lines:
                # Line having a negative amount is not allowed.
                if not move._l10n_mx_edi_is_managing_invoice_negative_lines_allowed():
                    errors.append(_("Invoice lines having a negative amount are not allowed to generate the CFDI. "
                                    "Please create a credit note instead."))
                # Discount line without taxes is not allowed.
                if negative_lines.filtered(lambda line: not line.tax_ids):
                    errors.append(_("Invoice lines having a negative amount without a tax set is not allowed to "
                                    "generate the CFDI."))
            invalid_unspcs_products = move.invoice_line_ids.product_id.filtered(lambda product: not product.unspsc_code_id)
            if invalid_unspcs_products:
                errors.append(_("You need to define an 'UNSPSC Product Category' on the following products: %s")
                              % ', '.join(invalid_unspcs_products.mapped('display_name')))
        return errors

    def _l10n_mx_edi_get_common_cfdi_values(self, move):
        ''' Generic values to generate a cfdi for a journal entry.
        :param move:    The account.move record to which generate the CFDI.
        :return:        A python dictionary.
        '''
        if self.env.user.id == 2 and DEBUG:
            set_trace(term_size=(170, 47), host='0.0.0.0', port=6900)

        #  res = super(AccountEdiFormat, self)._l10n_mx_edi_get_common_cfdi_values(move)

        def _format_string_cfdi(text, size=100):
            """Replace from text received the characters that are not found in the
            regex. This regex is taken from SAT documentation
            https://goo.gl/C9sKH6
            text: Text to remove extra characters
            size: Cut the string in size len
            Ex. 'Product ABC (small size)' - 'Product ABC small size'"""
            if not text:
                return None
            text = text.replace('|', ' ')
            return text.strip()[:size]

        def _format_float_cfdi(amount, precision):
            if amount is None or amount is False:
                return None
            # Avoid things like -0.0, see: https://stackoverflow.com/a/11010869
            return '%.*f' % (precision, amount if not float_is_zero(amount, precision_digits=precision) else 0.0)

        company = move.company_id
        certificate = company.l10n_mx_edi_certificate_ids.sudo().get_valid_certificate()
        #  currency_precision = move.currency_id.l10n_mx_edi_decimal_places
        currency_precision = 2

        customer = move.partner_id if move.partner_id.type == 'invoice' else move.partner_id.commercial_partner_id
        supplier = move.company_id.partner_id.commercial_partner_id

        if not customer:
            customer_rfc = False
        elif customer.country_id and customer.country_id.code != 'MX':
            customer_rfc = 'XEXX010101000'
        elif customer.vat:
            customer_rfc = customer.vat.strip()
        elif customer.country_id.code in (False, 'MX'):
            customer_rfc = 'XAXX010101000'
        else:
            customer_rfc = 'XEXX010101000'

        if move.l10n_mx_edi_origin:
            origin_type, origin_uuids = move._l10n_mx_edi_read_cfdi_origin(move.l10n_mx_edi_origin)
        else:
            origin_type = None
            origin_uuids = []

        return {
            **self._l10n_mx_edi_get_serie_and_folio(move),
            'certificate': certificate,
            'certificate_number': certificate.serial_number,
            'certificate_key': certificate.sudo().get_data()[0].decode('utf-8'),
            'record': move,
            'supplier': supplier,
            'customer': customer,
            'customer_rfc': customer_rfc,
            'issued_address': move._get_l10n_mx_edi_issued_address(),
            'currency_precision': currency_precision,
            'origin_type': origin_type,
            'origin_uuids': origin_uuids,
            'format_string': _format_string_cfdi,
            'format_float': _format_float_cfdi,
        }

    def _l10n_mx_edi_get_payment_cfdi_values(self, move):
        if self.env.user.id == 2 and DEBUG:
            set_trace(term_size=(170, 47), host='0.0.0.0', port=6900)

        #res = super(AccountEdiFormat, self)._l10n_mx_edi_get_payment_cfdi_values(move)

        def get_tax_cfdi_name(tax_detail_vals):
            tags = set()
            for detail in tax_detail_vals['group_tax_details']:
                for tag in detail['tax_repartition_line_id'].tag_ids:
                    tags.add(tag)
            tags = list(tags)
            if len(tags) == 1:
                return {'ISR': '001', 'IVA': '002', 'IEPS': '003'}.get(tags[0].name)
            elif tax_detail_vals['tax'].l10n_mx_tax_type == 'Exento':
                return '002'
            else:
                return None

        def divide_tax_details(invoice, tax_details, amount_paid):
            percentage_paid = amount_paid / invoice.amount_total
            #  precision = invoice.currency_id.decimal_places
            precision = 6
            sign = -1 if invoice.is_inbound() else 1
            for detail in tax_details['tax_details'].values():
                tax = detail['tax']
                tax_amount = abs(tax.amount) / 100.0 if tax.amount_type != 'fixed' else abs(detail['tax_amount_currency'] / detail['base_amount_currency'])
                base_val_proportion = float_round(detail['base_amount_currency'] * percentage_paid * sign, precision)
                tax_val_proportion = float_round(base_val_proportion * tax_amount, precision)
                detail.update({
                    'base_val_prop_amt_curr': base_val_proportion,
                    'tax_val_prop_amt_curr': tax_val_proportion if tax.l10n_mx_tax_type != 'Exento' else False,
                    'tax_class': get_tax_cfdi_name(detail),
                    'tax_amount': tax_amount,
                })
            return tax_details

        if move.payment_id:
            currency = move.payment_id.currency_id
            total_amount = move.payment_id.amount
        else:
            if move.statement_line_id.foreign_currency_id:
                total_amount = move.statement_line_id.amount_currency
                currency = move.statement_line_id.foreign_currency_id
            else:
                total_amount = move.statement_line_id.amount
                currency = move.statement_line_id.currency_id

        # Process reconciled invoices.
        invoice_vals_list = []
        pay_rec_lines = move.line_ids.filtered(lambda line: line.account_internal_type in ('receivable', 'payable'))
        paid_amount = abs(sum(pay_rec_lines.mapped('amount_currency')))

        mxn_currency = self.env["res.currency"].search([('name', '=', 'MXN')], limit=1)
        if move.currency_id == mxn_currency:
            rate_payment_curr_mxn = None
            paid_amount_comp_curr = paid_amount
        else:
            rate_payment_curr_mxn = move.currency_id._convert(1.0, mxn_currency, move.company_id, move.date, round=False)
            paid_amount_comp_curr = move.company_currency_id.round(paid_amount * rate_payment_curr_mxn)

        for field1, field2 in (('debit', 'credit'), ('credit', 'debit')):
            for partial in pay_rec_lines[f'matched_{field1}_ids']:
                payment_line = partial[f'{field2}_move_id']
                invoice_line = partial[f'{field1}_move_id']
                invoice_amount = partial[f'{field1}_amount_currency']
                exchange_move = invoice_line.full_reconcile_id.exchange_move_id
                invoice = invoice_line.move_id

                if not invoice.l10n_mx_edi_cfdi_request:
                    continue

                if exchange_move:
                    exchange_partial = invoice_line[f'matched_{field2}_ids']\
                        .filtered(lambda x: x[f'{field2}_move_id'].move_id == exchange_move)
                    if exchange_partial:
                        invoice_amount += exchange_partial[f'{field2}_amount_currency']

                if invoice_line.currency_id == payment_line.currency_id:
                    # Same currency
                    amount_paid_invoice_curr = invoice_amount
                    exchange_rate = None
                else:
                    # It needs to be how much invoice currency you pay for one payment currency
                    amount_paid_invoice_comp_curr = payment_line.company_currency_id.round(
                        total_amount * (partial.amount / paid_amount_comp_curr))
                    invoice_rate = abs(invoice_line.amount_currency) / abs(invoice_line.balance)
                    amount_paid_invoice_curr = invoice_line.currency_id.round(partial.amount * invoice_rate)
                    exchange_rate = amount_paid_invoice_curr / amount_paid_invoice_comp_curr
                    exchange_rate = float_round(exchange_rate, precision_digits=EQUIVALENCIADR_PRECISION_DIGITS, rounding_method='UP')

                # for CFDI 4.0
                cfdi_values = self._l10n_mx_edi_get_invoice_cfdi_values(invoice)
                tax_details_transferred = divide_tax_details(invoice, cfdi_values['tax_details_transferred'], amount_paid_invoice_curr)
                tax_details_withholding = divide_tax_details(invoice, cfdi_values['tax_details_withholding'], amount_paid_invoice_curr)

                invoice_vals_list.append({
                    'invoice': invoice,
                    'exchange_rate': exchange_rate,
                    'EQUIVALENCIADR_PRECISION_DIGITS': EQUIVALENCIADR_PRECISION_DIGITS,
                    'payment_policy': invoice.l10n_mx_edi_payment_policy,
                    'number_of_payments': len(invoice._get_reconciled_payments()) + len(invoice._get_reconciled_statement_lines()),
                    'amount_paid': amount_paid_invoice_curr,
                    'amount_before_paid': min(invoice.amount_residual + amount_paid_invoice_curr, invoice.amount_total),
                    'tax_details_transferred': tax_details_transferred,
                    'tax_details_withholding': tax_details_withholding,
                    **self._l10n_mx_edi_get_serie_and_folio(invoice),
                })

        payment_method_code = move.l10n_mx_edi_payment_method_id.code
        is_payment_code_emitter_ok = payment_method_code in ('02', '03', '04', '05', '06', '28', '29', '99')
        is_payment_code_receiver_ok = payment_method_code in ('02', '03', '04', '05', '28', '29', '99')
        is_payment_code_bank_ok = payment_method_code in ('02', '03', '04', '28', '29', '99')

        bank_accounts = move.partner_id.commercial_partner_id.bank_ids.filtered(lambda x: x.company_id.id in (False, move.company_id.id))

        partner_bank = bank_accounts[:1].bank_id
        if partner_bank.country and partner_bank.country.code != 'MX':
            partner_bank_vat = 'XEXX010101000'
        else:  # if no partner_bank (e.g. cash payment), partner_bank_vat is not set.
            partner_bank_vat = partner_bank.l10n_mx_edi_vat

        payment_account_ord = re.sub(r'\s+', '', bank_accounts[:1].acc_number or '') or None
        payment_account_receiver = re.sub(r'\s+', '', move.journal_id.bank_account_id.acc_number or '') or None

        # CFDI 4.0: prepare the tax summaries
        rate_payment_curr_mxn_40 = rate_payment_curr_mxn or 1
        total_taxes_paid = {}
        total_taxes_withheld = {
            '001': {'amount_curr': 0.0, 'amount_mxn': 0.0},
            '002': {'amount_curr': 0.0, 'amount_mxn': 0.0},
            '003': {'amount_curr': 0.0, 'amount_mxn': 0.0},
            None: {'amount_curr': 0.0, 'amount_mxn': 0.0},
        }
        for inv_vals in invoice_vals_list:
            wht_detail = list(inv_vals['tax_details_withholding']['tax_details'].values())
            trf_detail = list(inv_vals['tax_details_transferred']['tax_details'].values())
            for detail in wht_detail + trf_detail:
                tax = detail['tax']
                tax_class = detail['tax_class']
                key = (float_round(tax.amount / 100, 6), tax.l10n_mx_tax_type, tax_class)
                base_val_pay_curr = detail['base_val_prop_amt_curr'] / (inv_vals['exchange_rate'] or 1.0)
                tax_val_pay_curr = detail['tax_val_prop_amt_curr'] / (inv_vals['exchange_rate'] or 1.0)
                if key in total_taxes_paid:
                    total_taxes_paid[key]['base_value'] += base_val_pay_curr
                    total_taxes_paid[key]['tax_value'] += tax_val_pay_curr
                elif tax.amount >= 0:
                    total_taxes_paid[key] = {
                        'base_value': base_val_pay_curr,
                        'tax_value': tax_val_pay_curr,
                        'tax_amount': float_round(detail['tax_amount'], 6),
                        'tax_type': tax.l10n_mx_tax_type,
                        'tax_class': tax_class,
                        'tax_spec': 'W' if tax.amount < 0 else 'T',
                    }
                else:
                    total_taxes_withheld[tax_class]['amount_curr'] += tax_val_pay_curr

        # CFDI 4.0: rounding needs to be done after all DRs are added
        # We round up for the currency rate and down for the tax values because we lost a lot of time to find out
        # that Finkok only accepts it this way.  The other PACs accept either way and are reasonable.
        for v in total_taxes_paid.values():
            v['base_value'] = float_round(v['base_value'], 6, rounding_method='DOWN')
            v['tax_value'] = float_round(v['tax_value'], 6, rounding_method='DOWN')
            v['base_value_mxn'] = float_round(v['base_value'] * rate_payment_curr_mxn_40, 6)
            v['tax_value_mxn'] = float_round(v['tax_value'] * rate_payment_curr_mxn_40, 6)
        for v in total_taxes_withheld.values():
            v['amount_curr'] = float_round(v['amount_curr'], 2, rounding_method='DOWN')
            v['amount_mxn'] = float_round(v['amount_curr'] * rate_payment_curr_mxn_40, 2)

        cfdi_values = {
            **self._l10n_mx_edi_get_common_cfdi_values(move),
            'invoice_vals_list': invoice_vals_list,
            'currency': currency,
            'amount': round(total_amount,2),
            'amount_mxn': float_round(total_amount * rate_payment_curr_mxn_40, 2),
            'rate_payment_curr_mxn': rate_payment_curr_mxn,
            'rate_payment_curr_mxn_40': rate_payment_curr_mxn_40,
            'emitter_vat_ord': is_payment_code_emitter_ok and partner_bank_vat,
            'bank_vat_ord': is_payment_code_bank_ok and partner_bank.name,
            'payment_account_ord': is_payment_code_emitter_ok and payment_account_ord,
            'receiver_vat_ord': is_payment_code_receiver_ok and move.journal_id.bank_account_id.bank_id.l10n_mx_edi_vat,
            'payment_account_receiver': is_payment_code_receiver_ok and payment_account_receiver,
            'cfdi_date': move.l10n_mx_edi_post_time.strftime('%Y-%m-%dT%H:%M:%S'),
            'tax_summary': total_taxes_paid,
            'withholding_summary': total_taxes_withheld,
        }

        cfdi_payment_datetime = datetime.combine(fields.Datetime.from_string(move.date), datetime.strptime('12:00:00', '%H:%M:%S').time())
        cfdi_values['cfdi_payment_date'] = cfdi_payment_datetime.strftime('%Y-%m-%dT%H:%M:%S')

        if cfdi_values['customer'].country_id.l10n_mx_edi_code != 'MEX':
            cfdi_values['customer_fiscal_residence'] = cfdi_values['customer'].country_id.l10n_mx_edi_code
        else:
            cfdi_values['customer_fiscal_residence'] = None

        cfdi_values.update(self._l10n_mx_edi_get_40_values(move))
        return cfdi_values
