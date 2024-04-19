# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools, _, SUPERUSER_ID
from odoo.exceptions import UserError, AccessError, ValidationError

class DnkPDevCategoryPrice(models.Model):
    _name = "dnk.pdev.category.price"
    _description = "Category Price"
    _rec_name = 'name'
    _order = "sequence, name, id"

    name = fields.Char(string='- Name', required=True, translate=True)
    dnk_description = fields.Text(string=' - Description', translate=True)
    sequence = fields.Integer(string='- Sequence', default=1, help="Orden de las etapas.")
    fold = fields.Boolean(
        '- Mostrado en Kanban', help='La etapa está plegada cuando no hay registros en la etapa para mostrar.')


    dnk_price = fields.Integer(string=' - Price', copy=True)
    dnk_extra_price = fields.Integer(string=' - Extra Price', copy=True)
    dnk_product_category_id = fields.Many2one('product.category', string='- Product Category')
    active = fields.Boolean(string='- Activo', default=True)



class DnkProductDevLine(models.Model):
    _name = "dnk.crm.product.dev.line"
    _inherit = ['mail.thread']
    _rec_name = 'name'
    _description = "Product Development Line"
    _inherit = ['mail.thread', 'mail.activity.mixin', 'utm.mixin']

    dnk_pd_id = fields.Many2one('dnk.crm.product.dev', string='- Product Development', default=lambda self: self._default_pd_id(), ondelete='cascade', tracking=True, auto_join=True)
    dnk_stage_id = fields.Many2one('dnk.crm.pd.stage', string='- Stage', related="dnk_pd_id.dnk_stage_id")
    active = fields.Boolean(string='- Activo', related="dnk_pd_id.active")
    dnk_categ_type = fields.Char(string='- Category Type', related="dnk_pd_id.dnk_categ_type")

    name = fields.Char(string='- Name', index=True, default=lambda self: self._change_new_product(), copy=True)
    dnk_price = fields.Float(string='- Price',  help="Precio del Producto", copy=True)
    dnk_extra_price = fields.Float(string='- Extra Price',  help="Precio adicional al Producto", copy=True)
    dnk_price_detail = fields.Text(string='- Price Detail',  help="Detalle de Precios", copy=True)
    dnk_embroidery = fields.Char(string='- Embroidery', help="Detalles del Bordado", copy=True)
    dnk_ps_price_required = fields.Boolean(string='- Price Required?', help="¿Se requiere asignar precio?", copy=True)
    dnk_ps_required = fields.Boolean(string='- Product Sample Required?',  help="¿Se requiere muestra física?", copy=True)
    dnk_ps_date = fields.Boolean(string='- Sample Date',  help="Sample Delivery Date", copy=True)
    dnk_ps_qty = fields.Float(string='- Product Sample Qty',  help="Cantidad de Muestras", copy=True)
    dnk_ps_qty_desc = fields.Char(string='- Sample Qty Desc',  help="Descripción de la cantidad de Muestras", copy=True)
    dnk_ps_delivery_date = fields.Date(string='- Sample Delivery Date',  help="Fecha de Entrega de la Muestra", copy=True)
    dnk_ps_tracking_ref = fields.Char(string='- Tracking Reference',  help="Tracking Reference", copy=True)
    dnk_pd_type_id = fields.Many2one('dnk.crm.pd.type', string='- Type', ondelete='cascade', tracking=True)
    dnk_new_dev = fields.Boolean(string='- New Product Dev?', help="New Product Development")
    dnk_color_approval = fields.Selection([('arrastre', 'Arrastre'), ('standar', 'Estándar')], string='- Color Approval')
    dnk_purchase_price = fields.Char(string='- Purchase Price', help ="Purchase Price", copy=True)



    dnk_attribute_ids = fields.Many2many('dnk.pdev.attribute.value', 'dnk_pdev_attributes_rel','attribute_id', 'pdev_line_id',  string='Atributes', copy=True)




    dnk_product_id = fields.Many2one('product.product', string='- Product Variant', ondelete='cascade', tracking=True)
    dnk_product_tmpl_id = fields.Many2one('product.template', string='- Product', related="dnk_product_id.product_tmpl_id", store=True)
    currency_id = fields.Many2one('res.currency', string='- Currency', related="dnk_pd_id.currency_id")
    dnk_new_product = fields.Boolean(string='- New Product?', related="dnk_pd_id.dnk_new_product")
    dnk_family_id = fields.Many2one('product.category', string='- Family', related='dnk_pd_id.dnk_family_id', tracking=True)
    #La subfamilia ya no va a estar ligada a la DP, al menos no en las líneas.
    dnk_subfamily_id = fields.Many2one('product.category', string='- Subfamily', copy=True, tracking=True)

    ## Campos especificos que se utilizan aun variando la subfamilia
    dnk_new_default_code = fields.Char(string='- New Reference Code', copy=True)
    dnk_folder_url = fields.Char(string='- Folder URL', copy=True)
    dnk_uom_id = fields.Many2one(
        comodel_name='uom.uom',
        domain="[('id', 'in', ('14', '10'))]",
        string='- Bag UoM')
    dnk_description = fields.Text(string='- Additional Specifications', help="Additional Specifications", copy=True)

    dnk_length = fields.Float(string='- Length',  help="Length", copy=True)
    dnk_width  = fields.Float(string='- Width',  help="Width", copy=True)
    dnk_thickness  = fields.Float(string='- Thickness',  help="Thickness", copy=True)

    dnk_pricelist_dom = fields.Many2many(comodel_name='product.pricelist', string='- Product Pricelist Domain', compute="get_product_pricelist_dom", store=False, readonly=True)
    dnk_pricelist_id = fields.Many2one(
        comodel_name='product.pricelist',
        domain="[('id', 'in', dnk_pricelist_dom)]",
        string='- Pricelist', ondelete='cascade')
    dnk_pricelist_item_id = fields.Many2one(
        comodel_name='product.pricelist.item',
        domain="[('pricelist_id', '=', dnk_pricelist_id), ('applied_on', '=', '2_product_category'), ('compute_price', '=', 'percentage')]",
        string='- Pricelist Item', ondelete='cascade')

    dnk_attach_dom = fields.Many2many(comodel_name='product.attribute.value', string='- Attachments Domain', compute="get_attach_dom", store=False, readonly=True)
    dnk_attach_ids = fields.Many2many(
        comodel_name='product.attribute.value',
        relation='dnk_pdev_attach_rel',
        domain="[('id', 'in', dnk_attach_dom)]",
        string='- Attachments')



    dnk_size_dom = fields.Many2many(comodel_name='product.attribute.value', string='- Size Domain', compute="get_size_dom", store=False, readonly=True)
    dnk_size_id = fields.Many2one(
        comodel_name='product.attribute.value',
        domain="[('id', 'in', dnk_size_dom)]",
        string='- Size')

    dnk_fabric_color_dom = fields.Many2many(comodel_name='product.attribute.value', string='- Fabric Color Domain', compute="get_fabric_color_dom", store=False, readonly=True)
    # dnk_fabric_color_ids = fields.Many2many(
    #    comodel_name='product.attribute.value',
    #    relation='dnk_pdev_fabric_color_rel',
    #    domain="[('id', 'in', dnk_fabric_color_dom)]",
    #    string='- Fabric Color')
    dnk_fabric_color_id = fields.Many2one(
        comodel_name='product.attribute.value',
        domain="[('id', 'in', dnk_fabric_color_dom)]",
        string='- Fabric Color')

    dnk_fabric_type_dom = fields.Many2many(comodel_name='product.attribute.value', string='- Fabric Type Domain', compute="get_fabric_type_dom", store=False, readonly=True)
    dnk_fabric_type_id = fields.Many2one(
        comodel_name='product.attribute.value',
        domain="[('id', 'in', dnk_fabric_type_dom)]",
        string='- Fabric Type')

    dnk_fabric_cutting_dom = fields.Many2many(comodel_name='product.attribute.value', string='-  Fabric Cutting Domain', compute="get_fabric_cutting_dom", store=False, readonly=True)
    dnk_fabric_cutting_id = fields.Many2one(
        comodel_name='product.attribute.value',
        domain="[('id', 'in', dnk_fabric_cutting_dom)]",
        string='- Fabric Cutting')

    dnk_additional_atts_dom = fields.Many2many(comodel_name='product.attribute.value', string='- Additional Attributes Domain', compute="get_additional_atts_dom", store=False, readonly=True)
    dnk_additional_atts_ids = fields.Many2many(
        comodel_name='product.attribute.value',
        relation='dnk_pdev_add_atts_rel',
        domain="[('id', 'in', dnk_additional_atts_dom)]",
        string='- Additional Attributes')
    dnk_att_count = fields.Integer(string='- Additional Attribute Counter', compute="dnk_attribute_counter")

    ## Variables de BATA ##

    ##  Variables de Bolsa
    ## ###################

    dnk_bag_style_dom = fields.Many2many(comodel_name='product.attribute.value', string='- Bag Style Domain', compute="get_bag_style_dom", store=False, readonly=True)
    dnk_bag_style_id = fields.Many2one(
        comodel_name='product.attribute.value',
        domain="[('id', 'in', dnk_bag_style_dom)]",
        string='- Bag Style')

    dnk_bag_type_dom = fields.Many2many(comodel_name='product.attribute.value', string='- Bag Type Domain', compute="get_bag_type_dom", store=False, readonly=True)
    dnk_bag_type_id = fields.Many2one(
        comodel_name='product.attribute.value',
        domain="[('id', 'in', dnk_bag_type_dom)]",
        string='- Bag Type')

    dnk_bag_sealing_dom = fields.Many2many(comodel_name='product.attribute.value', string='- Bag Sealing Domain', compute="get_bag_sealing_dom", store=False, readonly=True)
    dnk_bag_sealing_id = fields.Many2one(
        comodel_name='product.attribute.value',
        domain="[('id', 'in', dnk_bag_sealed_dom)]",
        string='- Sealing Type')

    dnk_bag_use = fields.Char(string='- Bag Use', copy=True)
    dnk_bag_use = fields.Char(string='- Bag Use', copy=True)
    dnk_bag_specs = fields.Text(string='Bag Specs', help="Especificaciones de la bolsa")

    dnk_bag_design_dom = fields.Many2many(comodel_name='product.attribute.value', string='- Bag Design Domain', compute="get_bag_design_dom", store=False, readonly=True)
    dnk_bag_design_id = fields.Many2one(
        comodel_name='product.attribute.value',
        domain="[('id', 'in', dnk_bag_design_dom)]",
        string='- Bag Design')

    dnk_bag_gusset = fields.Float(string='- Bag Gusset',  help="Bag Gusset", copy=True)
    dnk_bag_gauge = fields.Float(string='- Bag Gauge',  help="Bag Gauge", copy=True)
    dnk_bag_temp = fields.Float(string='- Bag Temperature',  help="Temperature to Use in the bag", copy=True)

    ## Variables de Empaque de Diseño

    dnk_cavities_qty = fields.Integer(string='- Cavities Qty',  help="cavities", copy=True)

    dnk_mat_property_dom = fields.Many2many(comodel_name='product.attribute.value', string='- Material Property Domain', compute="get_mat_property_dom", store=False, readonly=True)
    dnk_mat_property_id = fields.Many2one(
        comodel_name='product.attribute.value',
        domain="[('id', 'in', dnk_mat_property_dom)]",
        string='- Material Property')

    dnk_material_dom = fields.Many2many(comodel_name='product.attribute.value', string='- Material Domain', compute="get_material_dom", store=False, readonly=True)
    dnk_material_id = fields.Many2one(
        comodel_name='product.attribute.value',
        domain="[('id', 'in', dnk_material_dom)]",
        string='- Material')

    ## Variables Overal
    dnk_garmet_identifier = fields.Char(string='- Identifier', copy=True)

    ##  Variables de Equipos
    dnk_brand = fields.Char(string='- Brand', copy=True)
    dnk_supplier = fields.Char(string='- Supplier', copy=True)
    dnk_reference = fields.Char(string='- Reference Source', copy=True)

    ##  Variables de Servicios
    dnk_serv_type_dom = fields.Many2many(comodel_name='product.attribute.value', string='- Type  Domain', compute="get_serv_type_dom", store=False, readonly=True)
    dnk_serv_type_id = fields.Many2one(
        comodel_name='product.attribute.value',
        domain="[('id', 'in', dnk_serv_type_dom)]",
        string='- Type')


    @api.depends('dnk_new_product')
    def get_product_pricelist_dom(self):
        for a in self:
            a.dnk_pricelist_dom = []
            att_val_dom = [
                ('compute_price', '=', 'percentage'),
                ('applied_on', '=', '2_product_category'),
                ('currency_id', '=', 3),
                ('percent_price', '>', 0)]
            a.dnk_pricelist_dom = self.env['product.pricelist.item'].search(att_val_dom).pricelist_id

    @api.depends('dnk_new_product')
    def get_attach_dom(self):
        for a in self:
            att_val_dom = ['|',
                ('dnk_subfamily_id', '=', a.dnk_subfamily_id.id),
                ('dnk_subfamily_id', '=', False),
                ('dnk_pdev_field', '=', 'dnk_attach_ids'),
                ('dnk_family_id', '=', a.dnk_family_id.id),
                ('active', '=', True)]
            a.dnk_attach_dom = self.env['dnk.pdev.attribute.value'].search(att_val_dom).dnk_pdav_ids


    @api.depends('dnk_additional_atts_ids')
    def dnk_attribute_counter(self):
        for rec in self:
            rec.dnk_att_count = len(rec.dnk_additional_atts_ids)


    def bttn_get_model(self):
        view_id = self.env.ref('dnk_crm_product_dev.dnk_view_get_model').id
        context = self._context.copy()
        context['dnk_partner_id'] = self.dnk_get_labour_cost()
        context['dnk_pdev_id'] = self.dnk_get_indirect_cost_ids()

        return {
            'name': 'Get Model Sequence',
            'view_type': 'form',
            'view_mode': 'form',
            'views': [(view_id, 'form')],
            'res_model': 'dnk.product.model',
            'view_id': view_id,
            'type': 'ir.actions.act_window',
            'target': 'new',
            'context': context,
        }

    @api.depends('dnk_new_product')
    def get_size_dom(self):
        for a in self:
            att_val_dom = ['|',
                ('dnk_subfamily_id', '=', a.dnk_subfamily_id.id),
                ('dnk_subfamily_id', '=', False),
                ('dnk_pdev_field', '=', 'dnk_size_id'),
                ('dnk_family_id', '=', a.dnk_family_id.id),
                ('active', '=', True)]
            a.dnk_size_dom = self.env['dnk.pdev.attribute.value'].search(att_val_dom).dnk_pdav_ids

    @api.depends('dnk_new_product')
    def get_fabric_color_dom(self):
        for a in self:
            att_val_dom = ['|',
                ('dnk_subfamily_id', '=', a.dnk_subfamily_id.id),
                ('dnk_subfamily_id', '=', False),
                ('dnk_pdev_field', '=', 'dnk_fabric_color_id'),
                ('dnk_family_id', '=', a.dnk_family_id.id),
                ('active', '=', True)]
            a.dnk_fabric_color_dom = self.env['dnk.pdev.attribute.value'].search(att_val_dom).dnk_pdav_ids

    @api.depends('dnk_new_product')
    def get_fabric_type_dom(self):
        for a in self:
            att_val_dom = ['|',
                ('dnk_subfamily_id', '=', a.dnk_subfamily_id.id),
                ('dnk_subfamily_id', '=', False),
                ('dnk_pdev_field', '=', 'dnk_fabric_type_id'),
                ('dnk_family_id', '=', a.dnk_family_id.id),
                ('active', '=', True)]
            a.dnk_fabric_type_dom = self.env['dnk.pdev.attribute.value'].search(att_val_dom).dnk_pdav_ids

    @api.depends('dnk_new_product')
    def get_fabric_cutting_dom(self):
        for a in self:
            att_val_dom = ['|',
                ('dnk_subfamily_id', '=', a.dnk_subfamily_id.id),
                ('dnk_subfamily_id', '=', False),
                ('dnk_pdev_field', '=', 'dnk_fabric_cutting_id'),
                ('dnk_family_id', '=', a.dnk_family_id.id),
                ('active', '=', True)]
            a.dnk_fabric_cutting_dom = self.env['dnk.pdev.attribute.value'].search(att_val_dom).dnk_pdav_ids

    @api.depends('dnk_new_product')
    def get_additional_atts_dom(self):
        for a in self:
            # categ_dom = [('name', 'ilike', 'PDev'), ('name', 'ilike', 'Especial')]
            # categ_ids = self.env['product.attribute.category'].search(categ_dom).ids
            att_val_dom = ['|',
                ('dnk_subfamily_id', '=', a.dnk_subfamily_id.id),
                ('dnk_subfamily_id', '=', False),
                ('dnk_pdev_field', '=', 'dnk_additional_atts_ids'),
                ('dnk_family_id', '=', a.dnk_family_id.id),
                ('active', '=', True)]
            a.dnk_additional_atts_dom = self.env['dnk.pdev.attribute.value'].search(att_val_dom).dnk_pdav_ids

    @api.depends('dnk_new_product')
    def get_bag_style_dom(self):
        for a in self:
            att_val_dom = ['|',
                ('dnk_subfamily_id', '=', a.dnk_subfamily_id.id),
                ('dnk_subfamily_id', '=', False),
                ('dnk_pdev_field', '=', 'dnk_bag_style_id'),
                ('dnk_family_id', '=', a.dnk_family_id.id),
                ('active', '=', True)]
            a.dnk_bag_style_dom = self.env['dnk.pdev.attribute.value'].search(att_val_dom).dnk_pdav_ids

    @api.depends('dnk_new_product')
    def get_bag_sealing_dom(self):
        for a in self:
            att_val_dom = ['|',
                ('dnk_subfamily_id', '=', a.dnk_subfamily_id.id),
                ('dnk_subfamily_id', '=', False),
                ('dnk_pdev_field', '=', 'dnk_bag_sealing_id'),
                ('dnk_family_id', '=', a.dnk_family_id.id),
                ('active', '=', True)]
            a.dnk_bag_sealing_dom = self.env['dnk.pdev.attribute.value'].search(att_val_dom).dnk_pdav_ids

    @api.depends('dnk_new_product')
    def get_bag_type_dom(self):
        for a in self:
            att_val_dom = ['|',
                ('dnk_subfamily_id', '=', a.dnk_subfamily_id.id),
                ('dnk_subfamily_id', '=', False),
                ('dnk_pdev_field', '=', 'dnk_bag_type_id'),
                ('dnk_family_id', '=', a.dnk_family_id.id),
                ('active', '=', True)]
            a.dnk_bag_type_dom = self.env['dnk.pdev.attribute.value'].search(att_val_dom).dnk_pdav_ids

    @api.depends('dnk_new_product')
    def get_bag_design_dom(self):
        for a in self:
            att_val_dom = ['|',
                ('dnk_subfamily_id', '=', a.dnk_subfamily_id.id),
                ('dnk_subfamily_id', '=', False),
                ('dnk_pdev_field', '=', 'dnk_bag_design_id'),
                ('dnk_family_id', '=', a.dnk_family_id.id),
                ('active', '=', True)]
            a.dnk_bag_design_dom = self.env['dnk.pdev.attribute.value'].search(att_val_dom).dnk_pdav_ids

    @api.depends('dnk_new_product')
    def get_serv_type_dom(self):
        for a in self:
            att_val_dom = ['|',
                ('dnk_subfamily_id', '=', a.dnk_subfamily_id.id),
                ('dnk_subfamily_id', '=', False),
                ('dnk_pdev_field', '=', 'dnk_serv_type_id'),
                ('dnk_family_id', '=', a.dnk_family_id.id),
                ('active', '=', True)]
            a.dnk_serv_type_dom = self.env['dnk.pdev.attribute.value'].search(att_val_dom).dnk_pdav_ids

    @api.depends('dnk_new_product')
    def get_material_dom(self):
        for a in self:
            att_val_dom = ['|',
                ('dnk_subfamily_id', '=', a.dnk_subfamily_id.id),
                ('dnk_subfamily_id', '=', False),
                ('dnk_pdev_field', '=', 'dnk_material_id'),
                ('dnk_family_id', '=', a.dnk_family_id.id),
                ('active', '=', True)]
            a.dnk_material_dom = self.env['dnk.pdev.attribute.value'].search(att_val_dom).dnk_pdav_ids


    def _default_pd_id(self):
        if self._context and self._context.get('active_model', False) == 'dnk.crm.product.dev':
            return self._context.get('active_id', False)
        return False

    @api.depends('dnk_new_default_code', 'dnk_new_product', 'dnk_product_id', 'dnk_extra_price','dnk_pricelist_item_id')
    @api.onchange('dnk_new_default_code', 'dnk_new_product', 'dnk_product_id', 'dnk_extra_price','dnk_pricelist_item_id')
    def _change_new_product(self):
        for record in self:
            record.dnk_price = 0
            if record.dnk_new_product:
                record._product_cat_price()
                record.name = ""
                attrs = []
                if record.dnk_categ_type == 'bata':
                    record.dnk_new_default_code = "ESM-0#$%"
                    if record.dnk_fabric_color_id: # Color 1
                        attrs.append(record.dnk_fabric_color_id.name)
                        record.dnk_new_default_code = record.dnk_new_default_code.replace("0",(record.dnk_fabric_color_id.dnk_reference_code_part or "0"), 1)
                        record.dnk_price = record.dnk_price + record.dnk_fabric_color_id.dnk_att_price
                        record.dnk_price_detail = record.dnk_price_detail + record.dnk_fabric_color_id.name + "($" + str(record.dnk_fabric_color_id.dnk_att_price) + ")</br>"
                    if record.dnk_fabric_type_id: # Tela 2
                        attrs.append(record.dnk_fabric_type_id.name)
                        record.dnk_new_default_code = record.dnk_new_default_code.replace("#",(record.dnk_fabric_type_id.dnk_reference_code_part or "#"), 1)
                        record.dnk_price = record.dnk_price + record.dnk_fabric_type_id.dnk_att_price
                        record.dnk_price_detail = record.dnk_price_detail + record.dnk_fabric_type_id.name + "($" + str(record.dnk_fabric_type_id.dnk_att_price) + ")</br>"
                    if record.dnk_fabric_cutting_id: # Corte 3
                        attrs.append(record.dnk_fabric_cutting_id.name)
                        record.dnk_new_default_code = record.dnk_new_default_code.replace("$",(record.dnk_fabric_cutting_id.dnk_reference_code_part or "$"), 1)
                        record.dnk_price = record.dnk_price + record.dnk_fabric_cutting_id.dnk_att_price
                        record.dnk_price_detail = record.dnk_price_detail + record.dnk_fabric_cutting_id.name + "($" + str(record.dnk_fabric_cutting_id.dnk_att_price) + ")</br>"
                    if record.dnk_size_id: # Talla 4
                        attrs.append(record.dnk_size_id.name)
                        record.dnk_new_default_code = record.dnk_new_default_code.replace("%",(record.dnk_size_id.dnk_reference_code_part or "%"), 1)
                        record.dnk_price = record.dnk_price + record.dnk_size_id.dnk_att_price
                        record.dnk_price_detail = record.dnk_price_detail + record.dnk_size_id.name + "($" + str(record.dnk_size_id.dnk_att_price) + ")</br>"
                    if record.dnk_additional_atts_ids:
                        for att in record.dnk_additional_atts_ids:
                            attrs.append(att.name)
                            record.dnk_price = record.dnk_price + att.dnk_att_price
                            record.dnk_price_detail = record.dnk_price_detail + att.name + "($" + str(att.dnk_att_price) + ")</br>"
                    if record.dnk_pricelist_item_id and record.dnk_pricelist_item_id.percent_price > 0:
                        record.dnk_price = record.dnk_price * (100-record.dnk_pricelist_item_id.percent_price/100)
                        record.dnk_price_detail = record.dnk_price_detail + "Discount: (%" + str(record.dnk_pricelist_item_id.percent_price) + ")</br>"
                    if attrs:
                        record.name = "[" + record.dnk_new_default_code + "] Bata " + ' '.join(map(str,attrs))
            else :
                record.name = record.dnk_product_id.name or 'New'

    @api.depends('dnk_fabric_cutting_id', 'dnk_fabric_color_id', 'dnk_size_id', 'dnk_additional_atts_ids')
    @api.onchange('dnk_fabric_cutting_id', 'dnk_fabric_color_id', 'dnk_size_id', 'dnk_additional_atts_ids')
    def _change_attributes(self):
        for rec in self:
            rec._change_new_product()


    def _product_cat_price(self):
        for rec in self:
            rec.dnk_price_detail = ""
            if rec.dnk_subfamily_id :
                b_price = self.env['dnk.pdev.category.price'].search([
                    ('active', '=', True),
                    ('dnk_product_category_id', '=', rec.dnk_subfamily_id.id)])
                for p in b_price:
                    rec.dnk_price = rec.dnk_price + p.dnk_price
                    rec.dnk_price_detail = rec.dnk_price_detail + p.name + "($" + str(p.dnk_price) + ")</br>"
            rec.dnk_price = rec.dnk_price + rec.dnk_extra_price
            rec.dnk_price_detail = rec.dnk_price_detail + "Extra ($" + str(rec.dnk_extra_price) + ")</br>"


    @api.depends('dnk_fabric_type_id')
    @api.onchange('dnk_fabric_type_id')
    def _change_fabric_type_field(self):
        for rec in self:
            if rec.dnk_fabric_type_id :
                if "PA" in rec.dnk_fabric_type_id.name.upper():
                    rec.dnk_subfamily_id = 781
                if "AD" in rec.dnk_fabric_type_id.name.upper():
                    rec.dnk_subfamily_id = 778
                if "L1" in rec.dnk_fabric_type_id.name.upper():
                    rec.dnk_subfamily_id = 779
                if "LR" in rec.dnk_fabric_type_id.name.upper():
                    rec.dnk_subfamily_id = 780
            rec.dnk_fabric_color_id = rec.dnk_fabric_cutting_id = rec.dnk_size_id = False
            rec.get_fabric_color_dom()
            rec.get_size_dom()
            rec.get_fabric_cutting_dom()
            rec.get_additional_atts_dom()
            rec._change_new_product()

    @api.depends('dnk_pricelist_id')
    @api.onchange('dnk_pricelist_id')
    def _change_pricelist(self):
        for rec in self:
            rec.dnk_pricelist_item_id = False
            rec.get_product_pricelist_dom()
            rec._change_new_product()

    def name_get(self):
        result = []
        for pd_line in self.sudo():
            name = '%s' % (pd_line.name)
            result.append((pd_line.id, name))
        return result

    def create(self, values):
        if 'dnk_new_default_code' in values or 'dnk_product_id' in values:
            self._change_new_product(self)
        result = super(DnkProductDevLine, self).create(values)
        return result

    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
        if operator in ('ilike', 'like', '=', '=like', '=ilike'):
            args = expression.AND([
                args or [],
                ['|', ('dnk_pd_id.name', operator, name), ('name', operator, name)]
            ])
            return self._search(args, limit=limit, access_rights_uid=name_get_uid)
        return super(SaleOrderLine, self)._name_search(name, args=args, operator=operator, limit=limit, name_get_uid=name_get_uid)
