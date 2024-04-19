# -*- coding: utf-8 -*-
from odoo import api, fields, models


class DenkerNewProductCost(models.TransientModel):
    _name = "dnk.new.product.cost"
    _description = "Denker New Product Cost"

    dnk_updt_std_cost = fields.Boolean('- Update Dnk Standard Cost', help="Si se marca, actualizará el campo - Denker Standard Cost", default='True')
    dnk_cost_option = fields.Selection([('std_price', 'Costo Promedio'), ('dnk_cost', 'Costo Estándar Dnk')], string="- Opción de Costeo", default='dnk_cost')

    def new_dnk_std_cost(self):
        for rec in self:
            if rec._context['active_model'] == 'product.product':
                products = self.env['product.product'].browse(rec._context['active_ids'])
                for product in products:
                    new_cost = {}
                    new_cost['dnk_product_id'] = False
                    usd_fixed_rate = product.product_tmpl_id.company_id.dnk_usd_cost_fixed_rate or self.env.user.company_id.dnk_usd_cost_fixed_rate
                    new_cost['dnk_labour_cost'] = product.dnk_get_labour_cost()
                    new_cost['dnk_cost_option'] = rec.dnk_cost_option
                    new_cost['dnk_indirect_cost'] = product.dnk_get_indirect_cost()
                    dnk_bom_cost_ids = product.get_dnk_product_boms_cost()
                    if len(dnk_bom_cost_ids) == 1:
                        for dnk_bom_id in dnk_bom_cost_ids:
                            new_cost['dnk_usd_cost_fixed_rate'] = usd_fixed_rate
                            new_cost['dnk_name'] = product.default_code
                            new_cost['dnk_product_id'] = product.id
                            new_cost['dnk_bom_ids'] = product.bom_ids
                            if rec.dnk_cost_option == "std_price":
                                new_cost['dnk_raw_mat_cost'] = dnk_bom_id.dnk_bom_cost
                            else:
                                new_cost['dnk_raw_mat_cost'] = dnk_bom_id.dnk_standard_cost
                            new_cost['dnk_attribute_cost'] = dnk_bom_id.dnk_attribute_cost
                            new_cost['dnk_attr_value_html'] = dnk_bom_id.dnk_attr_value_html
                            new_cost['dnk_move_raws_html'] = dnk_bom_id.dnk_move_raws_html
                            Total = new_cost['dnk_raw_mat_cost'] + new_cost['dnk_labour_cost'] + new_cost['dnk_indirect_cost'] + new_cost['dnk_attribute_cost']
                            new_cost['dnk_total_cost'] = Total
                            product.dnk_raw_mat_cost = new_cost['dnk_raw_mat_cost']
                            product.dnk_labour_cost = new_cost['dnk_labour_cost']
                            product.dnk_indirect_cost = new_cost['dnk_indirect_cost']
                            product.dnk_attribute_cost = new_cost['dnk_attribute_cost']
                            product.dnk_total_cost = Total
                        print("Product_id", new_cost['dnk_product_id'])
                        dnk_cost_id = self.env['dnk.product.cost'].create(new_cost)
                        if rec.dnk_updt_std_cost:
                            product.dnk_standard_cost = product.dnk_total_cost
        return {'type': 'ir.actions.act_window_close'}
