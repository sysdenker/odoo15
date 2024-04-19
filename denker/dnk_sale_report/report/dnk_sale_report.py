# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import tools
from odoo import api, fields, models


class SaleReport(models.Model):
    _name = "dnk.sale.report"
    _description = "Denker Sale Report"
    _auto = False
    _rec_name = 'invoice_date'
    _order = 'invoice_date desc'

    id = fields.Integer("", readonly=True)
    move_id = fields.Many2one('account.move', 'Invoice', readonly=True)
    company_id = fields.Many2one('res.company', 'Company', readonly=True)
    journal_type = fields.Many2one('account.journal', 'Journal', readonly=True)
    analytic_account_id = fields.Many2one('account.analytic.account', 'Analytic Account', readonly=True)
    account_id = fields.Many2one('account.account', 'Account', readonly=True)
    dnk_crm_lead_id  = fields.Many2one('crm.lead', '	Lead/Opportunity', readonly=True)
    invoice_date = fields.Datetime('Invoice Date', readonly=True)
    name = fields.Char('Name', readonly=True)
    dnk_usd_subtotal = fields.Float('USD Subtotal', readonly=True)
    dnk_usd_residual = fields.Float('USD Residual', readonly=True)
    price_subtotal = fields.Float('Untaxed Total', readonly=True)
    commercial_partner_id = fields.Many2one('res.partner', 'Partner Company', readonly=True)
    team_id = fields.Many2one('crm.team', 'Sales Team', readonly=True)
    invoice_user_id = fields.Many2one('res.users', 'Salesperson', readonly=True)
    medium_id = fields.Many2one('utm.medium', 'Medium', readonly=True)

    def _query(self, with_clause='', fields={}, groupby='', from_clause='', where=''):
        with_ = ("WITH %s" % with_clause) if with_clause else ""

        select_ = """
            account_invoice_report.id,
            account_invoice_report.move_id,
            account_invoice_report.company_id, res_company.name AS company_name,
            account_journal.type AS journal_type,
            account_analytic_account.id AS analytic_account_id,
            account_analytic_account.name AS analytic_account_name,
            account_invoice_report.account_id,  account_account.name AS account_name,
            dnk_crm_lead_id,
            invoice_date,
            account_invoice_report.name AS name,
            dnk_usd_subtotal,
            dnk_usd_residual,
            price_subtotal,
            res_partner.id as commercial_partner_id,
            res_partner.name AS commercial_partner_name,
            account_invoice_report.team_id,
            invoice_user_id,
            medium_id
        """

        for field in fields.values():
            select_ += field

        from_ = """
                account_invoice_report
                LEFT JOIN account_journal on account_journal.id = account_invoice_report.journal_id
                LEFT JOIN account_analytic_account on account_analytic_account.id = account_invoice_report.analytic_account_id
                LEFT JOIN account_account on account_account.id = account_invoice_report.account_id
                LEFT JOIN res_partner on res_partner.id = account_invoice_report.commercial_partner_id
                LEFT JOIN res_company on res_company.id = account_invoice_report.company_id
                %s
        """ % from_clause

        groupby_ = """
            account_invoice_report.id, move_id, account_invoice_report.company_id,account_journal.type,
            account_analytic_account.id,account_invoice_report.account_id, account_account.name,
            account_invoice_report.dnk_crm_lead_id,account_invoice_report.invoice_date,
            account_invoice_report.name, account_invoice_report.dnk_usd_subtotal,
    		account_invoice_report.dnk_usd_residual, account_invoice_report.price_subtotal, res_partner.id,
    		account_invoice_report.team_id, account_invoice_report.invoice_user_id, account_invoice_report.medium_id,
            res_company.name
            %s
        """ % (groupby)

        where_ = """
            account_invoice_report.state NOT IN ('draft','cancel')
        	AND (account_analytic_account.name NOT ILIKE '%Estrategia operativa%'
        		AND account_analytic_account.name NOT ILIKE '%terceros%'
        		AND account_analytic_account.name NOT ILIKE '%cuotas por servicios denker%'
        		AND account_analytic_account.name NOT ILIKE '%Otras Ventas%'
        		OR account_analytic_account.name IS NULL)
         	AND (account_account.name NOT ILIKE'%Otras Ventas%'
         		AND account_account.name NOT ILIKE '%Anticipo%'
         		AND account_account.name NOT ILIKE '%Otros ingresos%'
         		AND account_account.name NOT ILIKE '%Activo%'
          		OR account_account.name IS NULL)
        	AND res_partner.name not ilike '%CLIENTE MUESTRAS%'
	        AND (account_invoice_report.type = 'out_invoice' or account_invoice_report.type = 'out_refund')
        """

        return '%s (SELECT %s FROM %s WHERE %s GROUP BY %s)' % (with_, select_, from_, where_, groupby_)

    def init(self):
        self._table = "dnk_sale_report"
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute("""CREATE or REPLACE VIEW %s as (%s)""" % (self._table, self._query()))


class DnkSaleReportProforma(models.AbstractModel):
    _name = 'dnk.sale.report.proforma'
    _description = 'Denker Sale Report'

    def _get_report_values(self, docids, data=None):
        docs = self.env['dnk.sale.report.proforma'].browse(docids)
        return {
                'doc_ids': docs.ids,
                'doc_model': 'dnk.sale.report',
                'docs': docs,
                'proforma': True
            }
