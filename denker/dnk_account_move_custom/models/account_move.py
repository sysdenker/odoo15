# -*- coding: utf-8 -*-

from odoo import api, fields, models


PPD_Forced = {8765}

class AccountMove(models.Model):
    _inherit = 'account.move'

    dnk_product_default_code = fields.Char(string='- Product Internal Reference', related='stock_move_id.product_id.default_code')



    # Por petición de finanzas, voy a reescribir esta función, se supone que se forzará para que con un cliente en específico, en las notas
    # de crédito siempre se establezca PPD.

    # 27/sep/2023 Ya no se va a utilizar esta función, ya no lo quisieron.
    """
    @api.depends('move_type', 'invoice_date_due', 'invoice_date', 'invoice_payment_term_id', 'invoice_payment_term_id.line_ids')
    def _compute_l10n_mx_edi_payment_policy(self):
        for move in self:
            if move.is_invoice(include_receipts=True) and move.invoice_date_due and move.invoice_date:
                if move.move_type == 'out_invoice':
                    # In CFDI 3.3 - rule 2.7.1.43 which establish that
                    # invoice payment term should be PPD as soon as the due date
                    # is after the last day of  the month (the month of the invoice date).
                    if move.invoice_date_due.month > move.invoice_date.month or \
                       move.invoice_date_due.year > move.invoice_date.year or \
                       len(move.invoice_payment_term_id.line_ids) > 1:  # to be able to force PPD
                        move.l10n_mx_edi_payment_policy = 'PPD'
                    else:
                        move.l10n_mx_edi_payment_policy = 'PUE'
                else:
                    move.l10n_mx_edi_payment_policy = 'PUE'
                    if move.partner_id.id in PPD_Forced or move.partner_id.parent_id.id in PPD_Forced:
                        move.l10n_mx_edi_payment_policy = 'PPD'

            else:
                move.l10n_mx_edi_payment_policy = False

    """
class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    dnk_product_default_code = fields.Char(string='- Product Internal Reference', related='product_id.default_code')

    def _prepare_edi_vals_to_export(self):
        ''' The purpose of this helper is the same as '_prepare_edi_vals_to_export' but for a single invoice line.
        This includes the computation of the tax details for each invoice line or the management of the discount.
        Indeed, in some EDI, we need to provide extra values depending the discount such as:
        - the discount as an amount instead of a percentage.
        - the price_unit but after subtraction of the discount.

        :return: A python dict containing default pre-processed values.
        '''
        self.ensure_one()

        if self.discount == 100.0:
            gross_price_subtotal = self.price_unit * self.quantity
        else:
            gross_price_subtotal = self.price_subtotal / (1 - self.discount / 100.0)

        res = {
            'line': self,
            'price_unit_after_discount': self.currency_id.round(self.price_unit * (1 - (self.discount / 100.0))),
            'price_subtotal_before_discount': gross_price_subtotal,
            'price_subtotal_unit': self.currency_id.round(self.price_subtotal / self.quantity) if self.quantity else 0.0,
            'price_total_unit': self.currency_id.round(self.price_total / self.quantity) if self.quantity else 0.0,
            'price_discount': gross_price_subtotal - self.price_subtotal,
            'price_discount_unit': (gross_price_subtotal - self.price_subtotal) / self.quantity if self.quantity else 0.0,
            'gross_price_total_unit': (gross_price_subtotal / self.quantity) if self.quantity else 0.0,
            'unece_uom_code': self.product_id.product_tmpl_id.uom_id._get_unece_code(),
        }
        return res
