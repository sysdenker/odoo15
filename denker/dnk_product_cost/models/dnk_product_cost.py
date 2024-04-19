# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools, _, SUPERUSER_ID
from odoo.exceptions import UserError, AccessError, ValidationError


class DnkBomsTemp(models.Model):
    _name = 'dnk.mrp.bom'
    _rec_name = 'name'
    _description = "Denker Temporal BOM"

    def dnk_get_name(self):
        for rec in self:
            code = rec.dnk_bom_id.code if rec.dnk_bom_id.code else rec.dnk_product_id.name
            rec.name = "[USD $" + str(rec.dnk_bom_cost) + "] " + code

    dnk_product_id = fields.Many2one('product.product', '- Product', ondelete='cascade')
    dnk_bom_id = fields.Many2one('mrp.bom', '- Bill of Materials')
    name = fields.Char(compute='dnk_get_name')
    dnk_bom_cost = fields.Float(string="- Bom Cost", digits='Product Price', groups="base.group_user")
    dnk_usd_cost_fixed_rate = fields.Float(string="- USD Cost Fixed Rate", help="USD Cost Fixed Rate")
    dnk_attribute_cost = fields.Float(string="- Attributes Cost", digits='Product Price', groups="base.group_user")
    dnk_standard_cost = fields.Float(string="- Denker Standard Cost", digits='Product Price', help="Costo Estándar para Costeo.")
    dnk_commercial_cost = fields.Float(string="- Denker Commercial Cost", digits='Product Price', help="Costo Estándar para Costeo.")
    dnk_attr_value_html = fields.Html('- Attribute Values')
    dnk_move_raws_html = fields.Html('- Consumed Materials')


class DnkProductCosts(models.Model):
    _name = 'dnk.product.cost'
    _rec_name = 'dnk_name'
    _description = "Denker Product Cost"

    dnk_name = fields.Char(string='- Default Code', index=True, readonly=True, default=lambda self: _('New'))
    dnk_company_id = fields.Many2one('res.company', string='- Company', default=lambda self: self.env.company, readonly=True)
    dnk_active = fields.Boolean('- Activo', default=True)
    dnk_cost_option = fields.Selection([('std_price', 'Costo Promedio'), ('dnk_cost', 'Costo Estándar Dnk')], string="- Opción de Costeo", default='dnk_cost')
    dnk_description = fields.Text('Notas')

    dnk_usd_cost_fixed_rate = fields.Monetary(string="- USD Cost Fixed Rate", currency_field='dnk_currency_rate', readonly=True, help="USD Cost Fixed Rate to use on Margin.")
    dnk_currency_rate = fields.Many2one('res.currency', string='- Cost Currency', default=3, readonly=True)
    dnk_product_id = fields.Many2one('product.product', '- Product', ondelete='cascade', default=lambda self: self.dnk_get_product_id())

    dnk_total_cost = fields.Float(string="- Total Cost (USD)", digits='Product Price', readonly=True, compute="_get_total_cost", store=True, groups="base.group_user")

    dnk_standard_cost = fields.Float(string="- Standard Cost (USD)", digits='Product Price', groups="base.group_user")
    dnk_commercial_cost = fields.Float(string="- Denker Commercial Cost", digits='Product Price', help="Costo Estándar para Costeo.")
    dnk_raw_mat_cost = fields.Float(string="- Raw Material Cost (USD)", digits='Product Price', groups="base.group_user")
    dnk_labour_cost = fields.Float(string="- Labour Cost (USD)", digits='Product Price', default=lambda self: self.dnk_get_labour_cost())
    dnk_indirect_cost = fields.Float(string="- Indirect Cost(USD)", digits='Product Price', default=lambda self: self.dnk_get_indirect_cost())

    dnk_product_bom_cost = fields.Many2one('dnk.mrp.bom', string="- Bill of Materials")

    dnk_bom_ids = fields.One2many('mrp.bom', related='dnk_product_id.bom_ids')
    dnk_attr_value_html = fields.Html('- Attribute Values')
    dnk_attribute_cost = fields.Float(string="- Labor Attributes Cost", digits='Product Price', groups="base.group_user")
    dnk_move_raws_html = fields.Html('- Consumed Materials')

    @api.model
    def dnk_get_labour_cost(self, ):
        return self._context['dnk_labour_cost'] if 'dnk_labour_cost' in self._context else False

    @api.model
    def dnk_get_indirect_cost(self, dnk_indirect_cost_ids=False):
        for rec in self:
            costos_gif = 0
            costo_manufactura = False
            if 'dnk_indirect_cost' in self._context and self._context['dnk_indirect_cost']:
                costo_manufactura = self.env['dnk.indirect.manufacturing.cost'].search([('id', 'in', self._context['dnk_indirect_cost'])])
            if dnk_indirect_cost_ids:
                costo_manufactura = self.env['dnk.indirect.manufacturing.cost'].search([('id', 'in', dnk_indirect_cost_ids)])
            if costo_manufactura:
                for mc in costo_manufactura:
                    if mc.dnk_type == 'unit':
                        costos_gif = costos_gif + mc.dnk_value
                    if mc.dnk_type == 'percent':
                        costos_gif = costos_gif + (rec.dnk_raw_mat_cost * mc.dnk_value) / 100
                rec.dnk_indirect_cost = costos_gif
            return costos_gif or False

    @api.model
    def dnk_get_product_id(self):
        if 'active_model' in self._context and self._context['active_model'] == 'product.product':
            return self._context['active_id']

    @api.onchange("dnk_product_bom_cost")
    def dnk_mrp_bom_cost(self):
        for rec in self:
            rec.change_product_cost()
            rec.dnk_get_indirect_cost()

    def change_product_cost(self):
        for rec in self:
            if 'active_model' in self._context and self._context['active_model'] == 'product.product':
                if self.dnk_cost_option == 'dnk_cost':
                    self.dnk_raw_mat_cost = rec.dnk_product_bom_cost.dnk_standard_cost
                else:
                    self.dnk_raw_mat_cost = rec.dnk_product_bom_cost.dnk_bom_cost
                self.dnk_attribute_cost = rec.dnk_product_bom_cost.dnk_attribute_cost
                self.dnk_move_raws_html = rec.dnk_product_bom_cost.dnk_move_raws_html
                self.dnk_attr_value_html = rec.dnk_product_bom_cost.dnk_attr_value_html

    @api.onchange('dnk_cost_option')
    def update_cost_cost_option(self):
        for rec in self:
            rec.change_product_cost()
            rec._get_total_cost()

    @api.onchange('dnk_raw_mat_cost', 'dnk_labour_cost', 'dnk_indirect_cost')
    def update_total_cost(self):
        for rec in self:
            rec._get_total_cost()

    @api.model
    def _get_total_cost(self):
        self.dnk_total_cost = self.dnk_raw_mat_cost + self.dnk_labour_cost + self.dnk_indirect_cost + self.dnk_attribute_cost

    def dnk_change_cost(self):
        return {'type': 'ir.actions.act_window_close'}

    @api.model
    def create(self, vals):
        if 'dnk_product_id' not in vals:
            if 'active_model' in self._context:
                NombreMod = self._context['active_model']
                id = self._context['active_id']
            else:
                if vals['dnk_product_tmpl_id']:
                    NombreMod = 'product.template'
                    id = vals['dnk_product_tmpl_id']
                else:
                    NombreMod = 'product.product'
                    id = vals['dnk_product_id']
            vals['dnk_name'] = self.env[NombreMod].search([('id', '=', id)]).default_code
            Productos = self.env[NombreMod]
            product = Productos.browse(id)
            Total = vals['dnk_raw_mat_cost'] + vals['dnk_labour_cost'] + vals['dnk_indirect_cost'] + vals['dnk_attribute_cost']
            product.dnk_raw_mat_cost = vals['dnk_raw_mat_cost']
            product.dnk_labour_cost = vals['dnk_labour_cost']
            product.dnk_indirect_cost = vals['dnk_indirect_cost']
            product.dnk_attribute_cost = vals['dnk_attribute_cost']
            product.dnk_total_cost = Total
            usd_fixed_rate = product.product_tmpl_id.company_id.dnk_usd_cost_fixed_rate or self.env.user.company_id.dnk_usd_cost_fixed_rate
            vals['dnk_usd_cost_fixed_rate'] = usd_fixed_rate
            vals['dnk_product_id'] = id
            vals['dnk_bom_ids'] = product.bom_ids
            vals['dnk_total_cost'] = Total
        return super(DnkProductCosts, self).create(vals)
