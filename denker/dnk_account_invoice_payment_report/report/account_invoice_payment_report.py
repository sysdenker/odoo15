# -*- coding: utf-8 -*-

from odoo import tools
from odoo import models, fields, api

from functools import lru_cache


class AccountInvoicePaymentReport(models.Model):
    _name = "account.invoice.payment.report"
    _description = "Invoices Statistics"
    _auto = False
    _rec_name = 'invoice_date'
    _order = 'invoice_date desc'

    # Nuevos campos
    account_invoice_amount_untaxed_usd = fields.Float(string='Invoice Amount Untaxed USD', readonly=True)
    team_id = fields.Many2one('crm.team', string='Sales Channel', readonly=True)
    payment_currency_id = fields.Many2one('res.currency', string='Payment Currency', readonly=True)
    payment_id = fields.Many2one('account.payment', string='Payment', readonly=True)
    date = fields.Date(string='Payment Date', readonly=True)
    dnk_usd_subtotal = fields.Float(string='Price Subtotal', readonly=True)
    prorated_payment_amount = fields.Float(string='Payment Amount', readonly=True)

    # ==== Invoice fields ====
    move_id = fields.Many2one('account.move', readonly=True)
    name = fields.Char('Invoice #', readonly=True)
    journal_id = fields.Many2one('account.journal', string='Journal', readonly=True)
    company_id = fields.Many2one('res.company', string='Company', readonly=True)
    currency_id = fields.Many2one('res.currency', string='Invoice Currency', readonly=True)
    partner_id = fields.Many2one('res.partner', string='Partner', readonly=True)
    commercial_partner_id = fields.Many2one('res.partner', string='Partner Company', help="Commercial Entity")
    country_id = fields.Many2one('res.country', string="Country")
    invoice_user_id = fields.Many2one('res.users', string='Salesperson', readonly=True)
    type = fields.Selection(
        [
            ('out_invoice', 'Customer Invoice'),
            ('in_invoice', 'Vendor Bill'),
            ('out_refund', 'Customer Credit Note'),
            ('in_refund', 'Vendor Credit Note'),
        ], readonly=True)
    state = fields.Selection(
        [
            ('draft', 'Draft'),
            ('posted', 'Open'),
            ('cancel', 'Cancelled')
        ], string='Invoice Status', readonly=True)
    invoice_payment_state = fields.Selection(selection=[
        ('not_paid', 'Not Paid'),
        ('in_payment', 'In Payment'),
        ('paid', 'paid')
    ], string='Payment Status', readonly=True)
    fiscal_position_id = fields.Many2one('account.fiscal.position', string='Fiscal Position', readonly=True)
    invoice_date = fields.Date(readonly=True, string="Invoice Date")
    invoice_payment_term_id = fields.Many2one('account.payment.term', string='Payment Terms', readonly=True)
    invoice_partner_bank_id = fields.Many2one('res.partner.bank', string='Bank Account', readonly=True)
    nbr_lines = fields.Integer(string='Line Count', readonly=True)
    residual = fields.Float(string='Due Amount', readonly=True)
    amount_total = fields.Float(string='Total', readonly=True)
    l10n_mx_edi_sat_status = fields.Selection(
        selection=[
            ('none', 'State not defined'),
            ('undefined', 'Not Synced Yet'),
            ('not_found', 'Not Found'),
            ('cancelled', 'Cancelled'),
            ('valid', 'Valid'),
        ],
        string='Invoice SAT status',
        help='Refers to the status of the invoice inside the SAT system.',
        readonly=True)
    l10n_mx_edi_sat_status_payment = fields.Selection(
        selection=[
            ('none', 'State not defined'),
            ('undefined', 'Not Synced Yet'),
            ('not_found', 'Not Found'),
            ('cancelled', 'Cancelled'),
            ('valid', 'Valid'),
        ],
        string='Payment SAT status',
        help='Refers to the status of the CFDI inside the SAT system.',
        readonly=True, copy=False, required=True, ondelete='cascade',
        tracking=True, default='undefined')

    # ==== Invoice line fields ====
    quantity = fields.Float(string='Product Quantity', readonly=True)
    product_id = fields.Many2one('product.product', string='Product', readonly=True)
    product_uom_id = fields.Many2one('uom.uom', string='Unit of Measure', readonly=True)
    product_categ_id = fields.Many2one('product.category', string='Product Category', readonly=True)
    invoice_date_due = fields.Date(string='Due Date', readonly=True)
    account_id = fields.Many2one('account.account', string='Revenue/Expense Account', readonly=True, domain=[('deprecated', '=', False)])
    analytic_account_id = fields.Many2one('account.analytic.account', string='Analytic Account', groups="analytic.group_analytic_accounting")
    price_subtotal = fields.Float(string='Untaxed Total', readonly=True)
    price_average = fields.Float(string='Average Price', readonly=True, group_operator="avg")

    dnk_subfamily_id = fields.Many2one('product.category', string='- Subfamily', readonly=True)
    dnk_family_id = fields.Many2one('product.category', string='- Family', readonly=True)
    dnk_color_id = fields.Many2one('product.category', string='- Color', readonly=True)
    # dnk_profit_margin_color = fields.Char('- Margin Color')

    _depends = {
        'account.move': [
            'name', 'state', 'type', 'partner_id', 'invoice_user_id', 'fiscal_position_id',
            'invoice_date', 'invoice_date_due', 'invoice_payment_term_id', 'invoice_partner_bank_id',
        ],
        'account.move.line': [
            'quantity', 'price_subtotal', 'amount_residual', 'balance', 'amount_currency',
            'move_id', 'product_id', 'product_uom_id', 'account_id', 'analytic_account_id',
            'journal_id', 'company_id', 'currency_id', 'partner_id',
        ],
        'product.product': ['product_tmpl_id'],
        'product.template': ['categ_id'],
        'uom.uom': ['category_id', 'factor', 'name', 'uom_type'],
        'res.currency.rate': ['currency_id', 'name'],
        'res.partner': ['country_id'],
    }

    @api.model
    def _select(self):
        return '''
            SELECT
                line.id,
                line.move_id,
                line.product_id,
                line.account_id,
                line.analytic_account_id,
                line.journal_id,
                line.company_id,
                line.company_currency_id                                    AS currency_id,
                line.partner_id AS commercial_partner_id,
                move.name,
                move.state,
                move.type,
                move.partner_id,
                move.invoice_user_id,
                move.fiscal_position_id,
                move.invoice_payment_state,
                move.invoice_date,
                move.invoice_date_due,
                move.invoice_payment_term_id,
                move.invoice_partner_bank_id,
                -line.balance * (move.amount_residual_signed / NULLIF(move.amount_total_signed, 0.0)) * (line.price_total / NULLIF(line.price_subtotal, 0.0))
                                                                            AS residual,
                -line.balance * (line.price_total / NULLIF(line.price_subtotal, 0.0))    AS amount_total,
                uom_template.id                                             AS product_uom_id,
                template.categ_id                                           AS product_categ_id,
                line.quantity / NULLIF(COALESCE(uom_line.factor, 1) / COALESCE(uom_template.factor, 1), 0.0)
                                                                            AS quantity,
                -line.balance                                               AS price_subtotal,
                -line.balance / NULLIF(COALESCE(uom_line.factor, 1) / COALESCE(uom_template.factor, 1), 0.0)
                                                                            AS price_average,
                COALESCE(partner.country_id, commercial_partner.country_id) AS country_id,
                1                                                           AS nbr_lines

                ,fam_category.dnk_color_id,fam_category.dnk_subfamily_id,fam_category.dnk_family_id,
                CASE WHEN aml_apr.currency_name IS NULL THEN (aml_apr.amount*(SELECT rcr.rate FROM res_currency rc
                INNER JOIN res_currency_rate rcr ON rc.id = rcr.currency_id
                WHERE rc.name = 'USD' AND rcr.name <= line.date ORDER BY rcr.name DESC LIMIT 1)/move.dnk_usd_amount)*line.dnk_usd_subtotal*move.untaxed_percent
                ELSE (aml_apr.amount_currency/move.dnk_usd_amount)*line.dnk_usd_subtotal*move.untaxed_percent
                END AS prorated_payment_amount, line.dnk_usd_subtotal, aml_apr.currency_id AS payment_currency_id,
                aml_apr.payment_id AS payment_id, aml_apr.date, move.team_id AS team_id,
                move.dnk_usd_amount AS account_invoice_amount_untaxed_usd, move.l10n_mx_edi_sat_status AS l10n_mx_edi_sat_status,
                aml_apr.l10n_mx_edi_sat_status_payment AS l10n_mx_edi_sat_status_payment
        '''

        #                CASE WHEN line.dnk_profit_margin_ratio >= 0.5 THEN 'Azul'
        #                WHEN line.dnk_profit_margin_ratio >= 0.4 THEN 'Verde'
        #                WHEN line.dnk_profit_margin_ratio >= 0.3 THEN 'Amarillo'
        #                WHEN line.dnk_profit_margin_ratio >= 0.2 THEN 'Gris'
        #                WHEN line.dnk_profit_margin_ratio >= 0.0 THEN 'Negro'
        #                WHEN line.dnk_profit_margin_ratio < 0.0 THEN 'Morado'
        #                END dnk_profit_margin_color

    @api.model
    def _from(self):
        return '''
            FROM account_move_line line
                LEFT JOIN res_partner partner ON partner.id = line.partner_id
                LEFT JOIN product_product product ON product.id = line.product_id
                LEFT JOIN account_account account ON account.id = line.account_id
                LEFT JOIN account_account_type user_type ON user_type.id = account.user_type_id
                LEFT JOIN product_template template ON template.id = product.product_tmpl_id
                LEFT JOIN uom_uom uom_line ON uom_line.id = line.product_uom_id
                LEFT JOIN uom_uom uom_template ON uom_template.id = template.uom_id
                INNER JOIN (SELECT *, CASE WHEN amount_tax < 0 THEN amount_untaxed/amount_untaxed WHEN amount_tax >= 0 THEN amount_untaxed/(amount_untaxed+amount_tax) END AS untaxed_percent FROM account_move) move ON move.id = line.move_id

                INNER JOIN (SELECT apr.id, aml.move_id, apr.credit_move_id, apr.amount, apr.amount_currency, rc.name AS currency_name, apr.currency_id, aml_credit.payment_id, aml_credit.date, ap.l10n_mx_edi_sat_status AS l10n_mx_edi_sat_status_payment
                FROM account_move_line aml
                INNER JOIN account_partial_reconcile apr ON aml.id = apr.debit_move_id
                INNER JOIN account_move_line aml_credit ON aml_credit.id = apr.credit_move_id
                LEFT JOIN res_currency rc ON apr.currency_id = rc.id
                LEFT JOIN account_payment ap ON ap.id = aml_credit.payment_id
                ) aml_apr ON move.id = aml_apr.move_id

                LEFT JOIN res_partner commercial_partner ON commercial_partner.id = move.commercial_partner_id

                LEFT JOIN
                (SELECT subfamily.id AS dnk_subfamily_id, subfamily.name AS  subfamily,
                family.id AS dnk_family_id, family.name AS family, color.id AS dnk_color_id, color.name AS color
                FROM product_category subfamily
                LEFT JOIN
                (SELECT pc2.id, pc2.name, pc2.parent_id FROM product_category pc2 WHERE pc2.parent_id IN
                (SELECT id FROM product_category WHERE parent_id IS NULL)) family  ON family.id = subfamily.parent_id
                LEFT JOIN
                (SELECT pc3.id,pc3.name FROM product_category pc3 WHERE pc3.parent_id IS NULL) color ON family.parent_id = color.id
                WHERE subfamily.parent_id IS NOT NULL AND subfamily.parent_id NOT IN (SELECT id FROM product_category WHERE parent_id IS NULL))
                AS fam_category ON template.categ_id = fam_category.dnk_subfamily_id
        '''

    @api.model
    def _where(self):
        return '''
            WHERE move.type IN ('out_invoice', 'out_refund', 'in_invoice', 'in_refund', 'out_receipt', 'in_receipt')
                AND line.account_id IS NOT NULL
                AND NOT line.exclude_from_invoice_tab
        '''

    @api.model
    def _group_by(self):
        return '''
            GROUP BY
                line.id,
                line.move_id,
                line.product_id,
                line.account_id,
                line.analytic_account_id,
                line.journal_id,
                line.company_id,
                line.currency_id,
                line.partner_id,
                move.name,
                move.state,
                move.type,
                move.amount_residual_signed,
                move.amount_total_signed,
                move.partner_id,
                move.invoice_user_id,
                move.fiscal_position_id,
                move.invoice_payment_state,
                move.invoice_date,
                move.invoice_date_due,
                move.invoice_payment_term_id,
                move.invoice_partner_bank_id,
                uom_template.id,
                uom_line.factor,
                template.categ_id,
                COALESCE(partner.country_id, commercial_partner.country_id)
                ,move.dnk_usd_amount,move.untaxed_percent,aml_apr.currency_name,aml_apr.amount_currency,aml_apr.amount
                ,fam_category.dnk_color_id,fam_category.dnk_subfamily_id,fam_category.dnk_family_id,
                aml_apr.currency_id,
                aml_apr.payment_id,
                aml_apr.date,
                move.team_id,
                move.l10n_mx_edi_sat_status,
                aml_apr.l10n_mx_edi_sat_status_payment
        '''
                # dnk_profit_margin_color

    def init(self):
        tools.drop_view_if_exists(self.env.cr, self._table)
        # print('CREATE OR REPLACE VIEW %s AS (%s %s %s %s)' % (self._table, self._select(), self._from(), self._where(), self._group_by()))
        self.env.cr.execute('''
            CREATE OR REPLACE VIEW %s AS (
                %s %s %s %s
            )
        ''' % (
            self._table, self._select(), self._from(), self._where(), self._group_by()
        ))

    @api.model
    def read_group(self, domain, fields, groupby, offset=0, limit=None, orderby=False, lazy=True):
        @lru_cache(maxsize=32)  # cache to prevent a SQL query for each data point
        def get_rate(currency_id):
            return self.env['res.currency']._get_conversion_rate(
                self.env['res.currency'].browse(currency_id),
                self.env.company.currency_id,
                self.env.company,
                self._fields['invoice_date'].today()
            )
        result = super(AccountInvoicePaymentReport, self).read_group(domain, fields, set(groupby) | {'currency_id'}, offset, limit, orderby, lazy)
        for res in result:
            if res.get('currency_id') and self.env.company.currency_id.id != res['currency_id'][0]:
                for field in {'amount_total', 'price_average', 'price_subtotal', 'residual'} & set(res):
                    res[field] = self.env.company.currency_id.round((res[field] or 0.0) * get_rate(res['currency_id'][0]))
        return result


""" Comentado por si más a delante es encesario
class ReportInvoiceWithPayment(models.AbstractModel):
    _name = 'report.account.report_invoice_with_payments'
    _description = 'Account report with payment lines'

    @api.model
    def _get_report_values(self, docids, data=None):
        return {
            'doc_ids': docids,
            'doc_model': 'account.move',
            'docs': self.env['account.move'].browse(docids),
            'report_type': data.get('report_type') if data else '',
        }"""
