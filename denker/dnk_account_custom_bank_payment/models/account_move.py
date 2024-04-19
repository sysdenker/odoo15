
# -*- coding: utf-8 -*-
from odoo import api, models, fields


class AccountMove(models.Model):
    _inherit = "account.move"

    # Agregar el código del Diario para generar el nombre del PDF con el formato del la localización mexicana (l10n_mx_edi)
    # report_name = ''${object.dnk_journal_code}-${(object.name or '').replace('/','-')}-MX-Payment-10'
    # filename = ('%s-%s-MX-Invoice-%s.xml' % (
    #            inv.journal_id.code, inv.name, version.replace('.', '-'))).replace('/', '')
    dnk_journal_code = fields.Char(string='- Journal Code', size=5, related='journal_id.code', help="The journal entries of this journal will be named using this prefix.")
    # dnk_pac_version = fields.Char(string='- PAC Version', size=3, default=lambda self: self.l10n_mx_edi_get_pac_version(), readonly=True)
    dnk_pac_version = fields.Char(string='- PAC Version', size=3, default='4.0', readonly=True)
