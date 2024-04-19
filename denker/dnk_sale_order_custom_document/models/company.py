# -*- coding: utf-8 -*-
import base64
import os

from odoo import api, fields, models, tools, _


class Company(models.Model):
    _inherit = "res.company"

    primary_background_color = fields.Char(default='#00447a')
    secondary_background_color = fields.Char(default='#387b3d')
