# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools, _


class DnkManufacturingOp(models.Model):
    _name = 'dnk.manufacturing.op'
    _description = 'Manufacturing Operations'
    _rec_name = 'name'
    _order = 'name, sequence'

    name = fields.Char('- Name', index=True, required=True, translate=True)
    sequence = fields.Integer('- Sequence')
    description = fields.Text(
        '- Description', translate=True)
    dnk_equipment_id = fields.Many2one('maintenance.equipment.category', '- Equipment Category', ondelete='cascade')
    dnk_time = fields.Float(string="- Seconds", digits='Product Price', groups="base.group_user")
    dnk_family_ids = fields.Many2many('product.category', inverse_name="id", string="- Family")
    dnk_help =  fields.Char(string="- Help")
    # dnk_family_id = fields.One2many(
    #    comodel_name='product.category',
    #    inverse_name='manufacturing_op_id',
    #    string='- Volume Cost Line')


class DnkProductOp(models.Model):
    _name = 'dnk.product.op'
    _description = 'Product Operations'
    _rec_name = 'name'
    _order = 'name, sequence'

    name = fields.Char('- Name', index=True, required=True, default=lambda self: self._change_equipment_category())
    sequence = fields.Integer('- Sequence')
    dnk_manufacturing_op_dom = fields.Many2many(comodel_name='dnk.manufacturing.op', string='- Manufacturin Op Domain', compute="get_maufacturig_op_dom", store=False, readonly=True)
    dnk_manufacturing_op_id = fields.Many2one(
        comodel_name='dnk.manufacturing.op',
        domain="[('id', 'in', dnk_manufacturing_op_dom)]", 
        string='- Manufacturing Operation', ondelete='cascade', required=True)
    dnk_people_inv_qty = fields.Float(string="- People Involved", digits='Product Price', groups="base.group_user")
    dnk_product_tmpl_id = fields.Many2one('product.template', '- Product Template', default=lambda self: self._get_dnk_product_tmpl_id())
    dnk_equipment_id = fields.Many2one('maintenance.equipment.category', related="dnk_manufacturing_op_id.dnk_equipment_id")
    dnk_time =  fields.Float(string="- Seconds",  related="dnk_manufacturing_op_id.dnk_time")
    dnk_help =  fields.Char(string="- Help", related="dnk_manufacturing_op_id.dnk_help")
    dnk_family_id =  fields.Many2one(comodel_name='product.category',
        string='- Family', related="dnk_product_tmpl_id.x_studio_field_GDdsl")
    dnk_order = fields.Text(
        '- Order', help="Orden de las personas")
    description = fields.Text(
        '- Description', related="dnk_manufacturing_op_id.description")
    
    
    @api.model
    def _get_dnk_product_tmpl_id(self):
        if 'active_model' in self._context and self._context['active_model'] == 'product.template':
            return self._context['active_id']
    
    @api.depends('dnk_product_tmpl_id')
    def get_maufacturig_op_dom(self):
        for a in self:
            val_dom = [('dnk_family_ids', 'ilike', a.dnk_product_tmpl_id.x_studio_field_GDdsl.id),
               ]
            a.dnk_manufacturing_op_dom = self.env['dnk.manufacturing.op'].search(val_dom).ids

    @api.depends('dnk_manufacturing_op_id')
    @api.onchange('dnk_manufacturing_op_id')
    def _change_equipment_category(self):
        print("Funcion Nombre")
        for record in self:
            if record.dnk_manufacturing_op_id:
                record.name = record.dnk_manufacturing_op_id.name
            else:
                record.name = "new"