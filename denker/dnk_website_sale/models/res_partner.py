# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models

class DnkEdiUsage(models.Model):
    _inherit = 'res.partner'

    def get_website_sale_edi_usage(self):
        selections = self.fields_get()['dnk_l10n_mx_edi_usage']['selection']
        return selections

class DnkEdiPaymentMethod(models.Model):
    _inherit = 'l10n_mx_edi.payment.method'

    def get_website_sale_EdiPaymentMethod(self):
        return self.sudo().search([])
