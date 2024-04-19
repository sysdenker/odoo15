# -*- coding: utf-8 -*-
from odoo.addons import decimal_precision as dp
from odoo import models, fields, api


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    def _prepare_invoice_line(self, **optional_values):
        def _name_get(d):
            name = d.get('name', '')
            code = self._context.get('display_default_code', True) and d.get('default_code', False) or False
            if code:
                name = '[%s] %s' % (code, name)
            return (d['id'], name)

        product = self.product_id
        variable_attributes = product.attribute_line_ids.filtered(lambda l: l.attribute_id.dnk_show_in_invoice is True).mapped('attribute_id')
        variant = product.product_template_attribute_value_ids._variant_name(variable_attributes)

        # Generar el nombre de la línea de factura sólo con los atributos configurados a mostrar
        name = variant and "%s (%s)" % (product.name, variant) or product.name
        mydict = {
            'id': product.id,
            'name': name,
            'default_code': product.default_code,
        }
        res = super(SaleOrderLine, self)._prepare_invoice_line(**optional_values)
        # Reemplazar el nombre con todos las atributos, a nombre corto con los atributos configuradas
        res['name'] = _name_get(mydict)[1]

        return res
