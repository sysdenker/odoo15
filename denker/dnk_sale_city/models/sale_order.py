# -*- coding: utf-8 -*-
from odoo import models, fields, api


class dnk_sale_city(models.Model):
    _inherit = "sale.order"

    def _default_sale_city(self):
        if 'active_model' in self._context and self._context['active_model'] == 'crm.lead':
            sale_city_id = self.env['crm.lead'].search([('id', '=', self._context['active_id'])]).dnk_sale_city_id
            return sale_city_id
        return False

    dnk_sale_city_id = fields.Many2one('dnk.sale.city', '- City', default=lambda self: self._default_sale_city())


class dnk_sale_order_line(models.Model):
    _inherit = "sale.order.line"

    dnk_sale_city_id = fields.Many2one('dnk.sale.city', related='order_id.dnk_sale_city_id')
