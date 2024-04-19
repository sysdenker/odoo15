# -*- encoding: utf-8 -*-
from odoo import api, fields, http, models, _


class Website(models.Model):
    _inherit = 'website'

    def sale_product_domain(self):
        return [("sale_ok", "=", True), ('dnk_website_ids', 'in', ([self.id]))] + self.get_current_website().website_domain()
    #    return [("sale_ok", "=", True)] + self.get_current_website().website_domain()


    # def _get_product_oum():
    #    Uoms = request.env['uom.oum'].sudo()
    #    return Uoms.get_website_product_uom()
