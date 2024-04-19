# -*- coding: utf-8 -*-
from odoo import api, fields, models


class DenkerNewProductCost(models.TransientModel):
    _name = "dnk.account.move.wizard"
    _description = "Denker Update Account Move Wizard"


    dnk_company_id = fields.Many2one(comodel_name='res.company', string='Company',
                                 default=lambda self: self.env.company)
    dnk_invoice_option = fields.Selection(selection=[
        ('invoice_date', 'Invoice Date'),
        ('state', 'State'),
        ('accounting_date', 'Accounting Date'),
        ('delivery_address', 'Delivery Address'),
        ('invoice_date_due', 'Invoice Due Date'),
        ('invoice_payment_term_id', 'Due Date')], default="invoice_date")
    dnk_invoice_date = fields.Date('- New Invoice Date', help="Esta Fecha quedará registrada en todos los registros seleccionados")
    dnk_state = fields.Selection(selection=[
        ('draft', 'Draft'),
        ('posted', 'Posted'),
        ('cancel', 'Cancel'),], default="draft", string="Estatus Temporal para edición")
    dnk_accounting_date = fields.Date('- New Invoice Date', help="Esta Fecha quedará registrada en todos los registros seleccionados")
    dnk_invoice_date_due = fields.Date('- New Invoice Due Date', help="Esta Fecha quedará registrada en todos los registros seleccionados")
    dnk_invoice_payment_term_id = fields.Many2one('account.payment.term', string='- New Payment Terms',
        domain="['|', ('company_id', '=', False), ('company_id', '=', dnk_company_id)]")
    dnk_partner_shipping_id = fields.Many2one('res.partner', string='- Delivery Address',
        domain="['|', ('company_id', '=', False), ('company_id', '=', dnk_company_id)]")


    def _compute_company_id(self):
        for move in self:
            move.dnk_company_id = self.env.user.company_id

    def update_move_wizard(self):
        for rec in self:
            if rec._context['active_model'] == 'account.move':
                Moves = self.env['account.move'].browse(rec._context['active_ids'])
                for move in Moves:
                    if rec.dnk_invoice_option == 'state':
                        move.state = rec.dnk_state
                    if rec.dnk_invoice_option == 'invoice_date':
                        move.invoice_date = rec.dnk_invoice_date
                    if rec.dnk_invoice_option == 'accounting_date':
                        move.date = rec.dnk_accounting_date
                    if rec.dnk_invoice_option == 'delivery_address':
                        move.partner_shipping_id = rec.dnk_partner_shipping_id
                    if rec.dnk_invoice_option == 'invoice_payment_term_id':
                        move.invoice_payment_term_id = rec.dnk_invoice_payment_term_id
                    if rec.dnk_invoice_option == 'invoice_date_due':
                        move.invoice_date_due = rec.dnk_invoice_date_due

        return {'type': 'ir.actions.act_window_close'}
