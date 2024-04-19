# -*- coding: utf-8 -*-

from odoo import fields, models, _
from odoo.exceptions import UserError
import base64


class DnkQualityPointWizard(models.TransientModel):
    _name = 'dnk.quality.point.wiz'
    _description = 'Dnk Quality Point Wizard'

    # dnk_product_id = fields.Many2one('product.product', '- Product', ondelete='cascade')
    dnk_qp_name = fields.Char('- File Name')
    dnk_qp_file = fields.Binary('- File', store=True)
    dnk_tolerance_min = fields.Float('- Min Tolerance', digits='Quality Tests', default=0.0)
    dnk_tolerance_max = fields.Float('- Max Tolerance', digits='Quality Tests', default=1.0)
    dnk_norm = fields.Float('- Norm', digits='Quality Tests', default=0.0)  # TDE RENAME ?
    dnk_norm_unit = fields.Char('- Norm Unit', default=lambda self: 'Ω ohm')  # TDE RENAME ?

    def attach_file(self, producto):
        if producto:
            att_params = []
            att_params.append(('res_model', '=', 'product.template'))
            att_params.append(('name', '=', self.dnk_qp_name))
            att_params.append(('res_id', '=', producto.product_tmpl_id.id))
            search_attachment = self.env['ir.attachment'].sudo().search(att_params)
            if not search_attachment:
                att_data = {
                    'name': self.dnk_qp_name,
                    'type': 'binary',
                    # 'datas': base64.encodestring(self.dnk_qp_file),
                    'datas': self.dnk_qp_file,
                    'res_model': 'product.template',
                    'res_id': producto.product_tmpl_id.id
                }
                attachment_id = self.env['ir.attachment'].create(att_data)
                return attachment_id
            else:
                # search_attachment.datas = base64.encodestring(self.dnk_qp_file)
                search_attachment.datas = self.dnk_qp_file
                return search_attachment

    def create_quality_point(self):
        for rec in self:
            if rec._context['active_model'] == 'product.product':
                Productos = self.env['product.product'].browse(rec._context['active_ids'])
                for producto in Productos:
                    operation_id = False
                    picking_type_id = False
                    for bom in producto.bom_ids:
                        if bom.operation_ids:
                            for op in bom.operation_ids:
                                if "COSTURA" in op.name.upper():
                                    operation_id = op.id
                                    picking_type_id = bom.picking_type_id
                                    break
                        break
                    attachment = self.attach_file(producto)
                    params = []
                    params.append(('product_ids', 'in', producto.id))
                    qp_ids = self.env['quality.point'].sudo().search(params)
                    # print("qp_ids", qp_ids)
                    for qp in qp_ids:
                        # print("hay qp", qp)
                        qp.note = '<p><img src="/web/image/{0}/{1}" class="pull-left" style="width: 100%;"></p>'.format(attachment.id, attachment.name)
                        qp.norm = self.dnk_norm or 0.00
                        qp.norm_unit = self.dnk_norm_unit or 'Ω ohm'
                        qp.tolerance_min = self.dnk_tolerance_min or 0.00
                        qp.tolerance_max = self.dnk_tolerance_max or 1.00

                    if not qp_ids:
                        # print("NO hay qp_ids")
                        data = {
                            'title': 'Revisión Calidad Empaque Producción',
                            'product_ids': Productos,
                            # 'product_tmpl_id': producto.product_tmpl_id.id,
                            'picking_type_ids': picking_type_id,
                            'operation_id': operation_id,
                            'company_id': 1,
                            'test_type_id': 2,
                            'team_id': 1,
                            'measure_frequency_type': 'all',
                            'tolerance_min': self.dnk_tolerance_min or 0.00,
                            'tolerance_max': self.dnk_tolerance_max or 1.00,
                            'norm': self.dnk_norm or 0.00,
                            'norm_unit': self.dnk_norm_unit or 'Ω ohm',
                            'note': '<p><img src="/web/image/{0}/{1}" class="pull-left" style="width: 100%;"></p>'.format(attachment.id, attachment.name),
                        }
                        dnk_qp_id = self.env['quality.point'].create(data)
                        # print("dnk_qp_id", dnk_qp_id)
                    # raise UserError(_("Mi error a propósito"))
        return False

    def create_quality_point_ant(self, Productos):

        if Productos:
            # Adjunto
            for producto_uno in Productos:
                producto = producto_uno
                continue
            operation_id = False
            picking_type_id = False
            if producto:
                if producto.bom_ids:
                    for bom in producto.bom_ids:
                        if bom.operation_ids:
                            for op in bom.operation_ids:
                                if "COSTURA" in op.name.upper():
                                    operation_id = op.id
                                    picking_type_id = bom.picking_type_id
                                    break
                        break
                attachment = self.attach_file(producto)
            # if attachment:
                # print("")

            # prefijo = producto.default_code[:4]
            # if prefijo == 'ESM-':
            #    picking_type_id = [37]
            #    operation_id = 732# 84
            # Guarda
            # elif prefijo == 'EHS-':
            #    picking_type_id = [37]
            #    operation_id = 732
            # Overol
            # elif prefijo == 'EOV-':
            #    picking_type_id = [128]
            #    operation_id = 732
            # Prenda
            # elif prefijo == 'EGR-':
            #    picking_type_id = [129]
            #    operation_id = 732
            # Talon era
            # elif prefijo == 'EHL-':
            #    picking_type_id = [24]
            #    operation_id = 74
            params = []
            params.append(('product_ids', 'in', producto.id))
            qp_ids = self.env['quality.point'].sudo().search(params)
            # print("qp_ids", qp_ids)
            for qp in qp_ids:
                # print("hay qp", qp)
                qp.note = '<p><img src="/web/image/{0}/{1}" class="pull-left" style="width: 100%;"></p>'.format(attachment.id, attachment.name)
                qp.norm = self.dnk_norm or 0.00
                qp.norm_unit = self.dnk_norm_unit or 'Ω ohm'
                qp.tolerance_min = self.dnk_tolerance_min or 0.00
                qp.tolerance_max = self.dnk_tolerance_max or 1.00

            if not qp_ids:
                # print("NO hay qp_ids")
                data = {
                    'title': 'Revisión Calidad Empaque Producción',
                    'product_ids': Productos,
                    # 'product_tmpl_id': producto.product_tmpl_id.id,
                    'picking_type_ids': picking_type_id,
                    'operation_id': operation_id,
                    'company_id': 1,
                    'test_type_id': 2,
                    'team_id': 1,
                    'measure_frequency_type': 'all',
                    'tolerance_min': self.dnk_tolerance_min or 0.00,
                    'tolerance_max': self.dnk_tolerance_max or 1.00,
                    'norm': self.dnk_norm or 0.00,
                    'norm_unit': self.dnk_norm_unit or 'Ω ohm',
                    'note': '<p><img src="/web/image/{0}/{1}" class="pull-left" style="width: 100%;"></p>'.format(attachment.id, attachment.name),
                }
                dnk_qp_id = self.env['quality.point'].create(data)
                # print("dnk_qp_id", dnk_qp_id)
            # raise UserError(_("Mi error a propósito"))
        return False

    def button_create_qp_ant(self):
        for rec in self:
            product_internal_code = rec.dnk_qp_name[8:-4].replace('_', '|').replace('X', '_').replace('|', '\\_')
            params = []
            params.append(('default_code', '=like', product_internal_code))
            # print(product_internal_code)
            Productos = self.env['product.product'].sudo().search(params)
            # print(Productos)
            raise UserError(_("Mi error a propósito"))
            # rec.create_quality_point(Productos)
            # raise UserError(_("Mi error a propósito"))
            # for producto in Productos:
            #    quality_point_id = rec.create_quality_point(producto)
                # return False
                # raise UserError(_("Mi error a propósito"))

        return False


    def button_create_qp(self):
        for rec in self:
            rec.create_quality_point()

        return False
