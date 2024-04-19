# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import datetime, date, timedelta
from odoo.exceptions import UserError, ValidationError
import math


class MrpProduction(models.Model):
    _inherit = "mrp.production"

    dnk_time_perpiece = fields.Float('- Time per piece', compute="dnk_compute_time", store=True)
    dnk_time_allpieces = fields.Float('- Time for all pieces', compute="dnk_compute_time", store=True)

    dnk_amount = fields.Float(digits="Account", string="- Production Amount", compute="_dnk_compute_amount")
    dnk_price = fields.Float(digits="Account", string="- Mo Cost", compute="_dnk_compute_amount")
    dnk_to_consume = fields.Float(digits="Account", string="- Average Cost", compute="_dnk_amount_to_consume")
    dnk_validation = fields.Boolean('- Validarion Alert', default=True)
    dnk_reason_diff_cost = fields.Many2one('dnk.reason.difference.cost', '- Reason Cost Variation', ondelete='cascade')
    dnk_diff_cost_prc = fields.Float('- Porcentaje', digits=(3, 2), help='In Manufacturing Orders, Percentage Allowed')
    dnk_restricted = fields.Boolean('- Validation', compute="_dnk_mo_restricted")
    # Modificar la función Mark as done, para que si hay una diferencia en porcentaje de acuerdo a la categoría de producto.
    # Mandar una Alerta
    # So el campo dnk_price es mayor o menos a dnk_to_consume,  es cuando se alerta.1
    # Agregar un campo a categoría de producto. para determinar el porcentaje de diferencia que puede haber entre los 2 campos
    # Al  alertar, preguntar si avanzar así o no. y que muestre en ese Alert el porcentaje.

    def _dnk_mo_restricted(self):
        for rec in self:
            rec.dnk_restricted=False
            if rec.product_id.categ_id.dnk_alow_cost_diff:
                val_allowed = rec.product_id.categ_id.dnk_alow_cost_diff
                if val_allowed > 1 and val_allowed < 100:
                    val_min = rec.dnk_to_consume * (1 - (val_allowed / 100))
                    val_max = rec.dnk_to_consume * (1 + (val_allowed / 100))
                    if rec.dnk_price > val_max:
                        rec.dnk_restricted=True
                        return True
                    else:
                        rec.dnk_restricted=False
                        return False

    def return_percent_val(self, option=False):
        if option == 'post_inventory':
            view_id = self.env.ref('dnk_product_cost.dnk_view_cost_dif_inv_val').id
        else:
            view_id = self.env.ref('dnk_product_cost.dnk_view_cost_dif_val').id
        return {
            'name': ('Manufacturing Order Cost Validation'),
            'view_mode': 'form',
            'res_model': 'dnk.mrp.cost.val',
            'view_id': view_id,
            'type': 'ir.actions.act_window',
            'context': {
                'default_dnk_mo_id': self.id,
                'default_dnk_price': self.dnk_price,
                'default_dnk_to_consume': self.dnk_to_consume,
                'default_dnk_alow_cost_diff': self.product_id.categ_id.dnk_alow_cost_diff,
                'default_dnk_option': option,
                'default_dnk_restricted': self.dnk_restricted,
            },
            'target': 'new',
        }

    def post_inventory(self):
        for rec in self:
            rec.dnk_compute_time()
            if rec.dnk_validation:
                if rec.product_id.categ_id.dnk_alow_cost_diff:
                    val_allowed = rec.product_id.categ_id.dnk_alow_cost_diff
                    if val_allowed > 1 and val_allowed < 100:
                        val_min = rec.dnk_to_consume * (1 - (val_allowed / 100))
                        val_max = rec.dnk_to_consume * (1 + (val_allowed / 100))
                        if rec.dnk_price < val_min or rec.dnk_price > val_max:
                            return self.return_percent_val('post_inventory')
                            self.update_mrp_diff_percent()
                        else:
                            return super(MrpProduction, self).post_inventory()
            else:
                self.update_mrp_diff_percent()
                return super(MrpProduction, self).post_inventory()

    def update_mrp_diff_percent(self):
        for rec in self:
            for finished_id in rec.finished_move_line_ids:
                if not finished_id.dnk_diff_cost_prc:
                    if rec.dnk_to_consume == 0:
                        finished_id.dnk_diff_cost_prc = 0
                    else:
                        finished_id.dnk_diff_cost_prc = rec.dnk_price / rec.dnk_to_consume
                    finished_id.dnk_reason_diff_cost = rec.dnk_reason_diff_cost
                    finished_id.dnk_to_consume = rec.dnk_to_consume
                    finished_id.dnk_price = rec.dnk_price

    def button_mark_done(self):
        for rec in self:
            rec.dnk_compute_time()
            # Primero Validar campo dnk_validation
            if rec.dnk_validation:
                if rec.product_id.categ_id.dnk_alow_cost_diff:
                    val_allowed = rec.product_id.categ_id.dnk_alow_cost_diff
                    if val_allowed > 1 and val_allowed < 100:
                        val_min = rec.dnk_to_consume * (1 - (val_allowed / 100))
                        val_max = rec.dnk_to_consume * (1 + (val_allowed / 100))
                        if rec.dnk_price < val_min or rec.dnk_price > val_max:
                            return self.return_percent_val('mark_done')
                        else:
                            self.update_mrp_diff_percent()
                            return super(MrpProduction, self).button_mark_done()

            else:
                self.update_mrp_diff_percent()
                return super(MrpProduction, self).button_mark_done()
    
    @api.model
    def create(self, values):
        production = super(MrpProduction, self).create(values)
        if production.procurement_group_id:
            mo_origin = self.env['mrp.production'].search([
                ('procurement_group_id', '=', production.procurement_group_id.id), 
                ('id', '!=', production.id)],  order='id desc', limit=1)
            if mo_origin:
                production.x_studio_field_wGB7m = mo_origin.x_studio_field_wGB7m
                production.date_planned_start = mo_origin.date_planned_start
        return production
    

    def write(self, vals):
        res = super(MrpProduction, self).write(vals)
        for rec in self:
            if "x_studio_field_wGB7m" in vals:
                rec.dnk_update_work_center()
        return res
    
    def dnk_update_work_center(self):
        for production in self:
            for move in production.workorder_ids:
                move.workcenter_id = production.x_studio_field_wGB7m

    def _dnk_amount_to_consume(self):
        for production in self:
            amount = 0.0
            price = 0.0
            production.dnk_to_consume = 0
            for move in production.move_raw_ids:
                qty = move.product_uom_qty
                price_uom = move.product_id.uom_id._compute_price(move.product_id.standard_price, move.product_uom)
                amount += price_uom * qty
                production.dnk_to_consume = amount / production.product_qty

    def _dnk_compute_amount(self):
        for production in self:
            amount = 0.0
            price = 0.0
            for move in production.move_raw_ids:
                if move.product_id.type == "product":
                    qty = move.quantity_done
                    price_uom = move.product_id.uom_id._compute_price(move.product_id.standard_price, move.product_uom)
                    # print(move.product_id.name)
                    # print(qty)
                    # print(price_uom)
                    amount += price_uom * qty
            product_qty = 0
            if production.qty_producing == 0:
                product_qty = production.product_qty
            else:
                product_qty = production.qty_producing
            production.dnk_price = amount / product_qty
            production.dnk_amount = amount

    def _compute_amount(self):
        # print("Estoy entrando _compute_amount")
        for production in self:
            # calculate_price = 0.0
            amount = 0.0
            # service_amount = 0.0
            planned_cost = True
            # print("Voy a imprimir los move_raw_ids")
            for move in production.move_raw_ids:
                # print("Move", move, move.quantity_done)
                if move.quantity_done > 0:
                    # print("move.quantity_done > 0,planned_cost = False ")
                    planned_cost = False  # nu au fost facute miscari de stoc

            if planned_cost:
                # print("Si planned_cost entro otra vez a move_raw_ids")
                for move in production.move_raw_ids:
                    # print("Move", move)
                    if move.product_id.type == "product":
                        qty = move.qty_producing  # + move.product_qty * move.product_id.scrap
                        amount += move.price_unit * qty
                product_qty = production.qty_producing

            else:
                # print("planned_cost es Falso, por lo tanto entro al Else")
                for move in production.move_raw_ids:
                    # print("Tipo:", move.product_id.type)
                    if move.product_id.type == "product":
                        qty = move.quantity_done
                        amount += abs(move.price_unit) * qty
                        # print("QTY: ", qty)
                        # print("Amount: ", amount)
                product_qty = 0.0
                # print("move_finished_ids:", production.move_finished_ids)
                for move in production.move_finished_ids:
                    product_qty += move.quantity_done
                if product_qty == 0.0:
                    product_qty = production.qty_producing
                # print("product_qty:", product_qty)

            # adaugare manopera la costul estimat

            # if production.routing_id:
            #    for operation in production.routing_id.operation_ids:
            #        time_cycle = operation.get_time_cycle(quantity=product_qty, product=production.product_id)

            #       cycle_number = math.ceil(product_qty / operation.workcenter_id.capacity)
            #        duration_expected = (operation.workcenter_id.time_start
            #            + operation.workcenter_id.time_stop
            #            + cycle_number * time_cycle * 100.0 / operation.workcenter_id.time_efficiency)

            #        amount += (duration_expected / 60) * operation.workcenter_id.costs_hour

            # amount += production.service_amount
            calculate_price = amount / product_qty
            production.dnk_price = calculate_price
            production.dnk_amount = amount

    @api.depends('product_id', 'product_qty')
    def dnk_compute_time(self):
        for mo in self:

            mo.dnk_time_perpiece = 0
            time_lc = 0
            time_att = 0
            # para cada Labour cost, voy sumando tiempo
            for lc in mo.product_id.product_tmpl_id.dnk_lc_ids:
                time_lc += lc.dnk_product_labour_minutes_qty
            # Luego le sumo los tiempos de los attributos
            for value in mo.product_id.product_template_attribute_value_ids:
                time_att += value.product_attribute_value_id.dnk_product_labour_minutes_qty

            mo.dnk_time_perpiece = time_lc + time_att
            mo.dnk_time_allpieces = mo.product_qty * mo.dnk_time_perpiece
