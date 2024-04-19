# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class DnkCostDiffReasin(models.Model):
    _name = 'dnk.reason.difference.cost'
    _description = 'Reason for Difference in Cost '
    _rec_name = 'name'
    _order = 'name, id'

    name = fields.Char('- Name', index=True, readonly=False, required=True, translate=True)
    sequence = fields.Integer('- Sequence')
    company_id = fields.Many2one(
        'res.company', string='- Company')


class DnkMrpValidation(models.TransientModel):
    _name = 'dnk.mrp.cost.val'
    _description = 'Dnk Mrp Cost Validation'

    dnk_mo_id = fields.Many2one('mrp.production', '- Manufacturing Order', ondelete='cascade')
    dnk_price = fields.Float(digits="Account", string="- Mo Cost")
    dnk_to_consume = fields.Float(digits="Account", string="- Average Cost")
    dnk_alow_cost_diff = fields.Float('- Porcentaje', digits=(3, 2), help='In Manufacturing Orders, Percentage Allowed')
    dnk_option = fields.Selection([('mark_done', 'Mark As Done'), ('post_inventory', 'Post Inventory')], string="- Opción", default='mark_done')
    dnk_reason_diff_cost = fields.Many2one('dnk.reason.difference.cost', '- Reason Cost Variation', ondelete='cascade')
    dnk_restricted = fields.Boolean('- Validation')

    # Cuando se active la alerta, mostrar un nuevo campo many2one que tendrá el motivo de la diferencia en el costo.
    # Se creará modelo nuevo para agregar los motivos, campo obligatorio.
    # Para cada producto terminado.  actualizar ese motivo y el porcentaje de "eficiencia", en post inventory, en cada producto terminado nuevo-
    # y en marck as done,  primero  mando llamar super, actualizo productos terminados y ya luego regreso super-
    # Agregar la moneda a los campos de Average cost y Mo Cost.


    def button_mark_done(self):
        for rec in self:
            rec.dnk_mo_id.dnk_validation = False
            rec.dnk_mo_id.dnk_reason_diff_cost = rec.dnk_reason_diff_cost
            if rec.dnk_to_consume == 0:
                rec.dnk_mo_id.dnk_diff_cost_prc = 0
            else:
                rec.dnk_mo_id.dnk_diff_cost_prc = rec.dnk_price / rec.dnk_to_consume
            rec.dnk_mo_id.button_mark_done()

    def post_inventory(self):
        for rec in self:
            rec.dnk_mo_id.dnk_validation = False
            rec.dnk_mo_id.dnk_reason_diff_cost = rec.dnk_reason_diff_cost
            if rec.dnk_to_consume == 0:
                rec.dnk_mo_id.dnk_diff_cost_prc = 0
            else:
                rec.dnk_mo_id.dnk_diff_cost_prc = rec.dnk_price / rec.dnk_to_consume
            rec.dnk_mo_id.post_inventory()
