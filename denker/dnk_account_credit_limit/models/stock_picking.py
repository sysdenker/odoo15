# -*- coding: utf-8 -*-
from odoo import models, fields, api, exceptions, _
from datetime import datetime, date, time, timedelta
import calendar


class CreditLimitStockPicking(models.Model):
    _name = "stock.picking"
    _inherit = 'stock.picking'

    dnk_allow_delivery = fields.Boolean('- Allow Delivery?', help='Allow delivery with overdue invoices', default=False)

    def button_validate(self):
        for rec in self:
            companies = self.env['res.company'].sudo().search([]).partner_id
            if rec.partner_id not in companies or (rec.partner_id.parent_id and rec.partner_id.parent_id not in companies):
                if not(rec.partner_id.parent_id and rec.partner_id.parent_id.dnk_credit_policy) and not rec.partner_id.dnk_credit_policy:
                    if rec.picking_type_code == 'outgoing' and not rec.dnk_allow_delivery:
                        current_date = date.today() - timedelta(days=15)
                        params = []
                        partner_ids = ()
                        if rec.partner_id.parent_id:
                            partner_ids = partner_ids + (rec.partner_id.parent_id.id,)
                            for child in rec.partner_id.parent_id.child_ids:
                                partner_ids = partner_ids + (child.id,)
                            params.append(('partner_id', 'in', partner_ids))
                        else:
                            partner_ids = partner_ids + (rec.partner_id.id,)
                            for child in rec.partner_id.child_ids:
                                partner_ids = partner_ids + (child.id,)
                            params.append(('partner_id', 'in', partner_ids))
                        params.append(('move_type', '=', 'out_invoice'))
                        params.append(('state', '=', 'posted'))
                        params.append(('invoice_date_due', '<=', str(current_date)))
                        Invoices = rec.env['account.move'].sudo().search(params)
                        if Invoices:
                            raise exceptions.ValidationError('Customer has overdue invoices.')
            res = super(CreditLimitStockPicking, self).button_validate()
            return res
