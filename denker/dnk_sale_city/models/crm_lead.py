# -*- coding: utf-8 -*-

from odoo import models, fields, api


class CRMLead(models.Model):
    _inherit = "crm.lead"

    def _default_sale_city(self, user_id=False):
        # Desde la vista de formulario
        if not user_id and 'uid' in self._context:
            user = self._context['uid']
        else:
            if user_id:
                user = user_id.id
            else:
                return False
            cities = self.env['res.users'].search([('id', '=', user)]).dnk_sale_city_ids
            for city in cities:
                if city:
                    return city.id
        return False

    # @api.onchange('dnk_sale_city_id')
    # def _onchange_sale_city(self):
    #   self._onchange_partner_id_values()

    @api.onchange('user_id')
    def _onchange_user_id(self):
        # res = super(CRMLead, self)._onchange_user_id()
        self.dnk_sale_city_id = self._default_sale_city(self.user_id)
        # return res

    dnk_sale_city_id = fields.Many2one('dnk.sale.city', string='- City', default=lambda self: self._default_sale_city())
