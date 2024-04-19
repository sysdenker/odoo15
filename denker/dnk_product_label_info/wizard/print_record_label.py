# -*- coding: utf-8 -*-

from odoo import models, api, fields


class PrintRecordLabel(models.TransientModel):
    _inherit = 'dnk.wizard.print.record.label'

    def _default_label_id(self):
        # Automatically select the label, if only one is available
        if self.env.context.get('active_model') == 'mrp.production':
            ui_view_ids = []
            mpr_production = self.env[self.env.context.get('active_model')].browse(self.env.context.get('active_id'))
            print(mpr_production)
            if mpr_production.product_id.dnk_ir_ui_view_ids:
                self.onchange_active_model()
                return mpr_production.product_id.dnk_ir_ui_view_ids[0].id
        else:
            return super(PrintRecordLabel, self)._default_label_id()

    dnk_label_id = fields.Many2one(
        comodel_name='ir.ui.view', string='- Label', required=True, ondelete='cascade',
        domain="[('dnk_label_flag', '=', True),('dnk_label_group_id', '=', dnk_label_group_id),('model', '=', active_model)]",
        help='Label to print.', default=_default_label_id)

    @api.onchange('dnk_label_id')
    def onchange_active_model(self):
        if self.env.context.get('active_model') == 'mrp.production':
            ui_view_ids = []
            mpr_production = self.env[self.env.context.get('active_model')].browse(self.env.context.get('active_id'))
            for ui_view_id in mpr_production.product_id.dnk_ir_ui_view_ids:
                ui_view_ids.append(ui_view_id.id)

            # Si el producto no tiene ninguna etiqueta autorizada, no mostrar ninguna
            domain = [('id', 'in', ui_view_ids)]

            # Código por si se quiere modificar a que si el producto no tiene ninguna etiqueta, mostrar todas, NO ELIMINAR
            # if ui_view_ids:
            #    domain = [('id', 'in', ui_view_ids)]
            # else:
            #    label_group = self.env['printing.label.group'].search([
            #        ('dnk_model_id.model', '=', self.env.context.get('active_model')),
            #    ], limit=1)
            #    domain = [('dnk_label_flag', '=', True), ('dnk_label_group_id', '=', label_group.id), ('model', '=', self.env.context.get('active_model'))]

            return {'domain': {'dnk_label_id': domain}}
