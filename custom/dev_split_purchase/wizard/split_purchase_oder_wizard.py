# -*- coding: utf-8 -*-
##############################################################################
#
#    DevIntelle Solution(Odoo Expert)
#    Copyright (C) 2015 Devintelle Soluation (<http://devintelle.com/>)
#
##############################################################################

from odoo import api, fields, models, _


class split_order_confirm(models.TransientModel):
    """Split Purchase """
    _name = "split.order.confirm"

    def confirm_purchase(self):
        line_pool = self.env['purchase.order.line']
        purchase_pool = self.env['purchase.order']
        line_ids = self._context.get('active_ids')
        if line_ids:
            purchase = line_pool.browse(line_ids[0]).order_id
            if purchase:
                vals = {
                    'partner_id': purchase.partner_id.id or '',
                    'date_order': purchase.date_order or '',
                    'company_id': purchase.company_id.id or '',
                    'picking_type_id': purchase.picking_type_id.id or '',
                    'state': 'draft',
                    'origin': purchase.name,
                }
                new_purchase_id = purchase_pool.create(vals)
            for line in line_pool.browse(line_ids):
                line.write({'order_id': new_purchase_id.id})
            return {
                'view_mode': 'form',
                'res_id': new_purchase_id.id,
                'res_model': 'purchase.order',
                'view_type': 'form',
                'type': 'ir.actions.act_window',
                'context': self._context,
            }
        return True
