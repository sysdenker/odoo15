# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class AccountInvoiceReport(models.Model):
    _inherit = 'account.invoice.report'

    dnk_crm_lead_id = fields.Many2one('crm.lead', string='- Opportunity', readonly=True)
    medium_id = fields.Many2one('utm.medium', '- Medium')

    def _select(self):
        select_crm_lead_id = ",sale.opportunity_id AS dnk_crm_lead_id, lead.medium_id AS medium_id"

        return super(AccountInvoiceReport, self)._select() + select_crm_lead_id

    def _from(self):
        select_add_sale_order = """
            LEFT JOIN sale_order sale ON move.dnk_order_id = sale.id
            LEFT JOIN crm_lead lead ON sale.opportunity_id = lead.id
        """

        return super(AccountInvoiceReport, self)._from() + select_add_sale_order

    def _group_by(self):
        select_group = ", sale.opportunity_id, lead.medium_id"
        return super(AccountInvoiceReport, self)._group_by() + select_group
