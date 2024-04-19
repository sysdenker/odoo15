# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools, _, SUPERUSER_ID
from odoo.exceptions import UserError, AccessError, ValidationError


class DnkQualityClaimStages(models.Model):
    _name = "dnk.quality.claim.stage"
    _description = "Claim Stage"
    _rec_name = 'dnk_name'
    _order = "dnk_sequence, dnk_name, id"

    dnk_name = fields.Char('- Name', required=True, translate=True)
    dnk_description = fields.Text(translate=True)
    dnk_sequence = fields.Integer('- Sequence', default=1, help="Satages Order")
    # No se sigue el estándar porque los script buscan directamente fold
    # dnk_fold = fields.Boolean('- Mostrado en Kanban',
    # help='La etapa está plegada cuando no hay registros en la etapa para mostrar.')
    fold = fields.Boolean('- Shown in Kanban', help='Shown in Kanban View')

class DnkQualityClaimStages(models.Model):
    _name = "dnk.quality.claim.department"
    _description = "Claim Department"
    _rec_name = 'dnk_name'
    _order = "dnk_sequence, dnk_name, id"

    dnk_name = fields.Char('- Name', required=True, translate=True)
    dnk_description = fields.Text(translate=True)
    dnk_sequence = fields.Integer('- Sequence', default=1, help="Satages Order")
    # No se sigue el estándar porque los script buscan directamente fold
    # dnk_fold = fields.Boolean('- Mostrado en Kanban',
    # help='La etapa está plegada cuando no hay registros en la etapa para mostrar.')
    fold = fields.Boolean('- Shown in Kanban', help='Shown in Kanban View')


class DnkQualityClaimDepartment(models.Model):

    _name = "dnk.quality.claim.tags"
    _description = "Claim Tag"
    _rec_name = 'dnk_name'
    _order = "dnk_sequence, dnk_name, id"

    dnk_name = fields.Char('- Name', required=True, translate=True)
    dnk_company_id = fields.Many2one(
        'res.company', string='- Company',
        default=lambda self: self.env.company.id)
    dnk_sequence = fields.Integer('- Sequence', default=1, help="Satages Order")
    # No se sigue el estándar porque los script buscan directamente fold
    # dnk_fold = fields.Boolean('- Mostrado en Kanban',
    #   help='La etapa está plegada cuando no hay registros en la etapa para mostrar.')
    fold = fields.Boolean(
        '- Shown in Kanban',
        help='Shown in Kanban View')


class DnkQualityClaims(models.Model):
    _name = "dnk.quality.claims"
    _description = "Claim"
    _inherit = ['mail.thread']
    _rec_name = 'dnk_name'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'utm.mixin']

    @api.model
    def create(self, vals):

        vals['dnk_name'] = self.env['ir.sequence'].next_by_code(
            'dnk.quality.claims') or _('New')
        res = super(DnkQualityClaims, self).create(vals)
        if 'user_id' in vals and vals['user_id']:
            partner_id = self.env['res.users'].search([(
                'id', '=', vals['user_id'])], limit=1).partner_id
            self.message_subscribe(partner_ids=[partner_id.id])
        return res

    def write(self, vals):
        attachment_qty = self.get_attachment_qty()
        if 'dnk_stage_id' in vals and vals['dnk_stage_id']:
            dnk_stage = self.env['dnk.quality.claim.stage'].search([(
                'id', '=', vals['dnk_stage_id'])]).dnk_name
            if dnk_stage == 'Done' and attachment_qty <= 0:
                raise ValidationError(_('Es necesario ingresar al menos \
                un archivo adjunto para terminar la queja'))
        if 'user_id' in vals and vals['user_id']:
            partner_id = self.env['res.users'].search([(
                'id', '=', vals['user_id'])], limit=1).partner_id
            self.message_subscribe([partner_id.id])
            self.message_post(
                message_type='notification',
                partner_ids=[partner_id.id])
        res = super(DnkQualityClaims, self).write(vals)
        return res

    def name_get(self):
        result = []
        for claim in self:
            result.append((claim.id, "%s (#%d)" % (claim.dnk_name, claim.id)))
        return result

    @api.model
    def get_attachment_qty(self):
        attachment_search = self.env['ir.attachment'].search([(
            'res_model', '=', 'dnk.quality.claims'), ('res_id', '=', self.id)])
        return len(attachment_search)

    def _default_stage_id(self):
        claim_stage = self.env['dnk.quality.claim.stage'].sudo().search([])
        return claim_stage and claim_stage[0].id or False

    @api.model
    @api.onchange('dnk_order_id')
    def get_sale_order_name(self):
        self.dnk_sale_order_name = self.dnk_order_id.name

    @api.model
    def _read_group_stage_ids(self, stages, domain, order):
        stage_ids = stages._search([], order=order, access_rights_uid=SUPERUSER_ID)
        return stages.browse(stage_ids)

    def _default_user_id(self):
        if self._context and self._context.get('active_model', False) == 'dnk.quality.claims':
            return self.env['dnk.quality.claims'].search([(
                'id', '=', self._context.get('active_id', False))]).user_id
        return False

    def _update_invoice_fields(self):
        self.dnk_acc_move_qty = self.dnk_acc_move_line_id.quantity

    dnk_name = fields.Char(string='- Folio', index=True, readonly=True, default=lambda self: _('New'))
    dnk_company_id = fields.Many2one('res.company', string='- Company', default=lambda self: self.env.company.id, readonly=True)
    dnk_acc_move_id = fields.Many2one('account.move', '- Invoice', required=True, ondelete='cascade', tracking=True)
    dnk_acc_move_line_id = fields.Many2one(
        'account.move.line', required=True, ondelete='cascade', string='- Invoice Line',
        domain="[('move_id', '=', dnk_acc_move_id)]", store=True,
        tracking=True)

    dnk_invoice_date = fields.Date(string='- Invoice Date', related='dnk_acc_move_id.invoice_date')
    dnk_currency_id = fields.Many2one('res.currency', string='Currency', related='dnk_acc_move_id.currency_id')
    dnk_product_id = fields.Many2one('product.product', string='- Product', related='dnk_acc_move_line_id.product_id', store=True, tracking=True)
    dnk_subfamily_id = fields.Many2one('product.category', string='- Subfamily', store=True, related='dnk_product_id.product_tmpl_id.categ_id', tracking=True)
    dnk_family_id = fields.Many2one('product.category', string='- Family', store=True, related='dnk_subfamily_id.parent_id', tracking=True)
    dnk_color_id = fields.Many2one('product.category', string='- Color', store=True, related='dnk_family_id.parent_id', tracking=True)

    dnk_product_default_code = fields.Char(string='- Internal Reference', related='dnk_product_id.default_code', store=True, tracking=True)
    dnk_order_id = fields.Many2one('sale.order', string='- Sale Order', related='dnk_acc_move_id.dnk_order_id', store=True, tracking=True)
    dnk_sale_order_name = fields.Char(string='- Origin', store=True)
    dnk_manufacturing_order_id = fields.Many2one(
        'mrp.production', string='- Manufacturin Order',
        domain="[('origin', '=', dnk_sale_order_name)]",
        store=True, tracking=True)
    dnk_partner_id = fields.Many2one(
        'res.partner', string='- Customer',
        related='dnk_acc_move_id.partner_id.commercial_partner_id',
        store=True, tracking=True)
    user_id = fields.Many2one('res.users', string='- Assigned to', default=lambda self: self._default_user_id(), tracking=True)  # editable
    dnk_stage_id = fields.Many2one(
        'dnk.quality.claim.stage', string='- Stage', index=True,
        # group_expand='_read_group_stage_ids',
        default=lambda self: self._default_stage_id(),
        tracking=True)
    dnk_department_id = fields.Many2one(
        'dnk.quality.claim.department', string='- Department', index=True, tracking=True)
    dnk_tag_id = fields.Many2one('dnk.quality.claim.tags', string='- Tag', index=True, tracking=True)
    dnk_active = fields.Boolean('- Active', default=True)
    dnk_color = fields.Integer('- Color', default=0)

    dnk_damaged_qty = fields.Integer('- Damaged Quantity')
    dnk_acc_move_qty = fields.Integer('- Invoiced Qty', compute="_update_invoice_fields")
    dnk_description = fields.Text('- Description', tracking=True)
    dnk_observations = fields.Text('- Observations', tracking=True)
    dnk_date = fields.Datetime('- Claim Date', default=lambda self: fields.Datetime.now())
    dnk_evualuation = fields.Selection([
        ('procede', 'Procede'),
        ('no_procede', 'No procede'),
        ('info', 'Información')], string="- Evaluation",
        tracking=True)
    dnk_desc_evaluation = fields.Text(
        '- Evaluation Description', tracking=True)

    dnk_claim_value = fields.Float(
        '- Claim Value (USD)', tracking=True)
