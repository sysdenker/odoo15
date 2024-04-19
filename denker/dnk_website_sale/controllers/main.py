# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import json
import logging

from odoo import fields, http, SUPERUSER_ID, tools, _
from odoo.http import request

from odoo.addons.website.controllers.backend import WebsiteBackend

_logger = logging.getLogger(__name__)


class DnkWebsiteSale(WebsiteBackend):

    # def values_postprocess(self, order, mode, values, errors, error_msg):
    #    print("mi values postprocess")
    #    res1, res2, res3 = super(DnkWebsiteSale, self).values_postprocess(order, mode, values, errors, error_msg)

    #    return new_values, errors, error_msg


    def _get_mandatory_billing_fields(self):
        # print("_get_mandatory_billing_fields", request.website.company_id.id)
        if request.website.company_id.id == 1:
            return ["name", "email", "street", "city", "country_id", "l10n_mx_edi_colony", "zip"]
        else:
            return ["name", "email", "street", "city", "country_id", "zip"]

    def _get_mandatory_shipping_fields(self):
        # print("_get_mandatory_shipping_fields", request.website.company_id.id)
        if request.website.company_id.id == 1:
            return ["name", "street", "city", "country_id", "l10n_mx_edi_colony", "zip"]
        else:
            return ["name", "street", "city", "country_id", "zip"]
