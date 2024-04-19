# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class MaintenanceRequest(models.Model):
    _inherit = "maintenance.request"

    maintenance_type = fields.Selection(
        selection_add=[("improvement", "Improvement")]
    )

    #maintenance_type = fields.Selection(
    #    [('corrective', 'Corrective'), ('preventive', 'Preventive'), ('improvement', 'Improvement')],
    #    string='Maintenance Type', default="corrective")
