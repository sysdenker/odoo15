
# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class ResourceCalendar(models.Model):
    _inherit = 'resource.calendar'

    dnk_tiempo_comida = fields.Char(string=_('- Tiempo de Comida'), size=32, default='Sesenta Minutos')
