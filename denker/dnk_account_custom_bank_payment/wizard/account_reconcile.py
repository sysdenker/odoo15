# -*- coding: utf-8 -*-
from odoo import api, fields, models


class AccountMoveLineReconcile(models.TransientModel):
    _inherit = 'account.move.line.reconcile'

    """
    Descorregir un arreglo (FIX) de Odoo, porque en Denker tomamos el tipo de cambio que el cliente desea y no el del día del pago,
    sin esto, se dejan saldos en la facturas por la diferencia del tipo de cambio.
    Link: https://github.com/odoo/odoo/commit/b29172e4823fd45e6ba814df94b33657d8a0114f
    En el wizard es la línea 73 del archivo: sudo nano account/static/src/xml/account_reconciliation.xml
    """
    def trans_rec_get(self):
        context = self._context or {}
        credit = debit = 0
        lines = self.env['account.move.line'].browse(context.get('active_ids', []))
        for line in lines:
            if not line.full_reconcile_id:
                credit += line.credit
                debit += line.debit
        precision = self.env.user.company_id.currency_id.decimal_places
        writeoff = float_round(debit - credit, precision_digits=precision) + 0.0
        credit = float_round(credit, precision_digits=precision)
        debit = float_round(debit, precision_digits=precision)
        return {'trans_nbr': len(lines), 'credit': credit, 'debit': debit, 'writeoff': writeoff}
