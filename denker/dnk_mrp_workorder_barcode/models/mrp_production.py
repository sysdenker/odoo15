# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import Warning, ValidationError
import math

# Custom Exception
# from odoo.addons.custom_exception.models.exception import UserError

class MrpProduction(models.Model):
    _name = 'mrp.production'
    _inherit = ['mrp.production', 'barcodes.barcode_events_mixin']


    # 24 Abr 2024 Se agrega función de barcode por scanner
    dnk_product_barcode = fields.Char(string="- Product Barcode", related='product_id.barcode')

    def on_barcode_scanned(self, _barcode_scanned):
        print("on_barcode_scanned")
        sound_file = '/dnk_mrp_workorder_barcode/static/sounds/beep-5.wav'

        if self.dnk_product_barcode == _barcode_scanned:
            if self.qty_producing > self.product_qty - 1:
                raise ValidationError(_("La cantidad producida ha excedido la cantidad de la Orden de Trabajo."))
                # raise UserError(_("La cantidad producida ha excedido la cantidad de la Orden de Trabajo."), None, None, sound_file)

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
            # raise UserError(_("Este producto no pertenece a la actual Orden de Trabajo!"))
