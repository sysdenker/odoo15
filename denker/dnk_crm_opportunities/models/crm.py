# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from lxml import etree
from datetime import datetime
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError, RedirectWarning, ValidationError

class DnkCRMContactChannel(models.Model):
    _name = "dnk.crm.contact.channel"
    _description = "Contact Channel"
    _rec_name = 'name'
    _order = "sequence, name, id"

    name = fields.Char(string='- Nombre', required=True, translate=True)
    description = fields.Text(string='- Descripción', translate=True)
    sequence = fields.Integer(string='- Secuencia', default=1, help="Orden de las etapas.")
    color = fields.Integer(
        '- Color', help='Color de la etiqueta.')


class DnkCRMPurchaseIntent(models.Model):
    _name = "dnk.crm.purchase.intent"
    _description = "Purchase Intent"
    _rec_name = 'name'
    _order = "sequence, name, id"

    name = fields.Char(string='- Nombre', required=True, translate=True)
    description = fields.Text(string='- Descripción', translate=True)
    sequence = fields.Integer(string='- Secuencia', default=1, help="Orden de las etapas.")
    color = fields.Integer(
        '- Color', help='Color de la etiqueta.')


class CRMLead(models.Model):
    _name = 'crm.lead'
    _inherit = ['crm.lead', 'rating.mixin',]

    dnk_lead_partner_id = fields.Many2one(
        'res.partner', string='Lead Customer', check_company=True, index=True, tracking=10,
        help="Para seguimiento de los leads")

    def button_assign_dealer(self):
        return {
            'name': ('Assigned to Dealer'),
            'view_mode': 'form',
            'res_model': 'dnk.crm.dealer.assigned',
            'view_id': self.env.ref('dnk_crm_opportunities.dnk_view_crm_dealer').id,
            'type': 'ir.actions.act_window',
            'context': {
                'default_dnk_crm_lead_id': self.id
            },
            'target': 'new',
        }

    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
        res = super(CRMLead, self).fields_view_get(view_id=view_id, view_type=view_type, toolbar=toolbar, submenu=submenu)
        doc = etree.XML(res['arch'])
        for node in doc.xpath("//field[@name='dnk_family_id']"):
            colors = self.env['product.category'].search([('parent_id', '=', False)])
            if colors:
                parent_categ = []
                for color in colors:
                    if color:
                        parent_categ.append(color.id)
                if parent_categ:
                    node.set('domain', "[('parent_id', 'in', " + str(parent_categ) + ")]")
        res['arch'] = etree.tostring(doc)
        return res

    @api.onchange('dnk_price', 'dnk_pieces')
    @api.depends('dnk_price', 'dnk_pieces')
    def _get_revenue(self):
        for lead in self:
            lead.expected_revenue = lead.dnk_price * lead.dnk_pieces

    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        for rec in self:
            # res = super(CRMLead, self)._onchange_partner_id()
            # if rec.type == 'opportunity': # 18Ene2024 Petición de EMurillo
            suc = rec.dnk_sale_city_id.dnk_code if rec.dnk_sale_city_id.dnk_code else ""
            fam = rec.dnk_family_id.dnk_abbreviation if rec.dnk_family_id.dnk_abbreviation else ""
            subfam = rec.dnk_subfamily_id.dnk_abbreviation if rec.dnk_subfamily_id.dnk_abbreviation else ""
            if rec.partner_id.parent_id:
                name = rec.partner_id.parent_id.name if rec.partner_id.parent_name else ""
            else:
                name = rec.partner_id.name if rec.partner_id.name else ""
            rec.name = suc + " - " + fam + " - " + subfam + " - " + name #
            # return res

    @api.onchange('dnk_family_id','dnk_sale_city_id')
    def _onchange_family_id(self):
        self._onchange_partner_id()

    def write(self, vals):
        for rec in self:
            res = super(CRMLead, self).write(vals)
            # if rec.type == 'opportunity' and (rec.dnk_price <= 0 or rec.dnk_pieces <= 0):
            #    raise ValidationError(_('The Price and Pieces must be greater than 0.'))
            return res

    @api.model
    def create(self, vals):
        if vals.get('type') == 'opportunity' and (vals.get('dnk_price') <= 0 or vals.get('dnk_pieces') <= 0):
            raise ValidationError(_('Price and Pieces must be greater than 0.'))
        result = super(CRMLead, self).create(vals)
        return result

    def _dnk_compute_sale_usd_amount(self):
        for lead in self:
            total = 0.0
            self._cr.execute("SELECT SUM(dnk_usd_amount) FROM sale_order WHERE state NOT IN ('draft', 'sent', 'cancel') AND date_part('year',create_date) = date_part('year', now()) AND opportunity_id = %s", [lead.id])
            for res in self.env.cr.fetchall():
                lead.dnk_sale_usd_amount = res[0] if res[0] else 0

    def _dnk_compute_lastyear_sale_usd_amount(self):
        for lead in self:
            total = 0.0
            self._cr.execute("SELECT SUM(dnk_usd_amount) FROM sale_order WHERE state NOT IN ('draft', 'sent', 'cancel') AND date_part('year',create_date) = date_part('year', now())-1 AND opportunity_id = %s", [lead.id])
            for res in self.env.cr.fetchall():
                lead.dnk_sale_usd_lastyear_amount = res[0] if res[0] else 0

    def _dnk_compute_sale_year(self):
        # Solo para mostrar en el botón el año de venta que se está consultando
        today = datetime.today()

        for lead in self:
            lead.dnk_current_year = datetime.today().strftime("%Y")
            lead.dnk_last_year = today.year - 1

    def _dnk_compute_sale_usd_total_amount(self):
        for lead in self:
            total = 0.0
            self._cr.execute("SELECT SUM(dnk_usd_amount) FROM sale_order WHERE state NOT IN ('draft', 'sent', 'cancel') AND opportunity_id = %s ", [lead.id])
            for res in self.env.cr.fetchall():
                lead.dnk_sale_usd_total_amount = res[0] if res[0] else 0

    dnk_sale_usd_amount = fields.Float(compute='_dnk_compute_sale_usd_amount', string="- Sum of Current Year Orders", help="USD Current Year Confirmed Orders")
    dnk_sale_usd_lastyear_amount = fields.Float(compute='_dnk_compute_lastyear_sale_usd_amount', string="- Sum of Last Year Orders", help="Last Year USD Confirmed Orders")
    dnk_current_year = fields.Char(compute='_dnk_compute_sale_year', string="- Current Year", help="Current Year")
    dnk_last_year = fields.Char(compute='_dnk_compute_sale_year', string="- Last Year", help="Last Year")
    dnk_sale_usd_total_amount = fields.Float(compute='_dnk_compute_sale_usd_total_amount', string="- Sum Orders", help="USD Confirmed Orders")

    dnk_final_customer_id = fields.Many2one('res.partner', '- Final Customer')
    dnk_dealer_id = fields.Many2one('res.partner', '- Dealer')
    dnk_is_vendor = fields.Boolean('- Is Vendor?')
    dnk_family_id = fields.Many2one('product.category', '- Family', required=False)
    dnk_subfamily_id = fields.Many2one('product.category', '- SubFamily')
    dnk_product_id = fields.Many2one('product.product', '- Product')
    dnk_price = fields.Float("- Price")
    dnk_pieces = fields.Integer("- Pieces")
    dnk_contact_channel_ids = fields.Many2many(
        'dnk.crm.contact.channel', string='- Channel', readonly=False, store=True, compute_sudo=False)
    dnk_purchase_intent_id = fields.Many2one('dnk.crm.purchase.intent', string='- Purchase Intent',
        help="The extent to which customers are willing and inclined to buy a product or service")
    dnk_task_count = fields.Integer(string='Project Task Count', compute='_compute_project_task_count')


    def _compute_project_task_count(self):
        for rec in self:
            rec.dnk_task_count = self.env['project.task'].search_count([('x_studio_lead_ids', '=', rec.id)])


    def dnk_project_task_action(self):
        Task = self.env['project.task'].search([('x_studio_lead_ids', '=', self.id)])
        res = [line.id for line in Task]
        return {
            'domain': "[('id','in',[" + ','.join(map(str, list(res))) + "])]",
            'name': _('Project Task'),
            'view_mode': 'tree,form',
            'view_type': 'form',
            'res_model': 'project.task',
            'type': 'ir.actions.act_window', }

    @api.model
    def cron_update_crm_to_working(self):
        print ("++++++++++++Cron CRM Update Status New to Working Executed++++++++++++++++++++++")
        # Se van a buscar todas las oportinidades, que estén en estatus Nuevo y que ya tengan venta
        # en últimos seis meses.

        lead_working = self.env['crm.lead']
        lead_ids = lead_working.search([('active', '=', True), ('type', '=', 'opportunity'), ('stage_id', 'in', [(1)])])
        if lead_ids:
            today = datetime.today()
            date = today - relativedelta(months = 6)
            # print(date)
            # print(len(lead_ids))
            for lead in lead_ids:
                # Actividades
                activity_ids = self.env['mail.activity'].search([('res_model', '=', 'crm.lead'), ('res_id', '=', lead.id), ('create_date', '>', date)])
                if activity_ids:
                    lead.stage_id = 3
                    # print("Si hay actividad de la opp ", lead.name)
                sale_ids = self.env['sale.order'].search([('opportunity_id', '=', lead.id), ('create_date', '>', date), ('state', 'not in',  [('cancel'), ('draft'), ('sent')])])
                if sale_ids:
                    # print("Si hay sales de la opp ", lead.name)
                    lead.stage_id = 3

    @api.model
    def cron_update_crm_to_selling(self):
        print ("++++++++++++Cron CRM Update Status Working to Selling++++++++++++++++++++++")
        # Se van a buscar todas las oportinidades, que estén en estatus Working o Sale Stopped y que tengan venta
        # en los últimos seis meses y que sea mayor al 16% del presupuesto  anual

        lead_working = self.env['crm.lead']
        lead_ids = lead_working.search([('active', '=', True), ('type', '=', 'opportunity'), ('stage_id', 'in', [(3), (5)])])
        if lead_ids:
            today = datetime.today()
            date = today - relativedelta(months = 6)
            for lead in lead_ids:
                sale_ids = self.env['sale.order'].search([('opportunity_id', '=', lead.id), ('create_date', '>', date), ('state', 'not in', [('cancel'), ('draft'), ('sent')])])
                venta = 0
                if sale_ids:
                    for sale_id in sale_ids:
                        venta += sale_id.dnk_usd_amount
                    if lead.expected_revenue > 0 and venta > 0 and venta > (lead.expected_revenue * 0.08):
                        print("Pedidos con venta mayor al 8 %", lead.name)
                        lead.stage_id = 2

    @api.model
    def cron_update_crm_to_sale_stopped(self):
        print ("++++++++++++Cron CRM Update Status Selling to Sale Stopped++++++++++++++++++++++")
        # Se van a buscar todas las oportinidades, que estén en estatus Vendiendo y que no tengan venta
        # en los últimos seis meses.

        lead_working = self.env['crm.lead']
        lead_ids = lead_working.search([('active', '=', True), ('type', '=', 'opportunity'), ('stage_id', 'in', [(2)])])
        if lead_ids:
            today = datetime.today()
            date = today - relativedelta(months = 6)
            for lead in lead_ids:
                sale_ids = self.env['sale.order'].search([('opportunity_id', '=', lead.id), ('create_date', '>', date), ('state', 'not in', [('cancel'), ('draft'), ('sent')])])
                if not sale_ids:
                    print("No  hay sales de la opp ", lead.name)
                    lead.stage_id = 5
