# -*- encoding: utf-8 -*-
from odoo import api, fields, http, models,exceptions, _
from odoo.exceptions import ValidationError


class IrAttachment(models.Model):
    _inherit = "ir.attachment"
