# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError, RedirectWarning, ValidationError
import logging
import os


_logger = logging.getLogger(__name__)


class AccountMove(models.Model):
    _inherit = ['account.move']

    dnk_purchase_order_name = fields.Char('- Purchase Order Name', related='dnk_order_id.dnk_purchase_order_name')
    dnk_purchase_order_file = fields.Binary(
        string='- Purchase Order File',
        related='dnk_order_id.dnk_purchase_order_file',
        readonly=True, store=False)

    @api.onchange('dnk_purchase_order_name')
    def update_name_ref(self):
        for account in self:
            if account.dnk_purchase_order_name:
                account.name = os.path.splitext(account.dnk_purchase_order_name)[0].upper()


class MailComposerToAttachPurchaseOrder(models.TransientModel):
    _inherit = ['mail.compose.message']

    def _onchange_template_id(self, template_id, composition_mode, model, res_id):
        if model == 'account.move':
            Attachments = self.env['ir.attachment']
            Invoice = self.env['account.move'].search([('id', '=', res_id)])
            if Invoice.move_type == 'out_invoice' and not Invoice.website_id and Invoice.partner_id.dnk_attach_purchase_order and not Invoice.dnk_purchase_order_file :
                raise ValidationError(_('The settings for this client requires a purchase order file.'))
            if Invoice.move_type == 'out_invoice' and not Invoice.website_id and Invoice.partner_id.dnk_attach_purchase_order and Invoice.dnk_purchase_order_file and Invoice.dnk_purchase_order_name:
                # Busco si ya tengo adjunto, si no, lo creo
                PurchaseOrder = self.env['ir.attachment'].search([('res_id', '=', Invoice.id), ('name', '=', Invoice.dnk_purchase_order_name), ('res_model', '=', model)], limit=1, order="id desc")
                if not PurchaseOrder:
                    order_attachment_vals = {
                        'name': Invoice.dnk_purchase_order_name,
                        'res_id': Invoice.id,
                        'datas': Invoice.dnk_purchase_order_file,
                        'res_model': model,
                        'type': 'binary'}
                    try:
                        PurchaseOrder = self.env['ir.attachment'].create(order_attachment_vals)
                    except AccessError:
                        _logger.info("Cannot save Purchase Order %r as attachment", order_attachment_vals['name'])
                        raise ValidationError(_('The settings for this client requires a purchase order file.'))
                    else:
                        _logger.info('The Purchase Order %s is now saved in the database', order_attachment_vals['name'])
                if PurchaseOrder:
                    res = super(MailComposerToAttachPurchaseOrder, self)._onchange_template_id(template_id, composition_mode, model, res_id)
                    res['value']['attachment_ids'][0][2].append(PurchaseOrder.id)
                    return res
        res = super(MailComposerToAttachPurchaseOrder, self)._onchange_template_id(template_id, composition_mode, model, res_id)
        return res
