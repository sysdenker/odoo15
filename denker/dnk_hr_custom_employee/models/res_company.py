
# -*- coding: utf-8 -*-
from odoo import api, fields, models
from datetime import date
from .amount_to_text_es_MX import amount_to_text
import locale


def date_to_words(self, date_value):
    sep = ' de '

    if not date_value:
        return
    date_value = fields.Datetime.from_string(date_value)
    # context_timestamp(datetime.datetime.now()).strftime('%A, %d de %B de %Y')
    lang = 'es_ES'
    locale.setlocale(locale.LC_TIME, lang + '.utf8')
    return amount_to_text().amount_to_text(date_value.day) + sep + date_value.strftime('%B').lower() + sep + amount_to_text().amount_to_text(date_value.year)


class ResCompany(models.Model):
    _inherit = 'res.company'

    @api.depends('dnk_deed_date')
    def _get_date_to_text(self):
        for rec in self:
            rec.dnk_deed_date_text = date_to_words(self, rec.dnk_deed_date)

    # Número de Escritura
    dnk_deed_number = fields.Char(
        string='- Deed Number', required=True,
        help='Legal deed number of the company')
    # Fecha de Escritura (Date y Char)
    dnk_deed_date = fields.Date(
        string='- Deed Date', required=True,
        help='Certificate of incorporation date')
    dnk_deed_date_text = fields.Char(
        string='- Deed Date Text',
        compute='_get_date_to_text', store=True,
        help='Certificate of incorporation date text')

    # Descripción del Giro
    dnk_line_of_business = fields.Char(
        string='- Line of Business', required=True,
        help='The main activity of the company')

    # Representante Legal
    # dnk_legal_representative = fields.Char(string='- Legal Representative', required=True,
    #                            help='Legal representative person of the company')
    dnk_legal_representative = fields.Many2one(
        'res.partner', domain=[('type', '=', 'contact')], string='- Legal Representative', required=True,ondelete='cascade',
        help='Legal representative person of the company')

    dnk_public_notary_name = fields.Char(string='- Name', required=True, size=32)
    dnk_public_notary_number = fields.Char(string='- Number', required=True, size=4)
    dnk_public_notary_municipality = fields.Char(string='- Municipality', required=True, size=16)
    dnk_public_notary_state_id = fields.Many2one(
        'res.country.state', string='- State', required=True)
    # Campos del contrato de "AVISO DE PRIVACIDAD"
    dnk_notice_of_privacy_representative = fields.Many2one(
        'res.partner', domain=[('type', '=', 'contact')], string='- Representative',
        required=True,ondelete='cascade', help='"Notice of Privacy" representative person of the company')
    dnk_notice_of_privacy_email = fields.Char(string='- Email', required=True, size=32)
    dnk_notice_of_privacy_phone = fields.Char(string='- Phone', required=True, size=16)
