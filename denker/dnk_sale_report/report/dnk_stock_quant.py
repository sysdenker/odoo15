# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import tools
from odoo import api, fields, models


class DnkStockQuant(models.Model):
    _name = "dnk.stock.quant"
    _description = "Denker Stock Quant"
    _auto = False
    _rec_name = 'name'
    _order = 'in_date desc'

    id = fields.Many2one('stock.quant', 'Stock Quant', readonly=True)
    stock_id = fields.Many2one('stock.quant', 'Stock Quant', readonly=True)
    x_comment = fields.Text("+ Comments", readonly=True)
    company_id = fields.Many2one('res.company', 'Company', readonly=True)
    in_date = fields.Datetime('Incoming Date', readonly=True)
    product_id = fields.Many2one('product.product', 'Product', readonly=True)
    product_tmpl_id = fields.Many2one('product.template', 'Template', readonly=True)
    dnk_subfamily_id = fields.Many2one('product.category', string='- Subfamily', readonly=True)
    dnk_family_id = fields.Many2one('product.category', string='- Family', readonly=True)
    dnk_color_id = fields.Many2one('product.category', string='- Color', readonly=True)
    warehouse_id = fields.Many2one('stock.warehouse', string='- Warehouse', readonly=True)
    name = fields.Char('Warehouse Name', readonly=True)
    quantity_on_hand = fields.Float('Quantity', readonly=True)
    reserved_quantity = fields.Float('Reserved Quantity', readonly=True)
    available_quantity = fields.Float('Available Quantity', readonly=True)
    total_cost = fields.Float('Cost', readonly=True)
    available_cost = fields.Float('Available Cost', readonly=True)
    dnk_stock_move_line_last_sale_id = fields.Many2one('stock.move.line', 'Last Sale', readonly=True)
    last_sale_date = fields.Datetime('Last Sale Date', readonly=True)
    last_sale_qty = fields.Float('Last Sale Qty', readonly=True)
    last_sale_reference = fields.Char('Last Sale Reference', readonly=True)
    x_studio_location_type_sale = fields.Char('Sale Location Type', readonly=True)
    last_sale_days = fields.Float('Last Sale Days', readonly=True)
    dnk_stock_move_line_last_input_id = fields.Many2one('stock.move.line', 'Last Input', readonly=True)
    last_move_in_date = fields.Datetime('Last input Date', readonly=True)
    last_move_in_qty = fields.Float('Last Input Qty', readonly=True)
    last_move_in_reference = fields.Char('Last Input Reference', readonly=True)
    x_studio_location_type_origin = fields.Char('Input Location Type', readonly=True)
    last_input_days = fields.Float('Last Input Days', readonly=True)
    dnk_stock_move_line_last_output_id = fields.Many2one('stock.move.line', 'Last Output', readonly=True)
    last_move_out_date = fields.Datetime('Last Output Date', readonly=True)
    last_move_out_qty = fields.Float('Last Output Qty', readonly=True)
    last_move_out_reference = fields.Char('Last Output Reference', readonly=True)
    x_studio_location_type_destination = fields.Char('Output Location Type', readonly=True)
    last_output_days = fields.Float('Last Output Days', readonly=True)
    stock_warehouse_orderpoint_id = fields.Many2one('stock.warehouse.orderpoint', 'Minimum Inventory Rule', readonly=True)
    product_min_qty = fields.Float('Min Product Qty', readonly=True)
    product_max_qty = fields.Float('Max Product Qty', readonly=True)


    def _query(self, with_clause='', fields={}, groupby='', from_clause='', where=''):
        with_ = ("WITH %s" % with_clause) if with_clause else ""

        select_ = """
            stock_quant.id,
            stock_quant.x_comment,
            stock_quant.company_id,
            stock_quant.in_date,
            stock_quant.product_id,
            dnk_product_catalog.product_tmpl_id,
            dnk_product_catalog.dnk_family_id,
            dnk_product_catalog.dnk_subfamily_id,
            dnk_product_catalog.dnk_color_id,
            stock_warehouse.id AS warehouse_id,
            stock_warehouse.name,
            SUM(stock_quant.quantity) AS quantity_on_hand,
            SUM(stock_quant.reserved_quantity) AS reserved_quantity,
            SUM(stock_quant.quantity-stock_quant.reserved_quantity) AS available_quantity,
            SUM(ir_property.value_float) AS cost, SUM(ir_property.value_float * stock_quant.quantity) AS total_cost,
            SUM(ir_property.value_float * (stock_quant.quantity-stock_quant.reserved_quantity)) AS available_cost,
            smlls.id AS dnk_stock_move_line_last_sale_id,
            smlls.date AS last_sale_date,
            smlls.qty_done AS last_sale_qty,
            smlls.reference AS last_sale_reference,
            smlls.x_studio_location_type_destination AS x_studio_location_type_sale,
            smlls.last_sale_days,
            smlli.id as dnk_stock_move_line_last_input_id,
            smlli.date AS last_move_in_date,
            smlli.qty_done AS last_move_in_qty,
            smlli.reference AS last_move_in_reference,
            smlli.x_studio_location_type_origin,
            smlli.last_input_days,
            smllo.id AS dnk_stock_move_line_last_output_id,
            smllo.date AS last_move_out_date,
            smllo.qty_done AS last_move_out_qty,
            smllo.reference AS last_move_out_reference,
            smllo.x_studio_location_type_destination,
            smllo.last_output_days,
            MIN(swo.product_min_qty) AS product_min_qty,
            MAX(swo.product_max_qty) AS product_max_qty
        """

        for field in fields.values():
            select_ += field

        from_ = """
                stock_quant
                LEFT JOIN dnk_product_catalog ON dnk_product_catalog.product_id = stock_quant.product_id
                LEFT JOIN stock_warehouse ON stock_warehouse.id = stock_quant.x_studio_warehouse

                -- Para traer el nombre del almacen y el Min y Max
                LEFT JOIN (SELECT company_id, warehouse_id, product_id, MIN(product_min_qty) AS product_min_qty, MAX(product_max_qty) AS product_max_qty
                			FROM stock_warehouse_orderpoint
                		    GROUP BY company_id, warehouse_id, product_id) as swo
                			ON swo.company_id = stock_quant.company_id
                			AND swo.warehouse_id = stock_quant.x_studio_warehouse
                			AND swo.product_id = stock_quant.product_id

                -- Para traer la ultima ENTRADA con su referencia y el maximo de cantidad
                LEFT JOIN (SELECT smlli.company_id, smlli.product_id, smlli.x_studio_warehouse, smlli.date, sml.qty_done, sml.reference,
                		   sml.id, sml.x_studio_location_type_origin, DATE_PART('day',NOW() - sml.date) AS last_input_days
                		   FROM dnk_stock_move_line_last_input AS smlli
                		   LEFT JOIN stock_move_line AS sml
                				ON smlli.id = sml.id
                		   		AND smlli.company_id = sml.company_id
                				AND smlli.product_id = sml.product_id) AS smlli
                			ON smlli.id = stock_quant.id

                -- Para traer la ultima SALIDA con su referencia y el maximo de cantidad
                LEFT JOIN (SELECT smllo.company_id, smllo.product_id, smllo.x_studio_warehouse, smllo.date, sml.qty_done, sml.reference,
                		   sml.id, sml.x_studio_location_type_destination, DATE_PART('day',NOW() - sml.date) AS last_output_days
                		   FROM dnk_stock_move_line_last_output as smllo
                		   LEFT JOIN stock_move_line AS sml
                				ON smllo.id = sml.id
                		   		AND smllo.company_id = sml.company_id
                				AND smllo.product_id = sml.product_id) AS smllo
                			ON smllo.id = stock_quant.id

                -- Para traer la ultima VENTA con su referencia y el maximo de cantidad
                LEFT JOIN (SELECT smlls.company_id, smlls.product_id, smlls.x_studio_warehouse, smlls.date, sml.qty_done, sml.reference,
                		   sml.id, sml.x_studio_location_type_destination, DATE_PART('day',NOW() - sml.date) AS last_sale_days
                		   FROM dnk_stock_move_line_last_sale AS smlls
                		   LEFT JOIN stock_move_line AS sml
                				ON smlls.id = sml.id
                		   		AND smlls.company_id = sml.company_id
                				AND smlls.product_id = sml.product_id) AS smlls
                			ON smlls.id = stock_quant.id

                -- Para traer el costo del prodcuto
                LEFT JOIN ir_property
                		   	ON ir_property.res_id = 'product.product,' || stock_quant.product_id
                			AND ir_property.company_id = stock_quant.company_id
                			AND ir_property.name = 'standard_price'

                %s
        """ % from_clause

        groupby_ = """
                stock_quant.id,stock_quant.x_comment,stock_quant.company_id, stock_quant.in_date, stock_quant.product_id,
                dnk_product_catalog.product_tmpl_id, dnk_product_catalog.dnk_family_id,
                dnk_product_catalog.dnk_subfamily_id, dnk_product_catalog.dnk_color_id,
                stock_warehouse.id, stock_warehouse.name,
                smlli.id, smlli.date, smlli.qty_done, smlli.reference,
                smlli.x_studio_location_type_origin, smlli.last_input_days,
                smllo.id, smllo.date, smllo.qty_done, smllo.reference,
                smllo.x_studio_location_type_destination, smllo.last_output_days,
                smlls.id, smlls.date, smlls.qty_done, smlls.reference,
                smlls.x_studio_location_type_destination, smlls.last_sale_days
            %s
        """ % (groupby)

        where_ = """
            stock_quant.x_studio_location_type = 'internal'
        """

        return '%s (SELECT %s FROM %s WHERE %s GROUP BY %s)' % (with_, select_, from_, where_, groupby_)

    def init(self):
        self._table = "dnk_stock_quant"
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute("""CREATE or REPLACE VIEW %s as (%s) """ % (self._table, self._query()))


class DnkStockQuantProforma(models.AbstractModel):
    _name = 'dnk.stock.quant.proforma'
    _description = 'Denker Stock Quant Report'

    def _get_report_values(self, docids, data=None):
        docs = self.env['dnk.stock.quant.proforma'].browse(docids)
        return {
                'doc_ids': docs.ids,
                'doc_model': 'dnk.stock.quant',
                'docs': docs,
                'proforma': True
            }
