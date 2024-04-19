# -*- coding: utf-8 -*-

from odoo import fields, api, models, _
from odoo.exceptions import ValidationError


class PrintingLabelGroup(models.Model):
    _name = 'dnk.printing.label.group'
    _description = 'To group labels from a model'
    _rec_name = 'dnk_name'
    _order = 'dnk_model_id, dnk_name, id'

    dnk_name = fields.Char(string='- Name', required=True, help='Label Group Name.')
    dnk_active = fields.Boolean(string='- Active', default=True)
    dnk_description = fields.Char(string='- Description', help='Long description for this label group.')
    dnk_model_id = fields.Many2one(
        comodel_name='ir.model', string='- Model', required=True, ondelete='cascade',
        help='Model used to print this label.')
    dnk_ir_ui_view_ids = fields.One2many(
        comodel_name='ir.ui.view', inverse_name='dnk_label_group_id',
        string='- Label Views',
        help='Views which will be show to select on printing the label.', copy=False)
    dnk_action_window_id = fields.Many2one(
        comodel_name='ir.actions.act_window', string='- Action', readonly=True)
    dnk_script_file_extension = fields.Char(string='- Script File Extension', required=True, size=3, help='Script File Extension to create as Attachment to send to printer.', default="zpl")
    dnk_quantities_field_to_show = fields.Selection([
        ('none', 'None'),
        ('just_total', 'Just Total'),
        ('start_and_end', 'Start and End index'),
    ], string='- Quantities field to show', default='just_total')
    dnk_use_default_qty_field_flag = fields.Boolean(string="- Use default qty. field", help='Use default quantity field to print a certain quantity of labels.', default=False)
    dnk_default_qty_field = fields.Many2one(
        comodel_name='ir.model.fields', string='- Default qty. field',
        domain="[('model_id', '=', dnk_model_id), ('ttype', 'in', ['integer', 'float'])]",
        help='Field of the model used for the default quantity of labels to print.')
    dnk_menu_action_name = fields.Char(string='- Menu Action Name', default='Print Labels', help='The action name shown in the Action Menu.')

    _sql_constraints = [
        ('unique_model', 'unique(dnk_model_id)', 'Already exists a Print Label Group with the same Model'),
    ]

    def create_action(self):
        for label_group in self.filtered(lambda record: not record.dnk_action_window_id):
            label_group.dnk_action_window_id = self.env['ir.actions.act_window'].create({
                'name': _(label_group.dnk_menu_action_name),
                'res_model': label_group.dnk_model_id.model,
                'binding_model_id': label_group.dnk_model_id.id,
                'res_model': 'dnk.wizard.print.record.label',
                'view_mode': 'form',
                'target': 'new',
                'binding_type': 'action',
            })

        return True

    def unlink_action(self):
        self.mapped('dnk_action_window_id').unlink()

    @api.onchange('dnk_model_id')
    def onchange_model_id(self):
        self.dnk_default_qty_field = False

    @api.onchange('dnk_ir_ui_view_ids')
    def onchange_ir_ui_view_ids(self):
        # VALIDAR QUE NO SE PUEDA GRABAR SI LA VISTA no es del mismo MODEL y la flag y qweb
        for ir_ui_view in self.dnk_ir_ui_view_ids:
            # Validar que la vista y el grupo de etiquetas contengan el mismo modelo
            if ir_ui_view.model != self.dnk_model_id.model:
                raise ValidationError(_('The model of the \"Printing Label Group\" and the \"Label\" (%s) must be the same.') % (ir_ui_view.name))
            # Validar que la vista contenga el campo type = 'qweb'
            if ir_ui_view.type != 'qweb':
                raise ValidationError(_('The type of the \"Label\" (%s) must be QWeb.') % (ir_ui_view.name))
            # Validar que la vista contenga el campo dnk_label_flag = True
            if ir_ui_view.dnk_label_flag is not True:
                raise ValidationError(_('The flag of the \"Label\" (%s) must be True (Tab \"Label to Print\").') % (ir_ui_view.name))
        return
