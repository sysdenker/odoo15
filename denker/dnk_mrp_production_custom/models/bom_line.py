# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import timedelta
from odoo import api, fields, models, _
import string

class MrpBomLine(models.Model):
    _inherit = 'mrp.bom.line'

    @api.model
    def updat_operation_id(self):
        for rec in self:
            for op_id in rec.bom_id.operation_ids:
                if "CORTE" in op_id.name.upper():
                    rec.operation_id = op_id.id
