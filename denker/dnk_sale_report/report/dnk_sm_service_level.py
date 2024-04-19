# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import tools
from odoo import api, fields, models


class SaleReport(models.Model):
    _name = "dnk.sm.service.level"
    _description = "Denker Service Level Report"
    _auto = False
    _rec_name = 'sm_origin'
    _order = 'sm_commitment_date desc'

    id = fields.Integer("", readonly=True)
    sm_sale_order_id = fields.Many2one('sale.order', 'Sale Order', readonly=True)
    sm_origin = fields.Char('Source Document', readonly=True)
    sm_open_sale_order = fields.Boolean('Pedido Abierto', readonly=True)
    sm_date_order = fields.Datetime('SO Commitment_date', readonly=True)
    dnk_family_id = fields.Many2one('product.category', string='- Family', readonly=True)

    sm_date = fields.Datetime('Date Scheduled', readonly=True)

    sm_commitment_date = fields.Datetime('Date Scheduled', readonly=True)
    sm_ns = fields.Integer('Service Level', group_operator="min",readonly=True)
    sm_customer_id = fields.Many2one('res.partner', 'Cliente', readonly=True)
    sm_sales_team_id = fields.Many2one('crm.team', 'Equipo de Ventas', readonly=True)
    company_id = fields.Many2one('res.company', 'Company', readonly=True)

    def _query(self, with_clause='', fields={}, groupby='', from_clause='', where=''):
        with_ = ("WITH %s" % with_clause) if with_clause else ""

        select_ = """
            stock_move.x_order AS id, stock_move.x_order AS sm_sale_order_id,
            stock_move.origin AS sm_origin,
            stock_move.x_open_order AS sm_open_sale_order,
            MIN(stock_move.x_date_order) AS sm_date_order,
            MAX(stock_move.date) AS sm_date,
            MAX(stock_move.x_commitment_date) AS sm_commitment_date,
            CASE WHEN MAX(stock_move.x_commitment_date) >= MAX(stock_move.date)
                THEN 1
                ELSE 0
            END AS sm_ns,
            stock_move.x_customer AS sm_customer_id,
            stock_move.x_teamsale AS sm_sales_team_id,
            stock_move.x_familia AS dnk_family_id,
            stock_move.x_subfamilia AS dnk_subfamily_id,
            SUM(sale_order_line.dnk_confirmation_count) AS sm_confirmation_count,
            stock_move.company_id
        """

        for field in fields.values():
            select_ += field

        from_ = """
                stock_move
                LEFT JOIN sale_order_line ON sale_order_line.id = stock_move.sale_line_id
                %s
        """ % from_clause

        groupby_ = """
            stock_move.x_order, stock_move.origin, stock_move.x_open_order,
            stock_move.x_customer, stock_move.x_teamsale, stock_move.x_familia,
            stock_move.x_subfamilia, stock_move.company_id
            %s
        """ % (groupby)

        where_ = """
            stock_move.x_location_type_dest = 'customer'
            AND stock_move.state not in ('draft','cancel')
        """

        return '%s (SELECT %s FROM %s WHERE %s GROUP BY %s)' % (with_, select_, from_, where_, groupby_)

    def init(self):
        # self._table = "dnk_sm_service_level"
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute("""CREATE or REPLACE VIEW %s as (%s)""" % (self._table, self._query()))


class DnkSaleReportProforma(models.AbstractModel):
    _name = 'dnk.sm.service.level.proforma'
    _description = 'Denker Service Level Report'

    def _get_report_values(self, docids, data=None):
        docs = self.env['dnk.sm.service.level.proforma'].browse(docids)
        return {
                'doc_ids': docs.ids,
                'doc_model': 'dnk.sm.service.level',
                'docs': docs,
                'proforma': True
            }
