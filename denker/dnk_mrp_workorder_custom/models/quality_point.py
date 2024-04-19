# -*- coding: utf-8 -*-
from datetime import timedelta
from odoo import api, fields, models, _


class QualityPoint(models.Model):
    _inherit = "quality.point"

    # No lleva es standar dnk, ya que se está redefiniendo un campo existente, donde originalmente sanitize_attributes=True
    note = fields.Html(string='Note', sanitize=False, sanitize_tags=False, sanitize_attributes=False)
