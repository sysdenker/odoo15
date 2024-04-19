# -*- coding: utf-8 -*-
from odoo import api, models


class MrpWorkorder(models.Model):
    _inherit = 'mrp.workorder'

    @api.depends('state')
    def _update_mpr_production_workorder_state(self):
        # self.production_id.dnk_workorder_ready = workorder.name
        # self.production_id.dnk_workorder_ready_state = workorder.state
        for workorder in self:
            workorder.production_id.dnk_workorder_ready = workorder.name
            workorder.production_id.dnk_workorder_ready_state = workorder.state
            # Podría ser con write
            # workorder.write({'dnk_workorder_ready': workorder.name, 'dnk_workorder_ready_state': workorder.state})
