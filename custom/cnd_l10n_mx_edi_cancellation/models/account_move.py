# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-TODAY Odoo S.A. <http://www.odoo.com>
#    @author Paramjit Singh A. Sahota <sahotaparamjitsingh@gmail.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
from odoo import models, fields, api, _
from odoo.exceptions import UserError
import re
import json

"""
Tipo de cancelación
Momento en el que se presenta

"01" Comprobante emitido con errores con relación
Este supuesto aplica cuando la factura generada contiene un error en la clave del producto, valor unitario, descuento o cualquier otro dato, por lo que se debe reexpedir. En este caso, primero se sustituye la factura y cuando se solicita la
cancelación, se incorpora el folio de la factura que sustituye a la cancelada

"02" Comprobante emitido con errores sin relación
Se aplica cuando la factura generada contiene un error en la clave del producto, valor unitario, descuento o cualquier otro dato y no se requiera relacionar con otra factura generada.

"03" No se llevó a cabo la operación
Se aplica cuando se facturó una operación que no se concreta

"04" Operación nominativa relacionada en la factura global
Este supuesto aplica cuando se incluye una venta en la factura global de operaciones con el público en general y posterior a ello, el cliente solicita su factura nominativa, lo que conlleva a cancelar la factura global y reexpedirla, así como generar la factura nominativa al cliente
"""


class AccountMove(models.Model):
    _inherit = 'account.move'

    l10n_mx_edi_cancellation_type = fields.Selection(
        [
         ('01', '"01" Comprobante emitido con errores con relación'),
         ('02', '"02" Comprobante emitido con errores sin relación'),
         ('03', '"03" No se llevó a cabo la operación'),
         ('04', '"04" Operación nominativa relacionada en la factura global')],
        string='Cancellation Type',
        copy=False,
        states={'posted': [('readonly', False)]},
        help='The SAT has 4 cases in which an invoice could be cancelled, please fill this field based on your case:\n'
             'Case 1: The invoice was generated with errors and must be re-invoiced, the format must be:\n'
             '"01|UUID", where the UUID is the fiscal folio of the new invoice generated to replace invoice to cancel.\n'
             'Case 2: The invoice has an error on the customer, this will be cancelled and replaced by a new with de correct customer. The format must be:\n'
             '"02", only is required the case number.\n'
             'Case 3: It is applied when an operation that does not materialize was billed. The format must be:\n'
             '"03", only is required the case number.\n'
             'Case 4: This assumption applies when a sale is included in the global invoice for operations with the general public and after that, the client requests '
             'his nominative invoice, which leads to cancel the global invoice and reissue it, as well as generate the nominative invoice to the customer. The format must be:\n'
             '"04", only is required the case number.\n')

    l10n_mx_edi_cancellation_related_uuid = fields.Char(
        string='Cancellation Fiscal Folio',
        copy=False,
        states={'posted': [('readonly', False)]},
        help='Fiscal Folio (UUID) related to the "Cancellation Type" selection, required only if the "Cancellation Type" is "01".')

    @api.onchange('l10n_mx_edi_cancellation_related_uuid')
    def _onchange_l10n_mx_edi_cancellation(self):
        if self.l10n_mx_edi_cancellation_type == '01':
            format = '^[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12}\Z'
            regex = re.compile(format, re.I)
            match = regex.match(self.l10n_mx_edi_cancellation_related_uuid)
            if not bool(match):
                raise UserError(
                    _('The format must be similar to "aa6635e1-e394-463b-b43d-69eb4c3a8570", please, verify if the UUID is correct.'))
        else:
            self.l10n_mx_edi_cancellation_related_uuid = False
