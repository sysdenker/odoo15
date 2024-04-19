# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import datetime, date, timedelta


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    dnk_time_perpiece = fields.Float('- Time per piece', compute="dnk_compute_time", store=True)
    dnk_time_allpieces = fields.Float('- Time for all pieces', compute="dnk_compute_time", store=True)
    dnk_reason_diff_cost = fields.Many2one('dnk.reason.difference.cost', '- Reason Cost Variation', ondelete='cascade')
    dnk_diff_cost_prc = fields.Float('- Porcentaje', digits=(3, 2), help='In Manufacturing Orders, Percentage Allowed')
    dnk_to_consume = fields.Float(digits="Account", string="- Average Cost")
    dnk_price = fields.Float(digits="Account", string="- Mo Cost")

    def dnk_compute_time(self):
        for sml in self:

            sml.dnk_time_perpiece = 0
            time_lc = 0
            time_att = 0
            # para cada Labour cost, voy sumando tiempo
            for lc in sml.product_id.product_tmpl_id.dnk_lc_ids:
                time_lc += lc.dnk_product_labour_minutes_qty
            # Luego le sumo los tiempos de los attributos
            for value in sml.product_id.product_template_attribute_value_ids:
                time_att += value.product_attribute_value_id.dnk_product_labour_minutes_qty

            sml.dnk_time_perpiece = time_lc + time_att
            sml.dnk_time_allpieces = sml.product_qty * sml.dnk_time_perpiece


class StockMove(models.Model):
    _inherit = "stock.move"


    dnk_default_code = fields.Char('- Aging Code', help="Se utiliza como código de respaldo para seguimiento de máximos y mínimos", related="product_id.dnk_default_code")
