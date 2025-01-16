# -*- coding: utf-8 -*-
from odoo import api, fields, models


class DenkerNewProductCost(models.TransientModel):
    _name = "dnk.account.move.line.wizard"
    _description = "Denker Update Account Move Line Wizard"

    dnk_company_id = fields.Many2one(comodel_name='res.company', string='Company',
                                 default=lambda self: self.env.company)
    dnk_invoice_option = fields.Selection(selection=[
        ('account_id', '- Account'),('date', '- Date'), ('tax', '- Taxes')], default="account_id")
    dnk_account_id = fields.Many2one('account.account', '- Account', ondelete='cascade')
    dnk_date = fields.Date('- New Invoice Date', help="Esta Fecha quedará registrada en todos los registros seleccionados")
    dnk_tax_ids = fields.Many2many("account.tax", string='- New Taxes', help="Estos tax se agregarán a las líneas")

    def _compute_company_id(self):
        for move in self:
            move.dnk_company_id = self.env.user.company_id

    def update_move_line_wizard(self):
        for rec in self:
            if rec._context['active_model'] == 'account.move.line':
                Moves = self.env['account.move.line'].browse(rec._context['active_ids'])
                for move in Moves:
                    if rec.dnk_invoice_option == 'account_id':
                        move.account_id = rec.dnk_account_id
                    if rec.dnk_invoice_option == 'date':
                        
                        
                        if move.move_id.state == 'posted':
                            self._cr.execute("UPDATE account_move_line SET date = %s WHERE id = %s ", (rec.dnk_date.strftime("%Y-%m-%d"),move.id))
                           
                            # move.move_id.state = 'draft'
                            # move.date = rec.dnk_date
                            # move.move_id.state = 'posted'
                        else:
                            move.date = rec.dnk_date
                    if rec.dnk_invoice_option == 'tax':
                        if move.move_id.state == 'posted':
                            move.move_id.state = 'draft'
                            move.tax_ids = rec.dnk_tax_ids
                            move.move_id.state = 'posted'
                        else:
                            move.tax_ids = rec.dnk_tax_ids

        return {'type': 'ir.actions.act_window_close'}
