# -*- coding: utf-8 -*-
import base64
import os

from odoo import fields, models


class BaseDocumentLayout(models.TransientModel):
    _inherit = "base.document.layout"

    dnk_logo2 = fields.Binary(related='company_id.dnk_logo2', readonly=False)
