# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools
from PIL import Image
import base64
from datetime import datetime, timedelta


class AccountMove(models.Model):
    _inherit = "account.move"

    dnk_proof_of_delivery = fields.Image(string="- Proof Of Delivery", max_width=1024, max_height=1024)
    dnk_proof_of_delivery_tmp = fields.Image(string="- Proof Of Delivery Temp", related="dnk_proof_of_delivery", max_width=512, max_height=512)
    dnk_proof_file_type = fields.Char('- Type', store=False)
    dnk_proof_of_delivery_datetime = fields.Datetime('- Delivery Proof Date', copy=False)
    dnk_proof_days = fields.Integer('- Proof Days', copy=False)

    @api.onchange('dnk_proof_of_delivery')
    def onchnage_dnk_proof_of_delivery(self):
        self.dnk_proof_of_delivery_datetime = fields.Datetime.now()
        if self.create_date and self.dnk_proof_of_delivery_datetime:
            self.dnk_proof_days = (self.dnk_proof_of_delivery_datetime - self.create_date).days
        if not self.dnk_proof_of_delivery:
            self.dnk_proof_of_delivery_datetime = False
            self.dnk_proof_days = False

        # Queda pendiente la migración de esta parte, hasta que se termine de migrar el módulo [stock_picking_invoice_link]

        # for picking_id in self.picking_ids:
        #    values = {
        #        'dnk_proof_of_delivery_datetime': self.dnk_proof_of_delivery_datetime,
        #        'dnk_proof_days': self.dnk_proof_days,
        #    }
        #    picking_id.write(values)

    def write(self, vals):
        if 'dnk_proof_of_delivery' in vals:
            if vals['dnk_proof_of_delivery']:
                datetime = fields.Datetime.now()
                proof_days = (fields.Datetime.now() - self.create_date).days
            else:
                datetime = False
                proof_days = False
            vals_append = {
                'dnk_proof_of_delivery_datetime': datetime,
                'dnk_proof_days': proof_days,
            }
            vals.update(vals_append)
        return super(AccountMove, self).write(vals)
