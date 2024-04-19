# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from datetime import datetime, timedelta
from collections import namedtuple, OrderedDict, defaultdict
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT, float_compare, float_is_zero, float_round
import logging
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class SaleOrderLine(models.Model):
    _inherit = "sale.order"

    @api.onchange('warehouse_id', 'state')
    def _update_sale_line_commitment_date(self):
        for line in self.order_line:
            line._update_commitment_date()


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    dnk_expected_date = fields.Date(
        string='- Expected Date', store=True,
        # readonly=True,
        # tracking=True,
        help="Date by which the products are sure to be delivered. This is "
        "a date that you can promise to the customer, based on the "
        "Product Lead Times.")
    dnk_commitment_date = fields.Date(
        string='- Commitment Date', store=True,
        # readonly=True,
        # tracking=True,
        help="This is a date that you can promise to the customer")
    dnk_delivery_days = fields.Integer(
        string='- Delivery Days', store=True,
        # tracking=True,
        readonly=True,
        help="")
    dnk_confirmation_count = fields.Integer(string='- Confirmation Count', store=True, readonly=True, default=0)
    dnk_has_moves = fields.Boolean(string='- Has Stock Moves', compute='dnk_has_stock_moves', readonly=True, help="")

    @api.model
    def dnk_has_stock_moves(self):
        for rec in self:
            rec.dnk_has_moves = False
            if rec.move_ids:
                rec.dnk_has_moves = True

    @api.model
    def write(self, vals):
        res = super(SaleOrderLine, self).write(vals)
        for rec in self:
            if "dnk_expected_date" in vals:
                if "dnk_commitment_date" in vals:
                    if vals['dnk_expected_date'] != vals['dnk_commitment_date']:
                        rec.dnk_confirmation_count += 1
                        vals['dnk_commitment_date'] = rec.dnk_confirmation_count
                elif vals['dnk_expected_date'] != rec.dnk_commitment_date:
                    rec.dnk_confirmation_count += 1
                    vals['dnk_commitment_date'] = rec.dnk_confirmation_count
                if vals['dnk_expected_date'] != rec.dnk_commitment_date:
                    if rec.dnk_confirmation_count <= 1:
                        rec.dnk_commitment_date = vals['dnk_expected_date']
                        vals['dnk_commitment_date'] = vals['dnk_expected_date']
                    rec._update_expected_date(vals['dnk_expected_date'])
        return res

    # @api.onchange('dnk_expected_date')
    def _update_expected_date(self, dnk_expected_date=False):
        for line in self:
            if line.move_ids:
                for move in line.move_ids:
                    if move.state != 'done' and dnk_expected_date:
                        move.date = dnk_expected_date + " 06:00:00"
                # line.dnk_confirmation_count += 1
                if line.dnk_expected_date:
                    line.dnk_delivery_days = (line.dnk_expected_date - fields.date.today()).days

    @api.onchange('product_id', 'warehouse_id', 'customer_lead')
    def _update_commitment_date(self):
        procurements = []
        for line in self:
            if line.state != 'draft' or line.product_id.type not in ('consu', 'product'):
                continue

            values = line._prepare_procurement_values()
            product_qty = line.product_uom_qty

            line_uom = line.product_uom
            quant_uom = line.product_id.uom_id
            product_qty, procurement_uom = line_uom._adjust_uom_quantities(product_qty, quant_uom)
            procurements.append(self.env['procurement.group'].Procurement(
                line.product_id, product_qty, procurement_uom,
                line.order_id.partner_shipping_id.property_stock_customer,
                line.product_id.name, line.order_id.name, line.order_id.company_id, values))

        date_expected = False
        if procurements:
            move_ids = self.env['procurement.group'].run2(procurements)
            reg = self.order_id.company_id.id
            for move_id in move_ids:
                for move in move_id[reg]:
                    location_dest_id = self.env['stock.location'].browse(move['location_dest_id'])
                    if location_dest_id and location_dest_id.usage == 'customer':
                        date_expected = move['date_deadline']
                        # move.sale_line_id.dnk_expected_date = move['date_expected']

        if date_expected:
            # date_expected = datetime.strptime(date_expected[:10], '%Y-%m-%d')
            self.dnk_expected_date = date_expected
            self.dnk_commitment_date = date_expected
            self.dnk_confirmation_count = 0
            self.dnk_delivery_days = (date_expected.date() - fields.date.today()).days


class ProcurementGroup(models.Model):
    _inherit = 'procurement.group'

    def run2(self, procurements):
        """ Method used in a procurement case. The purpose is to supply the
        product passed as argument in the location also given as an argument.
        In order to be able to find a suitable location that provide the product
        it will search among stock.rule.
        """
        actions_to_run = defaultdict(list)
        errors = []
        for procurement in procurements:
            procurement.values.setdefault('company_id', self.env.company)
            procurement.values.setdefault('priority', '1')
            procurement.values.setdefault('date_planned', fields.Datetime.now())
            if (
                procurement.product_id.type not in ('consu', 'product') or float_is_zero(procurement.product_qty, precision_rounding=procurement.product_uom.rounding)
            ):
                continue
            rule = self._get_rule(procurement.product_id, procurement.location_id, procurement.values)
            if not rule:
                errors.append(
                    _('No rule has been found to replenish "%s" in "%s".\nVerify the routes configuration on the product.') %
                    (procurement.product_id.display_name, procurement.location_id.display_name))
            else:
                action = 'pull' if rule.action == 'pull_push' else rule.action
                actions_to_run[action].append((procurement, rule))

        if errors:
            raise UserError('\n'.join(errors))

        moves_values = []
        for action, procurements in actions_to_run.items():
            if hasattr(self.env['stock.rule'], '_run_%s2' % action):
                try:
                    moves_values.append(getattr(self.env['stock.rule'], '_run_%s2' % action)(procurements))
                except UserError as e:
                    errors.append(e.name)
            else:
                _logger.error("The method _run_%s doesn't exist on the procurement rules" % action)
                action = 'pull'
                moves_values.append(getattr(self.env['stock.rule'], '_run_%s2' % action)(procurements))

        if errors:
            raise UserError('\n'.join(errors))
        return moves_values


class StockRule(models.Model):
    """ A rule describe what a procurement should do; produce, buy, move, ... """
    _inherit = 'stock.rule'

    def _run_push2(self, move):
        """ Apply a push rule on a move.
        If the rule is 'no step added' it will modify the destination location
        on the move.
        If the rule is 'manual operation' it will generate a new move in order
        to complete the section define by the rule.
        Care this function is not call by method run. It is called explicitely
        in stock_move.py inside the method _push_apply
        """
        new_date = fields.Datetime.to_string(move.date_deadline + relativedelta(days=self.delay))
        if self.auto == 'transparent':
            new_move_vals = {
                'date': new_date,
                'date_deadline': new_date,
                'location_dest_id': self.location_id.id}
        else:
            new_move_vals = self._push_prepare_move_copy_values(move, new_date)
            # new_move = move.sudo().copy(new_move_vals)
            # move.write({'move_dest_ids': [(4, new_move.id)]})
            # new_move._action_confirm()
            return new_move_vals

    @api.model
    def _run_pull2(self, procurements):
        moves_values_by_company = defaultdict(list)
        mtso_products_by_locations = defaultdict(list)

        # To handle the `mts_else_mto` procure method, we do a preliminary loop to
        # isolate the products we would need to read the forecasted quantity,
        # in order to to batch the read. We also make a sanitary check on the
        # `location_src_id` field.
        for procurement, rule in procurements:
            if not rule.location_src_id:
                msg = _('No source location defined on stock rule: %s!') % (rule.name, )
                raise UserError(msg)

            if rule.procure_method == 'mts_else_mto':
                mtso_products_by_locations[rule.location_src_id].append(procurement.product_id.id)

        # Get the forecasted quantity for the `mts_else_mto` procurement.
        forecasted_qties_by_loc = {}
        for location, product_ids in mtso_products_by_locations.items():
            products = self.env['product.product'].browse(product_ids).with_context(location=location.id)
            forecasted_qties_by_loc[location] = {product.id: product.free_qty for product in products}

        # Prepare the move values, adapt the `procure_method` if needed.
        for procurement, rule in procurements:
            procure_method = rule.procure_method
            if rule.procure_method == 'mts_else_mto':
                mtso_products_by_locations[rule.location_src_id].append(procurement.product_id.id)

        # Get the forecasted quantity for the `mts_else_mto` procurement.
        forecasted_qties_by_loc = {}
        for location, product_ids in mtso_products_by_locations.items():
            products = self.env['product.product'].browse(product_ids).with_context(location=location.id)
            forecasted_qties_by_loc[location] = {product.id: product.free_qty for product in products}

        # Prepare the move values, adapt the `procure_method` if needed.
        for procurement, rule in procurements:
            procure_method = rule.procure_method
            if rule.procure_method == 'mts_else_mto':
                qty_needed = procurement.product_uom._compute_quantity(procurement.product_qty, procurement.product_id.uom_id)
                qty_available = forecasted_qties_by_loc[rule.location_src_id][procurement.product_id.id]
                if float_compare(qty_needed, qty_available, precision_rounding=procurement.product_id.uom_id.rounding) <= 0:
                    procure_method = 'make_to_stock'
                    forecasted_qties_by_loc[rule.location_src_id][procurement.product_id.id] -= qty_needed
                else:
                    procure_method = 'make_to_order'

            move_values = rule._get_stock_move_values(*procurement)
            move_values['procure_method'] = procure_method
            moves_values_by_company[procurement.company_id.id].append(move_values)

        return moves_values_by_company
