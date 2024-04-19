# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import datetime, date, timedelta


class StockMoveLine(models.Model):
    _inherit = "sale.order.line"

    dnk_time_perpiece = fields.Float('- Time per piece', compute="dnk_compute_time", store=True)
    dnk_time_allpieces = fields.Float('- Time for all pieces', compute="dnk_compute_time", store=True)

    def dnk_compute_time(self):
        for sol in self:

            sol.dnk_time_perpiece = 0
            time_lc = 0
            time_att = 0
            # para cada Labour cost, voy sumando tiempo
            for lc in sol.product_id.product_tmpl_id.dnk_lc_ids:
                time_lc += lc.dnk_product_labour_minutes_qty
            # Luego le sumo los tiempos de los attributos
            for value in sol.product_id.product_template_attribute_value_ids:
                time_att += value.product_attribute_value_id.dnk_product_labour_minutes_qty

            sol.dnk_time_perpiece = time_lc + time_att
            sol.dnk_time_allpieces = sol.product_uom_qty * sol.dnk_time_perpiece
