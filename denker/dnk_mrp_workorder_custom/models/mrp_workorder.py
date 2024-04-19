# -*- coding: utf-8 -*-
from datetime import timedelta
from odoo import api, fields, models, _
import string


def complementaryColor(hex):
    """ Returns complementary RGB color
    Example:
    >>>complementaryColor('FFFFFF')
    '000000'
    """
    if hex[0] == '#':
        hex = hex[1:]
    rgb = (hex[0:2], hex[2:4], hex[4:6])
    comp = ['{:02x}'.format(255 - int(a, 16)) for a in rgb]
    return '#' + "" . join(comp).upper()


def getColorByBgColor(bgColor):
    """
     * Get color (black/white) depending on bgColor so it would be clearly seen.
     * @param bgColor
     * @returns {string}
    """
    if not bgColor:
        return '#000000'
    if bgColor[0] == '#':
        bgColor = bgColor[1:]
    return '#000000' if (int(bgColor, 16) > 8388607) else '#FFFFFF'


class MrpWorkorder(models.Model):
    _inherit = 'mrp.workorder'

    @api.depends('product_id')
    def _dnk_compute_attribute_color(self):
        for workorder in self:
            workorder.dnk_attribute_color = "#313131"
            for attribute_value in workorder.product_id.product_template_attribute_value_ids:
                if attribute_value.html_color is not False:
                    workorder.dnk_attribute_color = attribute_value.html_color
                    workorder.dnk_attribute_color_name = attribute_value.name
                    if all(c in string.hexdigits for c in attribute_value.html_color[1:]):
                        workorder.dnk_attribute_inverse_color = getColorByBgColor(attribute_value.html_color)
                    break

    dnk_attribute_color = fields.Char(
        string='- Color', store=True, default="#313131",
        compute="_dnk_compute_attribute_color", readonly=True,
        help="HTML Color Attribute of the Product.")
    dnk_attribute_inverse_color = fields.Char(
        string='- Inverse Color', store=True, default="#313131",
        compute="_dnk_compute_attribute_color", readonly=True,
        help="HTML Color Attribute of the Product.")
    dnk_attribute_color_name = fields.Char(
        string='- Color Name', store=True,
        compute="_dnk_compute_attribute_color", readonly=True,
        help="Name Color Attribute of the Product.")
    # No lleva es standar dnk, ya que se está redefiniendo un campo existente
    note = fields.Html(
        string='Note',
        related='current_quality_check_id.note',
        sanitize=False, sanitize_tags=False, sanitize_attributes=False)
    dnk_product_default_code = fields.Char('Internal Reference', related='product_id.default_code', store=True)
