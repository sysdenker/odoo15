# -*- coding: utf-8 -*-

from odoo import api, models, fields, tools, _
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT, float_repr, is_html_empty, str2bool
from odoo.tests.common import Form
from odoo.exceptions import UserError

from datetime import datetime
from lxml import etree
from PyPDF2 import PdfFileReader
import base64
import markupsafe

import io

import logging

_logger = logging.getLogger(__name__)


DEFAULT_FACTURX_DATE_FORMAT = '%Y%m%d'


class AccountEdiFormat(models.Model):
    _inherit = 'account.edi.format'

    def _export_facturx(self, invoice):

        def format_date(dt):
            # Format the date in the Factur-x standard.
            dt = dt or datetime.now()
            return dt.strftime(DEFAULT_FACTURX_DATE_FORMAT)

        def format_monetary(number, currency):
            # Format the monetary values to avoid trailing decimals (e.g. 90.85000000000001).
            return float_repr(number, currency.decimal_places)

        self.ensure_one()
        # Create file content.
        template_values = {
            **invoice._prepare_edi_vals_to_export(),
            'tax_details': invoice._prepare_edi_tax_details(),
            'format_date': format_date,
            'format_monetary': format_monetary,
            'is_html_empty': is_html_empty,
        }

        xml_content = markupsafe.Markup("<?xml version='1.0' encoding='UTF-8'?>")
        xml_content += self.env.ref('account_edi_facturx.account_invoice_facturx_export')._render(template_values)
        return self.env['ir.attachment'].create({
            'name': 'factur-x.xml',
            'raw': xml_content.encode(),
            'mimetype': 'application/xml',
            'type': 'binary'
        })
