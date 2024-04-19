# -*- coding: utf-8 -*-
from odoo import api, fields, models


class DnkModMRPProd(models.TransientModel):
    _name = "dnk.mrp.production.pdate.wizard"
    _description = "Denker Update Planned Date Wizard"

    dnk_planned_date = fields.Datetime('- New Planned Date', help="Esta Fecha quedará registrada en todos los registros seleccionados")

    def dnk_mrp_planned_date_wizard(self):
        for rec in self:
            if rec._context['active_model'] == 'mrp.production':
                Moves = self.env['mrp.production'].browse(rec._context['active_ids'])
                for move in Moves:
                    self._cr.execute("UPDATE mrp_production SET date_planned_start = %s WHERE id = %s ", (rec.dnk_planned_date.strftime("%Y-%m-%d, %H:%M:%S"),move.id))
                    # move.date_planned_start = rec.dnk_planned_date
                    StockMoves = self.env['stock.move'].search([('reference', '=', move.name)])
                    for smove in StockMoves:
                        smove.date = rec.dnk_planned_date.strftime("%Y-%m-%d %H:%M:%S")
                        StockMovesLines = self.env['stock.move.line'].search([('move_id', '=', smove.id)])
                        for moveline in StockMovesLines:
                            moveline.date = rec.dnk_planned_date.strftime("%Y-%m-%d %H:%M:%S")



        return {'type': 'ir.actions.act_window_close'}
