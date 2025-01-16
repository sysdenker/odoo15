# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools, _, SUPERUSER_ID
from odoo.exceptions import UserError, AccessError, ValidationError

class DnkPDeveAtributeValues(models.Model):
    _name = "dnk.pdev.attribute.value"
    _description = "Product Development Attribute Value"
    _rec_name = 'name'
    _order = "sequence, name, id"

    name = fields.Char(string='- Name', required=True, translate=True)
    dnk_description = fields.Text(string=' - Description', translate=True)
    sequence = fields.Integer(string='- Sequence', default=1, help="Orden de los atributos.")
    fold = fields.Boolean(string='- Mostrado en Kanban', help='La etapa está plegada cuando no hay registros en la etapa para mostrar.')
    active = fields.Boolean(string='- Activo', default=True)
    dnk_family_id = fields.Many2one('product.category', string='- Family')
    dnk_subfamily_id = fields.Many2one('product.category', string='- Subfamily' )
    dnk_base_price = fields.Float(string='- Price',  help="Base Price", copy=True)
    dnk_pda_id = fields.Many2one('product.attribute', string='- Atributo')
    dnk_pda_category_id = fields.Many2one('product.attribute.category', string='- Category')
    dnk_pdav_dom = fields.Many2many(string='- Domain Attribute Values', comodel_name='product.attribute.value', store=False, compute="dnk_pdav_domain")
    dnk_pdav_ids = fields.Many2many(
        comodel_name='product.attribute.value',
        relation="dnk_pdev_attribute_val_rel",
        domain="[('id', 'in', dnk_pdav_dom)]",
        string='- Attribute Values')
    dnk_pdev_code = fields.Char(string='- Code', translate=True, help="Código que se agregará a la descripción")
    # dnk_pdev_field = fields.Char(string='- Field Name', translate=True, help="Nombre del campo para filtrar las opciones que se muestran en los campos de selección")
    dnk_pdev_field = fields.Selection(
        [
            ('dnk_attach_ids', '- Attachments'),
            ('dnk_size_id', '- Size'),
            ('dnk_fabric_color_id', '- Fabric Color'),
            ('dnk_fabric_type_id', '- Fabric Type'),
            ('dnk_fabric_cutting_id', '- Fabric Cutting'),
            ('dnk_additional_atts_ids', '- Additional Attributes'),
            ('dnk_bag_style_id', '- Bag Style'),
            ('dnk_bag_sealing_id', '- Sealing Type'),
            ('dnk_bag_type_id', '- Bag Type'),
            ('dnk_bag_design_id', '- Bag Design'),
            ('dnk_serv_type_id', '- Type'),
            ('dnk_material_id', '- Material'),
        ], '- Field Name',
        help='Nombre del campo en donde se mostrarán los atributos seleccionados', required="1")
    dnk_pdev_priority = fields.Integer(string='- Priority', default=1, help="Prioridad, aun no sé si lo necesitaré")

    @api.depends('dnk_pda_id')
    def dnk_pdav_domain(self):
        for a in self:
            domain = [('attribute_id', 'in', [a.dnk_pda_id.id])]
            a.dnk_pdav_dom = self.env['product.attribute.value'].search(domain)


    @api.depends('dnk_family_id', 'dnk_subfamily_id', 'dnk_pda_id')
    @api.onchange('dnk_family_id', 'dnk_subfamily_id', 'dnk_pda_id')
    def _get_name(self):
        for record in self:
            record.name = ""
            if record.dnk_family_id:
                record.name = ""
                record.name = record.dnk_family_id.name + " - "
            if record.dnk_subfamily_id:
                record.name = ""
                record.name = record.dnk_subfamily_id.name + " - "
            if record.dnk_pda_id:
                record.name = record.name + record.dnk_pda_id.name
