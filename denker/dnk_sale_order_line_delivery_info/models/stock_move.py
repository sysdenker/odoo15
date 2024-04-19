# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from datetime import datetime


class StockMove(models.Model):
    _inherit = "stock.move"

    dnk_availability_date = fields.Date(
        string='- Availability Date',
        help="Availability Date")

    dnk_availability_conf_date = fields.Date(
        string='- Confirmed Availability Date ',
        help="Confirmed Availability Date")

    dnk_conf_availability = fields.Boolean(
        string='- Confirmed Availability',
        help="Confirmed Availability")

    dnk_expedite_date = fields.Date(
        string='- Expedite Date',
        help="Expedite Date")

    dnk_expedite_conf_date = fields.Date(
        string='- Confirmed Expedite Date ',
        help="Confirmed Expedite Date")

    # dnk_expedite_conf = fields.Boolean(
    #    string='- Expedite Confirmed',
    #    help="Expedite Confirmed")



    def write(self, vals):
        res = super(StockMove, self).write(vals)
        for rec in self:
            if "dnk_availability_date" in vals:
                rec._dnk_availability_date()
            if "dnk_availability_conf_date" in vals:
                rec._conf_availability()
            if "dnk_expedite_conf_date" in vals:
                rec._conf_expedite_date()
        return res


    @api.onchange('dnk_availability_conf_date')
    @api.depends('dnk_availability_conf_date')
    def _conf_availability(self):
        for rec in self:
            rec.dnk_conf_availability = True


    @api.onchange('dnk_availability_date')
    @api.depends('dnk_availability_date')
    def _dnk_availability_date(self):
        for rec in self:
            if not rec.dnk_availability_conf_date:
                rec.dnk_availability_conf_date = rec.dnk_availability_date

    @api.onchange('dnk_expedite_conf_date')
    @api.depends('dnk_expedite_conf_date')
    def _conf_expedite_date(self):
        for rec in self:
            rec.dnk_availability_conf_date = rec.dnk_expedite_conf_date
