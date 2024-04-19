# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class Survey(models.Model):
    _inherit = "survey.survey"
    # El campo state en 15 dejó  ya no aplica
    state = fields.Selection(selection_add=[('permanent', 'Permanent')], ondelete={'permanent': 'cascade'})
