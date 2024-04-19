# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools


class SaleOrderPartner(models.Model):
    _inherit = "sale.order"

    def _prepare_invoice(self):
        res = super(SaleOrderPartner, self)._prepare_invoice()
        if self.website_id:
            payment_way = self.env['l10n_mx_edi.payment.method'].browse(5),
        else:
            payment_way = self.partner_id.commercial_partner_id.dnk_l10n_mx_edi_payment_method_id.id or False

        res.update({'fiscal_position_id': self.partner_id.commercial_partner_id.property_account_position_id.id or False,
                    'l10n_mx_edi_usage': self.partner_id.commercial_partner_id.dnk_l10n_mx_edi_usage or False,
                    'l10n_mx_edi_payment_method_id':payment_way, })
        return res
