# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import timedelta
from odoo import api, fields, models, _
# from odoo.exceptions import Warning, ValidationError
import string

# Custom Exception
# from odoo.addons.custom_exception.models.exception import UserError

"""
 * Get color (black/white) depending on bgColor so it would be clearly seen.
 * @param bgColor
 * @returns {string}
 """


# 25 Abr 2024 Cambios para planeación
class DnkMRPPManufacturingStatus(models.Model):
    _name = "dnk.mrp.manufacturing.status"
    _description = "MRP Manufacturing Status"
    _rec_name = 'name'
    _order = "sequence, name, id"

    name = fields.Char(string='- Name', required=True, translate=True)
    description = fields.Text(string=' - Description', translate=True)
    sequence = fields.Integer(string='- Sequence', default=1, help="Order")
    fold = fields.Boolean(
        '- Mostrado en Kanban', help='La etapa está plegada cuando no hay registros en la etapa para mostrar.')
    active = fields.Boolean(string='- Active', default=True)


class DnkMRPManufacturingDelays(models.Model):
    _name = "dnk.mrp.manufacturing.delays"
    _description = "MRP Manufacturing Delays"
    _rec_name = 'name'
    _order = "sequence, name, id"

    name = fields.Char(string='- Name', required=True, translate=True)
    description = fields.Text(string=' - Description', translate=True)
    sequence = fields.Integer(string='- Sequence', default=1, help="Order")
    fold = fields.Boolean(
        '- Mostrado en Kanban', help='La etapa está plegada cuando no hay registros en la etapa para mostrar.')
    active = fields.Boolean(string='- Active', default=True)

    

def getColorByBgColor(bgColor):
    if not bgColor:
        return '#000000'
    if bgColor[0] == '#':
        bgColor = bgColor[1:]
    return '#000000' if (int(bgColor, 16) > 8388607) else '#FFFFFF'


class MrpProduction(models.Model):
    _inherit = 'mrp.production'


    @api.depends('product_id')
    def _dnk_compute_attribute_color(self):
        for production in self:
            production.dnk_attribute_color = "#313131"
            for attribute_value in production.product_id.product_template_attribute_value_ids:
                if attribute_value.html_color is not False:
                    production.dnk_attribute_color = attribute_value.html_color
                    production.dnk_attribute_color_name = attribute_value.name
                    if all(c in string.hexdigits for c in attribute_value.html_color[1:]):
                        production.dnk_attribute_inverse_color = getColorByBgColor(attribute_value.html_color)
                    break

    # Sólo agregar al campo original: tracking=True
    date_planned_start = fields.Datetime(
        'Planned Date', copy=False, default=fields.Datetime.now,
        help="Date at which you plan to start the production.",
        index=True, required=True, store=True, tracking=True)

    dnk_subfamily = fields.Many2one('product.category', string='- Subfamily', related='product_id.product_tmpl_id.categ_id', store=True)
    dnk_family = fields.Many2one('product.category', string='- Family', related='dnk_subfamily.parent_id', store=True)
    dnk_color = fields.Many2one('product.category', string='- Color', related='dnk_family.parent_id', store=True)
    dnk_product_default_code = fields.Char(string='- Product Internal Reference', related='product_id.default_code', store=True)

    dnk_workorder_ready = fields.Char(
        '- Work Order', compute='_compute_workorder_ready',
        readonly=True, store=True)
    dnk_workorder_ready_state = fields.Selection([
        ('pending', 'Pending'),
        ('ready', 'Ready'),
        ('progress', 'In Progress'),
        ('done', 'Finished'),
        ('cancel', 'Cancelled')], string='- WO Status',
        compute='_compute_workorder_ready',
        readonly=True, store=True)

    dnk_attribute_color = fields.Char(string='- Attribute Color', store=True, default="#313131",
                                      compute="_dnk_compute_attribute_color", readonly=True,
                                      help="HTML Color Attribute of the Product.")
    dnk_attribute_inverse_color = fields.Char(
        string='- Inverse Attribute Color', store=True, default="#313131",
        compute="_dnk_compute_attribute_color", readonly=True,
        help="HTML Color Attribute of the Product.")
    dnk_attribute_color_name = fields.Char(
        string='- Attribute Color Name', store=True,
        compute="_dnk_compute_attribute_color", readonly=True,
        help="Name Color Attribute of the Product.")

    dnk_sale_order_id =  fields.Many2one('sale.order', string='- Sale Order', store=True, compute="dnk_compute_sale_order_id", default=False)

    # 25 Abr 2024  Campos nuevos para planeación
    
    dnk_fabric_cutting_date = fields.Date(
        '- Fabric Cutting Date', copy=False, 
        help="Date at which you plan to start the Cutting.",
        index=True, required=False, store=True, tracking=True)
    dnk_cutting_notes = fields.Html('- Cutting Notes', help="Cutting Notes")
    dnk_note = fields.Html('- Note', help="Manufacturing Order Notes")
    dnk_prod_status_id = fields.Many2one('dnk.mrp.manufacturing.status', default=False, string='- Cutting Status', help="Fabric Cutting Status")
    dnk_maufacturing_delays_id = fields.Many2one('dnk.mrp.manufacturing.delays', default=False, string='- Manuifacturing Delays', help="Manufacturin Delays")


    @api.depends('origin')
    def dnk_compute_sale_order_id(self):
        for rec in self:
            if rec.origin:
                index = rec.origin.find("-SO")
                so = list(rec.origin.split(","))
                so = list(rec.origin.split(" "))
                if len(so) == 1:
                    sale_order_id = self.env['sale.order'].search([('name','=',rec.origin), ('company_id', '=', rec.company_id.id)], limit=1)
                    rec.dnk_sale_order_id = sale_order_id
                    return sale_order_id.id
        rec.dnk_sale_order_id = False
        return False




    @api.depends('product_id', 'product_id.default_code')
    def _get_product_default_code(self):
        for production in self:
            production.dnk_product_default_code = production.product_id.default_code

    @api.depends('workorder_ids.state')
    # Revisar si esta función es nativa de Odoo
    # 17/Ene/2024 Ya no está el campo, por lo tanto tampoco la función, la renombro
    # para asociarla a los campos que creo en este módulo.
    def _compute_workorder_ready(self):
        data = self.env['mrp.workorder'].read_group([
            ('production_id', 'in', self.ids),
            ('state', '=', 'done')], ['production_id'], ['production_id'])
        count_data = dict((item['production_id'][0], item['production_id_count']) for item in data)
        for production in self:
            # production.workorder_done_count = count_data.get(production.id, 0)
            for workorder in production.workorder_ids:
                if workorder.state in ('ready', 'progress'):
                    production.write({'dnk_workorder_ready': workorder.name, 'dnk_workorder_ready_state': workorder.state})
                    break
