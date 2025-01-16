# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError, AccessError
import string


# * Get color (black/white) depending on bgColor so it would be clearly seen.
# * @param bgColor
# * @returns {string}
def getColorByBgColor(bgColor):
    if not bgColor:
        return '#000000'
    if bgColor[0] == '#':
        bgColor = bgColor[1:]
    return '#000000' if (int(bgColor, 16) > 8388607) else '#FFFFFF'


class MrpProduction(models.Model):
    _inherit = "mrp.production"

    # Esta función no se usa en este código puython, si no en la etiquetas a imprimir
    def get_last_digits(self, string, chars_qty):
        res = ''
        if string:
            iIndex = 0
            for char in string[::-1]:
                if char.isdigit() and iIndex < chars_qty:
                    res += char
                else:
                    break
                iIndex += 1
        return res[::-1].zfill(chars_qty)

    @api.depends('product_id')
    def _dnk_compute_attribute_color(self):
        print("_dnk_compute_attribute_color")
        for production in self:
            production.dnk_attribute_color = "#313131"
            for attribute_value in production.product_id.product_template_attribute_value_ids:
                if attribute_value.html_color is not False:
                    production.dnk_attribute_color = attribute_value.html_color
                    production.dnk_attribute_color_name = attribute_value.name
                    if all(c in string.hexdigits for c in attribute_value.html_color[1:]):
                        production.dnk_attribute_inverse_color = getColorByBgColor(attribute_value.html_color)
                if attribute_value.attribute_id.name.upper() == 'TALLA' or attribute_value.attribute_id.name.upper() == 'SIZE':
                    if "TALLA" in attribute_value.name.upper():
                        production.dnk_attribute_size = attribute_value.name[6:]
                    else:
                        production.dnk_attribute_size = attribute_value.name

    def _dnk_compute_costura_workorder(self):
        for production in self:
            production.dnk_costura_workorder_id = 0
            for workorder_id in production.workorder_ids:
                # _logger.warning('name: ' + workorder_id.name.upper())
                if 'COSTURA' in workorder_id.name.upper():
                    production.dnk_costura_workorder_id = workorder_id.id


    dnk_attribute_size = fields.Char(
        string='- Size', store=True,
        compute="_dnk_compute_attribute_color", readonly=True,
        help="Size Attribute of the Product.")

    dnk_costura_workorder_id = fields.Integer(
        string='- Costura WorkOrder',  # store=True,
        compute="_dnk_compute_costura_workorder",
        help="Id de la Order de Trabajo de Costura.")
