# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import Warning, UserError, ValidationError
import math

# Custom Exception
# from odoo.addons.custom_exception.models.exception import UserError


class MrpProduction(models.Model):
    """ Manufacturing Orders """
    _inherit = 'mrp.production'

    def _workorders_create(self, bom, bom_data):
        """
        :param bom: in case of recursive boms: we could create work orders for child
                    BoMs
        """
        workorders = self.env['mrp.workorder']

        # Initial qty producing
        quantity = max(self.product_qty - sum(self.move_finished_ids.filtered(lambda move: move.product_id == self.product_id).mapped('quantity_done')), 0)
        quantity = self.product_id.uom_id._compute_quantity(quantity, self.product_uom_id)
        if self.product_id.tracking == 'serial':
            quantity = 1.0
        # New Line JCT
        else:
            quantity = 0

        for operation in bom.routing_id.operation_ids:
            workorder_vals = self._prepare_workorder_vals(
                operation, workorders, quantity)
            workorder = workorders.create(workorder_vals)
            if workorders:
                workorders[-1].next_work_order_id = workorder.id
                workorders[-1]._start_nextworkorder()
            workorders += workorder

            moves_raw = self.move_raw_ids.filtered(lambda move: move.operation_id == operation and move.bom_line_id.bom_id.routing_id == bom.routing_id)
            moves_finished = self.move_finished_ids.filtered(lambda move: move.operation_id == operation)

            # - Raw moves from a BoM where a routing was set but no operation was precised should
            #   be consumed at the last workorder of the linked routing.
            # - Raw moves from a BoM where no rounting was set should be consumed at the last
            #   workorder of the main routing.
            if len(workorders) == len(bom.routing_id.operation_ids):
                moves_raw |= self.move_raw_ids.filtered(lambda move: not move.operation_id and move.bom_line_id.bom_id.routing_id == bom.routing_id)
                moves_raw |= self.move_raw_ids.filtered(lambda move: not move.workorder_id and not move.bom_line_id.bom_id.routing_id)

                moves_finished |= self.move_finished_ids.filtered(lambda move: move.product_id != self.product_id and not move.operation_id)

            moves_raw.mapped('move_line_ids').write({'workorder_id': workorder.id})
            (moves_finished | moves_raw).write({'workorder_id': workorder.id})

            workorder._generate_wo_lines()
        return workorders


class MrpWorkorder(models.Model):
    _name = 'mrp.workorder'
    _inherit = ['mrp.workorder', 'barcodes.barcode_events_mixin']

    dnk_product_barcode = fields.Char(string="- Product Barcode", related='product_id.barcode')

    def on_barcode_scanned(self, barcode):
        sound_file = '/dnk_mrp_workorder_barcode/static/sounds/beep-5.wav'

        if self.dnk_product_barcode == barcode:
            if self.qty_producing > self.qty_remaining - 1:
                # raise UserError(_("La cantidad producida ha excedido la cantidad de la Orden de Trabajo."), None, None, sound_file)
                raise ValidationError(_("La cantidad producida ha excedido la cantidad de la Orden de Trabajo."))

            self.qty_producing += 1
            # Reproduce sonido, pero hace log de error, por eso queda comentado
            # sound_file = '/dnk_mrp_workorder_barcode/static/sounds/smb3_coin.wav'
            # raise CustomSound(sound_file)
            return
        else:
            # Normal o con sonido
            # raise Warning(_("Error: This product does not belong to the current work order!"))
            # raise UserError(_("Este producto no pertenece a la actual Orden de Trabajo!"), None, None, sound_file)
            raise ValidationError(_("Este producto no pertenece a la actual Orden de Trabajo!"))
