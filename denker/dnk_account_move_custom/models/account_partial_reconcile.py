# -*- coding: utf-8 -*-
from odoo import api, fields, models, _, Command
from odoo.exceptions import UserError, ValidationError

from datetime import date


class AccountPartialReconcile(models.Model):
    _inherit = 'account.partial.reconcile'

    def _collect_tax_cash_basis_values(self):
        ''' Collect all information needed to create the tax cash basis journal entries on the current partials.
        :return:    A dictionary mapping each move_id to the result of 'account_move._collect_tax_cash_basis_values'.
                    Also, add the 'partials' keys being a list of dictionary, one for each partial to process:
                        * partial:          The account.partial.reconcile record.
                        * percentage:       The reconciled percentage represented by the partial.
                        * payment_rate:     The applied rate of this partial.
        '''
        tax_cash_basis_values_per_move = {}

        if not self:
            return {}

        for partial in self:
            for move in {partial.debit_move_id.move_id, partial.credit_move_id.move_id}:

                # Collect data about cash basis.
                if move.id not in tax_cash_basis_values_per_move:
                    tax_cash_basis_values_per_move[move.id] = move._collect_tax_cash_basis_values()

                # Nothing to process on the move.
                if not tax_cash_basis_values_per_move.get(move.id):
                    continue
                move_values = tax_cash_basis_values_per_move[move.id]

                # Check the cash basis configuration only when at least one cash basis tax entry need to be created.
                journal = partial.company_id.tax_cash_basis_journal_id

                if not journal:
                    raise UserError(_("There is no tax cash basis journal defined for the '%s' company.\n"
                                      "Configure it in Accounting/Configuration/Settings") % partial.company_id.display_name)

                partial_amount = 0.0
                partial_amount_currency = 0.0
                rate_amount = 0.0
                rate_amount_currency = 0.0
                if partial.debit_move_id.move_id == move:
                    partial_amount += partial.amount
                    partial_amount_currency += partial.debit_amount_currency
                    rate_amount -= partial.credit_move_id.balance
                    rate_amount_currency -= partial.credit_move_id.amount_currency
                    source_line = partial.debit_move_id
                    counterpart_line = partial.credit_move_id
                if partial.credit_move_id.move_id == move:
                    partial_amount += partial.amount
                    partial_amount_currency += partial.credit_amount_currency
                    rate_amount += partial.debit_move_id.balance
                    rate_amount_currency += partial.debit_move_id.amount_currency
                    source_line = partial.credit_move_id
                    counterpart_line = partial.debit_move_id

                if move_values['currency'] == move.company_id.currency_id:
                    # Percentage made on company's currency.
                    percentage = partial_amount / move_values['total_balance']
                else:
                    # raise UserError(_("Mi error '%s'") % move_values)
                    if  move_values['total_amount_currency'] == 0:
                        percentage = 1
                    else:
                        # Percentage made on foreign currency.
                        percentage = partial_amount_currency / move_values['total_amount_currency']

                if source_line.currency_id != counterpart_line.currency_id:
                    # When the invoice and the payment are not sharing the same foreign currency, the rate is computed
                    # on-the-fly using the payment date.
                    payment_rate = self.env['res.currency']._get_conversion_rate(
                        counterpart_line.company_currency_id,
                        source_line.currency_id,
                        counterpart_line.company_id,
                        counterpart_line.date,
                    )
                elif rate_amount:
                    payment_rate = rate_amount_currency / rate_amount
                else:
                    payment_rate = 0.0

                partial_vals = {
                    'partial': partial,
                    'percentage': percentage,
                    'payment_rate': payment_rate,
                }

                # Add partials.
                move_values.setdefault('partials', [])
                move_values['partials'].append(partial_vals)

        # Clean-up moves having nothing to process.
        return {k: v for k, v in tax_cash_basis_values_per_move.items() if v}
