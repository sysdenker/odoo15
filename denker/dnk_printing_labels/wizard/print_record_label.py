# -*- coding: utf-8 -*-
# See LICENSE file for full copyright and licensing details.

from odoo import models, api, fields, _
import base64
import datetime
from types import *
import math
from odoo.exceptions import UserError


class PrintRecordLabel(models.TransientModel):
    _name = 'dnk.wizard.print.record.label'
    _description = 'Print Record Label'

    def _default_label_id(self):
        # Automatically select the label, if only one is available
        label_group_id = self.env['dnk.printing.label.group'].search([
            ('dnk_model_id.model', '=', self.env.context.get('active_model')),
        ], limit=1)
        record = self.env[self.env.context.get('active_model')].browse(self.env.context.get('active_id'))

        if label_group_id:
            if label_group_id.dnk_ir_ui_view_ids:
                return label_group_id.dnk_ir_ui_view_ids[0].id

    dnk_label_group_id = fields.Many2one(
        'dnk.printing.label.group',
        string='- Label Group Id', readonly=True,
        help='Label Group Id.')

    dnk_active_model = fields.Char(
        string='- Active Model', readonly=True,
        default=lambda self: self.env.context.get('active_model'))

    dnk_label_id = fields.Many2one(
        comodel_name='ir.ui.view', string='- Label', required=True, ondelete='cascade',
        domain="[('dnk_label_flag', '=', True), ('dnk_label_group_id', '=', dnk_label_group_id), ('model', '=', active_model)]",
        help='Label to print.', default=_default_label_id)

    dnk_labels_to_print_index_start = fields.Integer(
        string='- Index Start', default=1,
        help='An integer number specifying at which label index to start to print. Default is 1')

    dnk_labels_to_print_index_stop = fields.Integer(
        string='- Index Stop', default=1,
        help='An integer number specifying at which label index to stop to print.')

    dnk_labels_to_print_qty = fields.Integer('- Quantity to Print', default=1, help='Quantity of lables to print.')

    dnk_quantities_field_to_show = fields.Selection(
        [
            ('none', 'None'),
            ('just_total', 'Just Total'),
            ('start_and_end', 'Start and End index'),
        ], string='- Quantities field to show', readonly=True)

    @api.model
    def default_get(self, fields_list):
        values = super(PrintRecordLabel, self).default_get(fields_list)

        # Automatically select the label, if only one is available
        label_group_id = self.env['dnk.printing.label.group'].search([
            ('dnk_model_id.model', '=', self.env.context.get('active_model')),
        ], limit=1)

        if label_group_id:
            values['dnk_label_group_id'] = label_group_id.id
            values['dnk_quantities_field_to_show'] = label_group_id.dnk_quantities_field_to_show
            # if label_group.dnk_ir_ui_view_ids:
            #    values['label_id'] = label_group.dnk_ir_ui_view_ids[0].id

        # Si el grupo de etiquetas tiene activado la bandera de "campo de cantidad por defecto"
        if label_group_id.dnk_use_default_qty_field_flag:
            record = self.env[self.env.context.get('active_model')].browse(self.env.context.get('active_id'))
            values['dnk_labels_to_print_index_stop'] = math.ceil(record[label_group_id.dnk_default_qty_field.name])
            values['dnk_labels_to_print_qty'] = values['dnk_labels_to_print_index_stop']

        return values

    def print_label(self):
        """ Prints a label per selected record """
        record_model = self.env.context['active_model']

        if self.dnk_labels_to_print_index_stop < self.dnk_labels_to_print_index_start:
            raise UserError(_('The "Index Start" must be smaller or equal to "Index Stop".'))

        for record_id in self.env.context['active_ids']:
            # Automatically select the label, if only one is available
            label_group = self.env['dnk.printing.label.group'].search([
                ('dnk_model_id.model', '=', self.env.context.get('active_model')),
            ], limit=1)










            if label_group:
                view_id = self.dnk_label_id.id

                record = self.env[record_model].browse(record_id)

                # Creación de paquetes con la cantidad a imprimir, Se crearán paquetes con la cantidad que contengan las etiquetas
                # para que el contador aumente por la cantidad del paquete.
                if record_model == 'mrp.workorder':

                    product = record.product_id
                    wo_qty = record.qty_production
                    print_qty = self.dnk_labels_to_print_qty
                    res_qty = wo_qty % print_qty or False


                    if res_qty:
                        pqty_2 = self.env['product.packaging'].search_read([('product_id', '=', product.id), ('qty', '=', res_qty)])
                        if not pqty_2:
                            self.env['product.packaging'].create({
                                'name': product.barcode + "-" + str(int(res_qty)),
                                'qty': res_qty,
                                'product_id': product.id,
                                'barcode': product.barcode + "-" + str(int(res_qty))
                                })
                    pqty_1 = self.env['product.packaging'].search_read([('product_id', '=', product.id), ('qty', '=', print_qty)])
                    if not pqty_1:
                        self.env['product.packaging'].create({
                            'name': product.barcode + "-" + str(print_qty),
                            'qty': print_qty,
                            'product_id': product.id,
                            'barcode': product.barcode + "-" + str(print_qty)
                            })




                self.env[record_model].search_read([('id', '=', view_id)], ['id', 'name'])

                # Agregar en la etiqueta lo siguiente si es en lenguaje zpl:
                # Repetir la etiqueta N veces
                # ^PQ<t t-esc="labels_to_print_index_stop"/>,0,1,Y
                values = {
                    'record': record,
                    'dnk_labels_to_print_index_start': self.dnk_labels_to_print_index_start,
                    'dnk_labels_to_print_index_stop': self.dnk_labels_to_print_index_stop,
                    'dnk_labels_to_print_qty': self.dnk_labels_to_print_qty,
                }

                label_txt = self.env['ir.ui.view'].browse(view_id)._render(values=values, engine='ir.qweb')

                # Convertir a Base64
                b64_txt = base64.b64encode(label_txt.encode())

                # Save txt as attachment
                texttime = fields.Datetime.context_timestamp(self, timestamp=datetime.datetime.now()).strftime('%Y%m%d%H%M%S')
                file_extension = label_group.dnk_script_file_extension
                attachment_name = texttime + "-labels." + file_extension

                return self.env['ir.attachment'].create({
                    'name': attachment_name,
                    'type': 'binary',
                    'datas': b64_txt,
                    'store_fname': attachment_name,
                    'res_model': record_model,
                    'res_id': record_id,
                    'mimetype': 'text/plain'
                })
