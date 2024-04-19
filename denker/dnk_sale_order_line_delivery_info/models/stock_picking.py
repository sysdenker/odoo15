# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from datetime import datetime


class Picking(models.Model):
    _inherit = "stock.picking"

    @api.depends('move_lines.date_expected')
    def _compute_scheduled_date(self):
        super(Picking, self)._compute_scheduled_date()
        for picking in self:
            for move in picking.move_ids_without_package:
                if move.location_dest_id.usage == 'customer' and move.sale_line_id:
                    # Si cambió la fecha de entrega al cliente
                    if move.date.date() != move.sale_line_id.dnk_expected_date:
                        previous_expected_date = move.sale_line_id.dnk_expected_date
                        move.sale_line_id.dnk_expected_date = move.date.date()

                        msg = _("The scheduled delivery date of product '%s' of has changed, it was updated from %s to %s.<br>Please advise the customer.") % (move.sale_line_id.name, previous_expected_date, move.sale_line_id.dnk_expected_date)
                        move.sale_line_id.order_id.activity_schedule(
                            'mail.mail_activity_data_warning',
                            datetime.today().date(),
                            note=msg,
                            user_id=move.sale_line_id.order_id.user_id.id or SUPERUSER_ID
                        )
