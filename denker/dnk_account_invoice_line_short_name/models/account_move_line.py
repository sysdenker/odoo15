# -*- coding: utf-8 -*-
from odoo.addons import decimal_precision as dp
from odoo import models, fields, api


class AccountInvoiceLine(models.Model):
    _inherit = "account.move.line"

    @api.onchange('product_id')
    def _onchange_product_id(self):
        def _name_get(d):
            name = d.get('name', '')
            code = self._context.get('display_default_code', True) and d.get('default_code', False) or False
            if code:
                name = '[%s] %s' % (code, name)
            return (d['id'], name)

        domain = super(AccountInvoiceLine, self)._onchange_product_id()

        part = self.move_id.partner_id
        type = self.move_id.move_type

        if self.product_id:
            if part.lang:
                product = self.product_id.with_context(lang=part.lang)
            else:
                product = self.product_id

            self.name = product.partner_ref

            result = []
            # display only the attributes with multiple possible values on the template
            variable_attributes = product.attribute_line_ids.filtered(lambda l: l.attribute_id.dnk_show_in_invoice is True).mapped('attribute_id')
            variant = product.product_template_attribute_value_ids._variant_name(variable_attributes)

            name = variant and "%s (%s)" % (product.name, variant) or product.name
            mydict = {
                'id': product.id,
                'name': name,
                'default_code': product.default_code,
            }

            if type in ('in_invoice', 'in_refund'):
                if product.description_purchase:
                    self.name += '\n' + product.description_purchase
            else:
                if product.description_sale:
                    self.name = _name_get(mydict)[1]
                    self.name += '\n' + product.description_sale
        return domain
