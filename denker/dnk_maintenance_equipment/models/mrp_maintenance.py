# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from dateutil.relativedelta import relativedelta
from datetime import timedelta, datetime
from collections import defaultdict

from odoo import api, fields, models, _
from odoo.addons.resource.models.resource import Intervals


class MaintenanceEquipment(models.Model):
    _inherit = "maintenance.equipment"

    dnk_owner_id = fields.Many2one(
        'dnk.asset.owner', string='Asset Owner', copy=True)
    dnk_is_service = fields.Boolean('- Is Service?', default=False,
        help="Campo para utilizar equipos como servicios y ver si podemos controlar periodicidad de pagos.")
