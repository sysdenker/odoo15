# -*- coding: utf-8 -*-
from odoo import api, SUPERUSER_ID


def pre_init_hook(cr):
    env = api.Environment(cr, SUPERUSER_ID, {})
    email_template_edi_invoice = env.ref('account.email_template_edi_invoice', raise_if_not_found=False)
    if email_template_edi_invoice:
        report_name = "${object.l10n_mx_edi_cfdi_name and object.dnk_journal_code+'-'+(object.name or '').replace('/','')+'-MX-Invoice-'+(object.dnk_pac_version or '').replace('.','-')}"
        email_template_edi_invoice.with_context(lang='es_MX').sudo().write({'report_name': report_name})
        email_template_edi_invoice.with_context(lang='en_US').sudo().write({'report_name': report_name})

    mail_template_data_payment_receipt = env.ref('account.mail_template_data_payment_receipt', raise_if_not_found=False)
    if mail_template_data_payment_receipt:
        report_name = "${object.dnk_journal_code+'-'+(object.name or '').replace('/','-')+'-MX-Payment-10'}"
        mail_template_data_payment_receipt.with_context(lang='es_MX').sudo().write({'report_name': report_name})
        mail_template_data_payment_receipt.with_context(lang='en_US').sudo().write({'report_name': report_name})
