# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError, RedirectWarning, ValidationError
import os


class PurchaseOrderFile(models.Model):
    _inherit = ['sale.order']

    #_sql_constraints = [('dnk_purchase_order_name', 'unique (dnk_purchase_order_name,company_id)',
    #                     'Duplicate records in Customer Reference not allowed!')]

    dnk_purchase_order_name = fields.Char('- Purchase Order Name')
    dnk_purchase_order_file = fields.Binary('- Purchase Order File', store=True)
    dnk_po_file_count = fields.Integer(
        string='- Purchase Order Count', compute='po_file_count',
        readonly=True, help = "Cuenta de archivos que tienen el mismo nombre")

    def po_file_count(self):
        for sale in self:
            sale.dnk_po_file_count = 0
            if sale.dnk_purchase_order_name:
                POs = self.env['sale.order'].search(
                    [('dnk_purchase_order_name','=',sale.dnk_purchase_order_name),
                    ('company_id','=',self.company_id.id)])
                sale.dnk_po_file_count = len(POs)

    @api.onchange('dnk_purchase_order_name')
    def update_client_order_ref(self):
        for sale in self:
            if sale.dnk_purchase_order_name:
                sale.client_order_ref = os.path.splitext(sale.dnk_purchase_order_name)[0].upper()

    def action_confirm(self):
        if not self.website_id and self.partner_id.dnk_purchase_order_required and not self.dnk_purchase_order_name:
            raise ValidationError(_('This customer requires a Purchase Order file.'))
        res = super(PurchaseOrderFile, self).action_confirm()
        return res
