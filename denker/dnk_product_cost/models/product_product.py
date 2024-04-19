# -*- coding: utf-8 -*-
from odoo import models, fields, api


class ProductProduct(models.Model):
    _inherit = "product.product"

    dnk_default_code = fields.Char('- Aging Code', copy=True,  default=lambda self: self.get_dnk_default_code(), help="Se utiliza como código de respaldo para seguimiento de máximos y mínimos")
    dnk_ellc_used = fields.Boolean('- Used in  LLC ', copy=True, help="Se utiliza para reportes en LLC")

    dnk_raw_mat_cost = fields.Float(
        string='- Raw Material Cost', company_dependent=True,
        help="Costo de Materia Prima", digits='Product Price')
    dnk_labour_cost = fields.Float(
        string='- Labour Cost', company_dependent=True,
        digits='Product Price', help="Costo de Mano de Obra")
    dnk_indirect_cost = fields.Float(
        string="- Indirect Cost", company_dependent=True,
        digits='Product Price', help="Gastos Indirectos de Fabricación")
    dnk_attribute_cost = fields.Float(
        string="- Attribute Cost", company_dependent=True,
        digits='Product Price', help="Costo Total de Atributos")
    dnk_standard_cost = fields.Float(
        string="- Denker Standard Cost", company_dependent=True, tracking=True,
        digits='Product Price', help="Costo Estándar para Costeo.")
    dnk_commercial_cost = fields.Float(
        string="- Denker Commercial Cost", company_dependent=True, tracking=True,
        digits='Product Price', help="Costo Comercial para Costeo.")
    dnk_total_cost = fields.Float(string="- Total Cost (USD)", digits='Product Price', company_dependent=True)

    dnk_cost_currency_id = fields.Many2one('res.currency', string='- Denker Cost Currency', related='product_tmpl_id.dnk_cost_currency_id')

    dnk_product_cost_ids = fields.One2many('dnk.product.cost', 'dnk_product_id', string="- Denker Costs (USD)")

    def bttn_new_cost(self):
        view_id = self.env.ref('dnk_product_cost.dnk_view_change_product_cost').id
        context = self._context.copy()
        context['dnk_labour_cost'] = self.dnk_get_labour_cost()
        context['dnk_indirect_cost'] = self.dnk_get_indirect_cost_ids()
        context['dnk_mrp_product_bom_cost'] = self.get_dnk_product_boms_cost()
        return {
            'name': 'Change Product Costs',
            'view_type': 'form',
            'view_mode': 'form',
            'views': [(view_id, 'form')],
            'res_model': 'dnk.product.cost',
            'view_id': view_id,
            'type': 'ir.actions.act_window',
            'target': 'new',
            'context': context,
        }

    @api.depends('default_code')
    @api.onchange('default_code')
    def get_dnk_default_code(self):
        for rec in self:
            rec.dnk_default_code = rec.default_code

    def button_denker_standar_cost(self):
        action_rec = self.env.ref('dnk_product_cost.action_view_change_denker_cost')
        action = action_rec.read([])[0]
        for rec in self:
            prev = rec.dnk_standard_cost
            cost = rec.dnk_total_cost
            action['context'] = {
                'default_dnk_prev_cost': prev,
                'default_dnk_new_cost': cost}
            return action

    def button_denker_commercial_cost(self):
        action_rec = self.env.ref('dnk_product_cost.action_view_update_commercial_cost')
        action = action_rec.read([])[0]
        for rec in self:
            prev = rec.dnk_commercial_cost
            action['context'] = {
                'default_dnk_prev_cost': prev,}
            return action

    @api.model
    def dnk_get_labour_cost(self):
        costo = 0
        dnk_cost_ids = self.product_tmpl_id.dnk_lc_ids
        for costo_man in dnk_cost_ids:
            costo = costo + costo_man.dnk_unit_price_usd * costo_man.dnk_product_labour_minutes_qty
        return costo

    @api.model
    def dnk_get_indirect_cost_ids(self):
        dnk_gifs = []
        for rec in self.product_tmpl_id.dnk_imc_ids:
            dnk_gifs.append(rec.id)
        return dnk_gifs

    @api.model
    def dnk_get_indirect_cost(self):
        for rec in self:
            costos_gif = 0
            for mc in self.product_tmpl_id.dnk_imc_ids:
                if mc.dnk_type == 'unit':
                    costos_gif = costos_gif + mc.dnk_value
                if mc.dnk_type == 'percent':
                    costos_gif = costos_gif + (rec.dnk_raw_mat_cost * mc.dnk_value) / 100
            return costos_gif or False

    @api.model
    def get_dnk_product_boms_cost(self, template_id=False):
        digits = self.env['decimal.precision'].search([('name', '=', 'Product Price')]).digits
        dnk_bom_cost = []

        self.env.cr.execute("DELETE FROM dnk_mrp_bom WHERE dnk_product_id = %s" % self.id)

        boms = self.bom_ids
        for bom in boms:
            product_lines = []
            attributes = []
            html_lc = ""
            html_att = ""
            total_attr_val = 0
            total_min_val = 0

            total_lc_min = 0
            total_lc_val = 0
            for lc_id in self.product_tmpl_id.dnk_lc_ids:
                total_lc_min += lc_id.dnk_product_labour_minutes_qty
                html_lc += "<tr><td align='left'><b>" + lc_id.dnk_product_labour_cost_id.dnk_name + "</b></td>"
                html_lc += "<td align='left'>" + "%0.*f" % (digits, lc_id.dnk_unit_price_usd) + "</td><td>" + str(lc_id.dnk_product_labour_minutes_qty) + "</td>"
                html_lc += "<td align='right'>$" + "%0.*f" % (digits, lc_id.dnk_product_labour_minutes_qty * lc_id.dnk_unit_price_usd) + "</td></tr>"
                total_lc_val += lc_id.dnk_product_labour_minutes_qty * lc_id.dnk_unit_price_usd
            for value in self.product_template_attribute_value_ids:
                attributes += [(value.attribute_id.name, value.name)]

                if (value.product_attribute_value_id.dnk_unit_price_usd and value.product_attribute_value_id.dnk_unit_price_usd > 0) or value.product_attribute_value_id.dnk_product_labour_minutes_qty > 0:
                    total_attr_val += value.product_attribute_value_id.dnk_product_labour_minutes_qty * value.product_attribute_value_id.dnk_unit_price_usd
                    total_min_val += value.product_attribute_value_id.dnk_product_labour_minutes_qty
                    total_att_cost = value.product_attribute_value_id.dnk_product_labour_minutes_qty * value.product_attribute_value_id.dnk_unit_price_usd
                    html_att += "<tr><td align='left'>" + value.name + "</td><td align='left'>$" + "%0.*f" % (digits, value.product_attribute_value_id.dnk_unit_price_usd) + "</td>"
                    html_att += "<td>" + str(value.product_attribute_value_id.dnk_product_labour_minutes_qty) + " </td><td align='right'>$" + "%0.*f" % (digits, total_att_cost) + "</td></tr>"

            # total_att = "<tr style ='background-color: #cccccc;'><td colspan='2' align='left'><b>Total: <b/></td><td><b>"
            # total_att += "%0.*f" % (digits, total_min_val + total_lc_min) + " </b></td><td align='right'><b>$"
            # total_att += "%0.*f" % (digits, total_attr_val + total_lc_val) + "</b></td></tr>"
            html_head_lc = "<thead><tr><td><b></b></td><td>Unit Price(USD).</td><td>Time (<b>min.</b>):</td><td align='right'>Cost (<b>USD</b>):</td></tr>"
            html_head_lc += "<tr style ='background-color: #cccccc;' ><td colspan='2' ><b>Labor Cost:</b></td>"
            html_head_lc += "<td align='left'><b> %0.*f" % (digits, total_lc_min) + "</b></td>"
            html_head_lc += "<td align='right'><b> %0.*f" % (digits, total_lc_val) + "</b></td></tr></thead>"
            html_head_att = "<thead><tr style ='background-color: #cccccc;' ><td colspan = '2'><b>Labor Attributes Cost:</b></td>"
            html_head_att += "<td align='left'><b> %0.*f" % (digits, total_min_val) + "</b></td>"
            html_head_att += "<td align='right'><b> %0.*f" % (digits, total_attr_val) + "</b></td></tr></thead>"
            html_att = "<table width='100%'class='table table-condensed' >" + html_head_lc + html_lc + html_head_att + html_att + "</table>" if total_attr_val or total_lc_min > 0 else False

            result, result2 = bom.explode(self, 1)
            move_raws_html = "<table class='o_list_view table table-condensed table-striped o_list_view_ungrouped'>"
            move_raws_html += "<tr style ='background-color: #cccccc;'><td align='left'><b>Product</b></td><td  align='right'><b>Unit Of Measure</b></td>"
            move_raws_html += "<td  align='right'>To Consume</td><td  align='right'><b>Costo Prom.(USD)</b></td><td  align='right'><b>Costo Estándar Dnk(USD)</b></td></tr>"

            total = 0.0
            total_dnk_std_cost = 0.0
            for bom_line, line_data in result2:
                price_uom = bom_line.product_id.uom_id._compute_price(bom_line.product_id.standard_price, bom_line.product_uom_id)
                dnk_std_cost = bom_line.product_id.dnk_standard_cost
                dnk_price_uom = bom_line.product_id.uom_id._compute_price(dnk_std_cost, bom_line.product_uom_id)
                line = {
                    'product_id': bom_line.product_id,
                    'product_uom_qty': line_data['qty'],  # line_data needed for phantom bom explosion
                    'product_uom': bom_line.product_uom_id,
                    'price_unit': price_uom,
                    'dnk_standard_cost': dnk_std_cost,
                    'total_price': price_uom * line_data['qty'],
                    'total_std_cost': dnk_price_uom * line_data['qty'],
                }
                move_raws_html += "<tr><td>" + bom_line.product_id.name
                move_raws_html += "</td><td align='right'>"
                move_raws_html += bom_line.product_uom_id.name
                move_raws_html += "</td><td align='right'>" + str(line_data['qty'])
                move_raws_html += "</td><td align='right'>" + "%0.*f" % (digits, line['total_price'] / self.env.user.company_id.dnk_usd_cost_fixed_rate) + "</td>"
                move_raws_html += "</td><td align='right'>" + "%0.*f" % (digits, line['total_std_cost']) + "</td></tr>"
                total += line['total_price']
                total_dnk_std_cost += line['total_std_cost']

            move_raws_html += "<tr  style ='background-color: #cccccc;'><td colspan=3  align='left'><b>Total USD: </b> </td>"
            move_raws_html += "<td align='right'><b>" + "%0.*f" % (digits, total / self.env.user.company_id.dnk_usd_cost_fixed_rate) + "</b></td>"
            move_raws_html += "<td align='right'><b>" + "%0.*f" % (digits, total_dnk_std_cost) + "</b></td></tr>"
            move_raws_html += "</table>"

            # move_raws_html += "<tr><td colspan=3  align='left'><b>Total USD: </td><td align='right'>" + "%0.*f" % (digits, total / self.env.user.company_id.dnk_usd_cost_fixed_rate) + "</b></td><tr>"
            # move_raws_html += "</table>"

            move_raws_html += "</table>"

            dnk_bom_cost = self.env['dnk.mrp.bom'].create({
                'dnk_product_id': self.id,
                'dnk_bom_id': bom.id,
                'dnk_attribute_cost': total_attr_val,
                'dnk_attr_value_html': html_att,
                'dnk_move_raws_html': move_raws_html,
                'name': bom.code,
                'dnk_usd_cost_fixed_rate': self.env.user.company_id.dnk_usd_cost_fixed_rate,
                'dnk_bom_cost': (total) / self.env.user.company_id.dnk_usd_cost_fixed_rate,
                'dnk_standard_cost': total_dnk_std_cost})
        return dnk_bom_cost
