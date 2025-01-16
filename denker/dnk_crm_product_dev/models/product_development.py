# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools, _, SUPERUSER_ID
from odoo.exceptions import UserError, AccessError, ValidationError
from datetime import datetime, date


class DnkProductDevelopmentStage(models.Model):
    _name = "dnk.crm.pd.stage"
    _description = "Stage"
    _rec_name = 'name'
    _order = "sequence, name, id"

    name = fields.Char(string='- Stage', required=True, translate=True)
    dnk_description = fields.Text(string=' - Description', translate=True)
    sequence = fields.Integer(string='- Sequence', default=1, help="Orden de las etapas.")
    fold = fields.Boolean(
        '- Mostrado en Kanban', help='La etapa está plegada cuando no hay registros en la etapa para mostrar.')
    dnk_department = fields.Char(string='- Department', required=True, translate=True)
    dnk_stage_type = fields.Selection(
        [('operative', 'Operative'), ('commercial', 'Commercial'), ('final', 'Final')],
        string="- Stage Type", help="Para medir tiempos en etapas")

    active = fields.Boolean(string='- Activo', default=True)


    @api.depends('dnk_description', 'sequence', 'dnk_department')
    @api.onchange('dnk_description', 'sequence', 'dnk_department')
    def _get_name(self):
        for record in self:
            record.name = "[" + str(record.sequence) + "-" + record.dnk_department + "] " + record.dnk_description


class DnkPdevStageHist(models.Model):
    _name = "dnk.crm.pd.stage.hist"
    _description = "Stage Hist"
    _rec_name = 'dnk_pd_id'
    _order = "dnk_pd_id"

    dnk_pd_id = fields.Many2one('dnk.crm.product.dev', string='- PDev')
    dnk_stage_id = fields.Many2one('dnk.crm.pd.stage', string='- Stage')
    dnk_prev_stage_id = fields.Many2one('dnk.crm.pd.stage', string='- Prev Stage')
    dnk_last_update = fields.Datetime(string='- Last Update')
    dnk_date_diff = fields.Char(string='- Date Diff')
    dnk_days_apart = fields.Char(string='- Days Apart')
    dnk_pd_version = fields.Integer(string='- Version')
    dnk_stage_type = fields.Selection(
        [('operative', 'Operative'), ('commercial', 'Commercial'), ('final', 'Final')],
        string="- Stage Type", help="Para medir tiempos en etapas")


class DnkDevelopmentType(models.Model):
    _name = "dnk.crm.pd.type"
    _description = "Type of Development"
    _rec_name = 'name'
    _order = "sequence, name, id"

    name = fields.Char(string='- Name', required=True, translate=True)
    sequence = fields.Integer(string='- Sequence', default=1, help="Orden")
    active = fields.Boolean(string='- Activo', default=True)
    fold = fields.Boolean(string='- Mostrado en Kanban', help='La etapa está plegada cuando no hay registros en la etapa para mostrar.')
    # dnk_department = fields.Char(string='- Department', required=True, translate=True)
    dnk_ps_delivery_date = fields.Integer(string='- Product Sample Delivery Days', help="Tiempo de entrega para la muestra")
    dnk_pc_delivery_date = fields.Integer(string='- Product Cost Delivery Days', help="Tiempo de entrega para el Costeo")

PDVersionUpdt = {13, 85}

class DnkProductDevelopment(models.Model):
    _name = "dnk.crm.product.dev"
    _inherit = ['mail.thread']
    _rec_name = 'name'
    _description = "Product Development"
    _inherit = ['mail.thread', 'mail.activity.mixin', 'utm.mixin']



    name = fields.Char(string='- Folio', index=True, default=lambda self: _('New'), copy=True)
    dnk_stage_id = fields.Many2one('dnk.crm.pd.stage', string='- Stage', index=True, default=lambda self: self._default_stage_id(), tracking=True)
    dnk_last_stage_update = fields.Datetime(string= "- Last Stage Update")
    dnk_stage_type = fields.Selection(
        [('operative', 'Operative'), ('commercial', 'Commercial'), ('final', 'Final')],
        string="- Stage Type", help="Para medir tiempos en etapas", tracking=True, copy=True)
    active = fields.Boolean(string='- Activo', default=True)
    dnk_product_ids = fields.One2many('dnk.crm.product.dev.line', 'dnk_pd_id', string='Product', copy=True, auto_join=True)
    dnk_line_count = fields.Integer(string='- Product Line Counter', compute="dnk_line_counter")
    dnk_new_product = fields.Boolean(string='- New Product?', copy=True)
    dnk_delivery_address_id = fields.Many2one('res.partner', string='- Delivery Address', ondelete='cascade', tracking=True, copy=True)
    dnk_mrp_prod_count = fields.Integer(string='Manufacturing Orders', compute='_compute_mrp_prod_count')
    dnk_delivery_count = fields.Integer(string='Delivery', compute='_compute_stock_picking_count')
    dnk_mrp_eco_count = fields.Integer(string='PLM', compute='_compute_mrp_eco_count')
    dnk_pd_type_id = fields.Many2one('dnk.crm.pd.type', string='- Type', ondelete='cascade', tracking=True, copy=True)
    dnk_pd_version = fields.Integer(string='- Version', default=1, help="Product Version")



    dnk_spec_req = fields.Boolean(string='- Is specification required?', default=False, copy=True, help ="Check this if the specification is required")
    dnk_spec_ref = fields.Char(string='- Spec. Reference', help ="Link to specification reference", copy=True)
    dnk_final_spec = fields.Char(string='- Final Specification', help ="Link to Final Specification", copy=True)
    dnk_ref_doc = fields.Char(string='- Reference Document', help ="Link to Reference Document", copy=True)
    dnk_project_id = fields.Many2one('project.project', string='- Project (I&D)', ondelete='cascade', help ="Related Project", tracking=True, copy=True)
    dnk_model = fields.Char(string='- Model',help ="Model", copy=True,)
    dnk_folder = fields.Char(string='- Folder', help ="Folder", copy=True)


    # Información de la oportunidad
    dnk_lead_id = fields.Many2one('crm.lead', string='- Lead', required=True, ondelete='cascade', default=lambda self: self._default_lead_id(), tracking=True)
    currency_id = fields.Many2one('res.currency', string='- Currency', required=True, ondelete='cascade', default=lambda self: self.env['res.currency'].search([('name', '=', 'USD')]).id,readonly=True)
    dnk_expected_revenue = fields.Monetary(string='- Expected Revenue', related="dnk_lead_id.expected_revenue")
    dnk_lead_stage = fields.Many2one('crm.stage', string='- Lead Stage', related="dnk_lead_id.stage_id")
    dnk_user_id = fields.Many2one('res.users', string='- Sales Person', related="dnk_lead_id.user_id")
    dnk_team_id = fields.Many2one('crm.team', string='- Canal de venta', related="dnk_lead_id.team_id")
    dnk_customer_serv_id = fields.Many2one('res.users', string='- Customer Service', related="dnk_team_id.user_id")
    dnk_company_id = fields.Many2one('res.company', string='- Company', default=lambda self: self.env.company.id, readonly=True, tracking=True)
    dnk_family_id = fields.Many2one('product.category', string='- Family', related='dnk_lead_id.dnk_family_id', tracking=True)
    dnk_categ_type = fields.Char(string='- Category Type', compute="_compute_categ_type")


    dnk_subfamily_id = fields.Many2one('product.category', string='- Subfamily', related='dnk_lead_id.dnk_subfamily_id', tracking=True, store=True)
    dnk_sale_order_id = fields.Many2one('sale.order', string='- Order', tracking=True)

    @api.depends('dnk_family_id')
    @api.onchange('dnk_family_id')
    def _compute_categ_type(self):
        for rec in self:
            # print ("ID ", rec.dnk_family_id.id)
            rec.dnk_categ_type = 'otro'
            if rec.dnk_family_id.id in [212]:
                rec.dnk_categ_type = 'bata'
            if rec.dnk_family_id.id in [217]:
                rec.dnk_categ_type = 'bolsa'
            if rec.dnk_family_id.id in [208, 220, 222]:
                rec.dnk_categ_type = 'equipo'
            if rec.dnk_family_id.id in [210]:
                rec.dnk_categ_type = 'servicio'
            if rec.dnk_family_id.id in [218, 202, 219]:
                rec.dnk_categ_type = 'empaque'
            if rec.dnk_family_id.id in [214]:
                rec.dnk_categ_type = 'overol'
            if rec.dnk_family_id.id in [215]:
                rec.dnk_categ_type = 'prenda'


    def _default_lead_id(self):
        if self._context and self._context.get('active_model', False) == 'crm.lead':
            return self._context.get('active_id', False)
        return False

    def _compute_mrp_prod_count(self):
        for rec in self:
            rec.dnk_mrp_prod_count = self.env['mrp.production'].search_count([('dnk_pd_id', '=', rec.id)])

    def _compute_stock_picking_count(self):
        for rec in self:
            rec.dnk_delivery_count = self.env['stock.picking'].search_count([('dnk_pd_id', '=', rec.id)])

    def _compute_mrp_eco_count(self):
        for rec in self:
            rec.dnk_mrp_eco_count = self.env['mrp.eco'].search_count([('dnk_pd_id', '=', rec.id)])

    def dnk_line_counter(self):
        for rec in self:
            rec.dnk_line_count = self.env['dnk.crm.product.dev.line'].search_count([('dnk_pd_id', '=', rec.id)])

    def _default_stage_id(self):
        pd_stage = self.env['dnk.crm.pd.stage'].sudo().search([])
        return pd_stage and pd_stage[0].id or False

    # def _default_user_id(self):
    #    if self._context and self._context.get('active_model', False) == 'crm.lead':
    #        return self.env['crm.lead'].search([('id', '=', self._context.get('active_id', False))]).user_id
    #    return False

    def dnk_crm_pdev_stage_hist_action(self):
        SategeH = self.env['dnk.crm.pd.stage.hist'].search([('dnk_pd_id', 'ilike', self.id)])
        res = [line.id for line in SategeH]
        return {
            'domain': "[('id','in',[" + ','.join(map(str, list(res))) + "])]",
            'name': _('Stage Changes '),
            'view_mode': 'tree,form',
            'view_type': 'form',
            'res_model': 'dnk.crm.pd.stage.hist',
            'type': 'ir.actions.act_window', }

    def dnk_crm_pdev_plm_action(self):
        PLMs = self.env['mrp.eco'].search([('dnk_pd_id', 'ilike', self.id)])
        res = [line.id for line in PLMs]
        return {
            'domain': "[('id','in',[" + ','.join(map(str, list(res))) + "])]",
            'name': _('Engineering Change Orders'),
            'view_mode': 'tree,form',
            'view_type': 'form',
            'res_model': 'mrp.eco',
            'type': 'ir.actions.act_window', }

    def action_pdev_mo_view(self):
        MOs = self.env['mrp.production'].search([('dnk_pd_id', 'ilike', self.id)])
        res = [line.id for line in MOs]
        return {
            'domain': "[('id','in',[" + ','.join(map(str, list(res))) + "])]",
            'name': _('Manufacturing Orders'),
            'view_mode': 'tree,form',
            'view_type': 'form',
            'res_model': 'mrp.production',
            'type': 'ir.actions.act_window', }

    def action_pdev_delivery_view(self):
        Deliverys = self.env['stock.picking'].search([('dnk_pd_id', 'ilike', self.id)])
        res = [line.id for line in Deliverys]
        return {
            'domain': "[('id','in',[" + ','.join(map(str, list(res))) + "])]",
            'name': _('Transfers'),
            'view_mode': 'tree,form',
            'view_type': 'form',
            'res_model': 'stock.picking',
            'type': 'ir.actions.act_window', }


    """
    @api.depends('dnk_product_ids', 'dnk_new_product')
    @api.onchange('dnk_product_ids', 'dnk_new_product')
    def _change_new_product(self):
        for record in self:
            for pd in record.dnk_product_ids:
                if pd.dnk_new_product:
                    if pd.dnk_new_default_code:
                        pd._change_new_product()
                else :
                    pd.name = pd.dnk_product_id.default_code
    """

    def write(self, values):
        if 'dnk_stage_id' in values:
            for record in self:
                print(values)
                stage= self.env['dnk.crm.pd.stage'].search([('id', '=', values['dnk_stage_id'])])
                if stage.dnk_stage_type != record.dnk_stage_type:
                    record.dnk_stage_type = stage.dnk_stage_type
                if record.dnk_stage_id.sequence >=90 and stage.sequence <= 90:
                    raise UserError(_("No es posible regresar a una etapa de ese nivel"))
                if record.dnk_line_count < 1:
                    raise UserError(_("Es necesario completar la información para cambiar el estatus"))
                if stage.sequence in PDVersionUpdt:
                    record.dnk_pd_version = record.dnk_pd_version + 1

                diff = datetime.now() - (record.dnk_last_stage_update or record.create_date)
                self.env['dnk.crm.pd.stage.hist'].create({
                    'dnk_stage_id': values['dnk_stage_id'],
                    'dnk_prev_stage_id': record.dnk_stage_id.id,
                    'dnk_pd_id': record.id,
                    'dnk_date_diff': diff,
                    'dnk_days_apart': diff.days,
                    'dnk_pd_version': record.dnk_pd_version,
                    'dnk_stage_type': record.dnk_stage_type,
                    'dnk_last_update': record.dnk_last_stage_update or record.create_date,
                })
                record.dnk_last_stage_update = datetime.now()

                # raise UserError(_("Es necesario completar la información para cambiar el estatus"))
        result = super(DnkProductDevelopment, self).write(values)
        return result
