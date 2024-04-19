
# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class ResPartner(models.Model):
    _inherit = 'res.partner'

    slide_channel_ids = fields.Many2many(
        'slide.channel', 'slide_channel_partner', 'partner_id', 'channel_id', copy=False,
        string='eLearning Courses', groups="website_slides.group_website_slides_officer")
