# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import tools
from odoo import api, fields, models


class SaleReport(models.Model):
    _name = "dnk.stock.move.report"
    _description = "Stock Move Analysis Report"
    _auto = False
    _rec_name = 'date'
    _order = 'date desc'

    id = fields.Integer("", readonly=True)
    move_id = fields.Many2one('stock.move', 'Stock Move', readonly=True)
    move_line_id = fields.Many2one('stock.move.line', 'Move Line', readonly=True)
    product_id = fields.Many2one('product.product', 'Product', readonly=True)
    company_id = fields.Many2one('res.company', 'Company', readonly=True)
    picking_id = fields.Many2one('stock.picking', 'Stock Picking', readonly=True)
    product_uom_id = fields.Many2one('uom.uom', 'Unit of Measure', readonly=True)
    product_qty = fields.Float('Real Reserved Quantity', readonly=True)
    product_uom_qty = fields.Float('Reserved', readonly=True)
    qty_done = fields.Float('Done', readonly=True)
    package_id = fields.Many2one('stock.quant.package', 'Source Package', readonly=True)
    package_level_id = fields.Many2one('stock.package_level', 'Package Level', readonly=True)
    lot_id = fields.Many2one('stock.production.lot', 'Lot/Serial Number', readonly=True)
    lot_name = fields.Char('Lot/Serial Number Name', readonly=True)
    result_package_id = fields.Many2one('stock.quant.package', 'Destination Package', readonly=True)
    date = fields.Datetime('Date', readonly=True)
    owner_id = fields.Many2one('res.partner', 'From Owner', readonly=True)

    location_id = fields.Many2one('stock.location', 'From', readonly=True)
    location_dest_id = fields.Many2one('stock.location', 'To', readonly=True)

    state = fields.Selection([
        ('draft', 'New'), ('cancel', 'Cancelled'),
        ('waiting', 'Waiting Another Move'),
        ('confirmed', 'Waiting Availability'),
        ('partially_available', 'Partially Available'),
        ('assigned', 'Available'),
        ('done', 'Done')], string='Status', readonly=True)
    reference = fields.Char('Reference', readonly=True)

    creation_date = fields.Datetime("Creation Date", readonly=True)

    origin = fields.Char(related='move_id.origin', string='Source')
    picking_type_entire_packs = fields.Boolean(related='picking_id.picking_type_id.show_entire_packs', readonly=True)
    description_picking = fields.Text(string="Description picking")
    categ_id = fields.Many2one('product.category', 'Product Category', readonly=True)

    # Aquí empieza Stock Move
    operation_type = fields.Char("Operation Type", readonly=True)
    inventory_id = fields.Many2one('stock.inventory', 'Inventory Adjustment', readonly=True)
    # Campos de Stock Picking
    date_done = fields.Datetime("Transfer Date", readonly=True)
    partner_id = fields.Many2one('res.partner', 'Partner', readonly=True)
    scheduled_date = fields.Datetime("Expected Date", readonly=True)
    picking_type_code = fields.Selection([
        ('incoming', 'Vendors'),
        ('outgoing', 'Customers'),
        ('internal', 'Internal')], string="Type", readonly=True)
    # Tal vez  pueda relacionar todo
    delay = fields.Float("Delay (Days)", readonly=True)
    cycle_time = fields.Float("Cycle Time (Days)", readonly=True)
    """
    name = fields.Char('Description', readonly=True)
    sequence = fields.Integer('Sequence', readonly=True)
    priority = fields.Selection(PROCUREMENT_PRIORITIES, string='Priority', readonly=True)
    create_date = fields.Datetime('Creation Date', readonly=True)
    date = fields.Datetime('Date', readonly=True)

    date_expected = fields.Datetime('Expected Date', readonly=True, help="Scheduled date for the processing of this move")
    description_picking = fields.Text('Description of Picking', readonly=True)
    product_qty = fields.Float('Real Quantity', readonly=True)
    product_uom_qty = fields.Float('Initial Demand', readonly=True)
    product_uom_category_id = fields.Many2one(related='product_id.uom_id.category_id')
    product_tmpl_id = fields.Many2one('product.template', related='product_id.product_tmpl_id', 'Product Template', readonly=True)
    location_id = fields.Many2one('stock.location', 'Source Location', readonly=True)
    location_dest_id = fields.Many2one('stock.location', 'Destination Location', readonly=True)
    partner_id = fields.Many2one('res.partner', 'Destination Address ', readonly=True)
    # move_dest_ids = fields.Many2many('stock.move', 'Destination Moves', readonly=True)
    # move_orig_ids = fields.Many2many('stock.move', 'Original Move', readonly=True)
    picking_id = fields.Many2one('stock.picking', 'Transfer Reference', readonly=True)
    picking_partner_id = fields.Many2one('res.partner', 'Transfer Destination Address', related='picking_id.partner_id', readonly=True)
    note = fields.Text('Notes', readonly=True)
    state = fields.Selection([
        ('draft', 'New'), ('cancel', 'Cancelled'),
        ('waiting', 'Waiting Another Move'),
        ('confirmed', 'Waiting Availability'),
        ('partially_available', 'Partially Available'),
        ('assigned', 'Available'),
        ('done', 'Done')], string='Status', readonly=True)
    price_unit = fields.Float('Unit Price', readonly=True)
    backorder_id = fields.Many2one('stock.picking', 'Back Order of', related='picking_id.backorder_id', readonly=True)
    origin = fields.Char("Source Document", readonly=True)
    procure_method = fields.Selection([
        ('make_to_stock', 'Default: Take From Stock'),
        ('make_to_order', 'Advanced: Apply Procurement Rules')], string='Supply Method', readonly=True)
    scrapped = fields.Boolean('Scrapped', related='location_dest_id.scrap_location', readonly=True)
    scrap_ids = fields.One2many('stock.scrap', 'move_id', readonly=True)
    group_id = fields.Many2one('procurement.group', 'Procurement Group', readonly=True)
    rule_id = fields.Many2one('stock.rule', 'Stock Rule', oreadonly=True)
    propagate_cancel = fields.Boolean('Propagate cancel and split', readonly=True)
    propagate_date = fields.Boolean(string="Propagate Rescheduling", readonly=True)
    propagate_date_minimum_delta = fields.Integer(string='Reschedule if Higher Than', readonly=True)
    delay_alert = fields.Boolean('Alert if Delay', readonly=True)
    picking_type_id = fields.Many2one('stock.picking.type', 'Operation Type', readonly=True)
    inventory_id = fields.Many2one('stock.inventory', 'Inventory', readonly=True)
    move_line_ids = fields.One2many('stock.move.line', 'move_id', readonly=True)
    move_line_nosuggest_ids = fields.One2many('stock.move.line', 'move_id', readonly=True)
    origin_returned_move_id = fields.Many2one('stock.move', 'Origin return move', readonly=True)
    returned_move_ids = fields.One2many('stock.move', 'origin_returned_move_id', 'All returned moves', readonly=True)
    reserved_availability = fields.Float('Quantity Reserved', readonly=True)
    availability = fields.Float('Forecasted Quantity', readonly=True)
    string_availability_info = fields.Text('Availability', readonly=True)
    restrict_partner_id = fields.Many2one('res.partner', 'Owner ', readonly=True)
    ###
    route_ids = fields.Many2many('stock.location.route', 'Destination route', readonly=True)
    ###
    warehouse_id = fields.Many2one('Warehouse', readonly=True)
    ###
    has_tracking = fields.Selection(related='product_id.tracking', string='Product with Tracking')
    quantity_done = fields.Float('Quantity Done', readonly=True)
    show_reserved_availability = fields.Boolean('From Supplier', readonly=True)
    picking_code = fields.Selection(related='picking_id.picking_type_id.code', readonly=True)
    product_type = fields.Selection(related='product_id.type', readonly=True)
    additional = fields.Boolean("Whether the move was added after the picking's confirmation", readonly=True)
    is_locked = fields.Boolean(readonly=True)
    is_initial_demand_editable = fields.Boolean('Is initial demand editable', readonly=True)
    is_quantity_done_editable = fields.Boolean('Is quantity done editable', readonly=True)

    has_move_lines = fields.Boolean(readonly=True)
    package_level_id = fields.Many2one('stock.package_level', 'Package Level', readonly=True)
    picking_type_entire_packs = fields.Boolean(related='picking_type_id.show_entire_packs', readonly=True)
    display_assign_serial = fields.Boolean(readonly=True)
    """

    def _query(self, with_clause='', fields={}, groupby='', from_clause=''):
        with_ = ("WITH %s" % with_clause) if with_clause else ""

        select_ = """
            move_line.id,
            move_line.id AS move_line_id,
            move_line.move_id,
            move_line.product_id,
            move_line.company_id,
            move_line.picking_id,
            move_line.product_uom_id,
            move_line.product_qty,
            move_line.product_uom_qty,
            move_line.qty_done,
            move_line.package_id,
            move_line.package_level_id,
            move_line.lot_id,
            move_line.lot_name,
            move_line.result_package_id,
            move_line.date,
            move_line.owner_id,
            move_line.location_id,
            move_line.state,
            move_line.reference,
            move_line.create_uid AS creation_date,
            move_line.create_date,
            move_line.workorder_id,
            move_line.production_id,
            move_line.lot_produced_qty,
            move_line.done_move,
            move_line.location_processed,
            spt.code as picking_type_code,
            spt.name as operation_type,
            sp.date_done as date_done,
            cat.id as categ_id,
            sp.partner_id as partner_id,
            sp.scheduled_date as scheduled_date,
            stock_move.inventory_id as inventory_id,
            extract(epoch from avg(date_trunc('day',sp.date_done)-date_trunc('day',sp.scheduled_date)))/(24*60*60)::decimal(16,2) as delay,
            extract(epoch from avg(date_trunc('day',sp.date_done)-date_trunc('day',sp.date)))/(24*60*60)::decimal(16,2) as cycle_time
        """

        for field in fields.values():
            select_ += field

        from_ = """
                stock_move_line move_line
                LEFT JOIN stock_move ON stock_move.id = move_line.move_id
                LEFT JOIN stock_picking sp ON sp.id = move_line.picking_id
                LEFT JOIN stock_picking_type spt ON stock_move.picking_type_id = spt.id
                INNER JOIN product_product p ON stock_move.product_id = p.id
                INNER JOIN product_template t ON p.product_tmpl_id = t.id
                INNER JOIN product_category cat ON t.categ_id = cat.id
                %s
        """ % from_clause

        groupby_ = """
            move_line.id,
            spt.name,
            sp.date_done,
            cat.id,
            stock_move.inventory_id,
            sp.partner_id,
            sp.scheduled_date,
            spt.code
             %s
        """ % (groupby)

        return '%s (SELECT %s FROM %s WHERE move_line.id IS NOT NULL GROUP BY %s)' % (with_, select_, from_, groupby_)

    def init(self):
        # self._table = sale_report
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute("""CREATE or REPLACE VIEW %s as (%s)""" % (self._table, self._query()))


class StockMoveReportProforma(models.AbstractModel):
    _name = 'report.stock.report_saleproforma'
    _description = 'Proforma Report'

    def _get_report_values(self, docids, data=None):
        docs = self.env['sale.order'].browse(docids)
        return {
            'doc_ids': docs.ids,
            'doc_model': 'sale.order',
            'docs': docs,
            'proforma': True
        }
