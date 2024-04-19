# -*- coding: utf-8 -*-
import base64
import os

from odoo import fields, models


class BaseDocumentLayout(models.TransientModel):
    _inherit = "base.document.layout"

    primary_background_color = fields.Char(related='company_id.primary_background_color', readonly=False)
    secondary_background_color = fields.Char(related='company_id.secondary_background_color', readonly=False)
