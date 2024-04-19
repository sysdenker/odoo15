# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import tools
from odoo import api, fields, models


class DnkStockMoveLastSale(models.Model):
    _name = "dnk.stock.move.line.last.sale"
    _description = "Denker Stock Move Line last Sale"
    _auto = False
    _rec_name = 'id'
    _order = 'id desc'

    id = fields.Many2one('stock.move.line', 'Stock Move Line', readonly=True)
    date = fields.Datetime('Date', readonly=True)
    company_id = fields.Many2one('res.company', 'Company', readonly=True)
    product_id = fields.Many2one('product.product', 'Product', readonly=True)
    x_studio_warehouse = fields.Many2one('stock.warehouse', '+ Almacen', readonly=True)
    x_studio_location_type_destination = fields.Char('Description on Picking', readonly=True)

    def _query(self, with_clause='', fields={}, groupby='', from_clause='', where=''):
        with_ = ("WITH %s" % with_clause) if with_clause else ""

        select_ = """
        MAX(sml.id) AS id,
        MAX(sml.date) AS date,
        sml.company_id,
        sml.product_id,
        stock_location.x_studio_warehouse
        """

        for field in fields.values():
            select_ += field

        from_ = """
            stock_move_line sml
            LEFT JOIN stock_location ON stock_location.id = sml.location_id
                %s
        """ % from_clause

        groupby_ = """
            sml.company_id, sml.product_id, stock_location.x_studio_warehouse
            %s
        """ % (groupby)

        where_ = """
            sml.state = 'done' -- AND sml.x_studio_location_type_destination = 'customer'
        """

        return '%s (SELECT %s FROM %s WHERE %s GROUP BY %s)' % (with_, select_, from_, where_, groupby_)
    def init(self):
        self._table = "dnk_stock_move_line_last_sale"
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute("""CREATE or REPLACE VIEW %s as (%s)""" % (self._table, self._query()))


class DnkProductCatalogProforma(models.AbstractModel):
    _name = 'dnk.stock.move.line.last.sale.proforma'
    _description = 'Denker Stock Move Last Sale Report'

    def _get_report_values(self, docids, data=None):
        docs = self.env['stock.move.line'].browse(docids)
        return {
                'doc_ids': docs.ids,
                'doc_model': 'dnk.stock.line.move.last.sale',
                'docs': docs,
                'proforma': True
            }
