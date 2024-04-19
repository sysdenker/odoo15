# -*- coding: utf-8 -*-
from odoo import api, fields, models, tools, _


class IndirectManufacturingCost(models.Model):
    _name = 'dnk.indirect.manufacturing.cost'
    _description = 'Indirect Manufacturing Costs (GIF Gastos Indirectos de Fabricación)'
    _rec_name = 'dnk_name'
    _order = 'dnk_name, id'

    dnk_name = fields.Char('- Name', index=True, required=True, translate=True)
    sequence = fields.Integer('- Sequence')
    dnk_description = fields.Text(
        '- Description', translate=True)
    dnk_type = fields.Selection([
        ('unit', 'Unit'),
        ('volume', 'Volume'),
        ('percent', 'Percent')], string='- Type', default='unit', required=True,  ondelete='cascade',
        help='Unit cost is added only once.\n'
             'Volume cost is added depending of the quantity of MO, is only for view purpose.\n'
             'Percent cost is a percet of the total of Material Cost.')
    dnk_default_value_html = fields.Html(
        '- Value', translate=False)
    dnk_value = fields.Float(
        '- Value',
        digits='Product Price')
    dnk_volume_cost_line_ids = fields.One2many(
        comodel_name='dnk.indirect.manufacturing.cost.volume',
        inverse_name='dnk_indirect_anufacturing_cost_id',
        string='- Volume Cost Line')

    @api.onchange('dnk_type', 'dnk_volume_cost_line_ids', 'dnk_value')
    def onchange_type(self):
        for gif in self:
            precision_digits = self.env['decimal.precision'].search([('name', '=', 'Product Price')]).digits
            if gif.dnk_type != 'volume':
                if gif.dnk_type == 'percent':
                    gif.dnk_default_value_html = '<table width="100%"><tr><td align="right">' + '%0.*f' % (2, gif.dnk_value) + ' %</td></tr></table>'
                else:
                    gif.dnk_default_value_html = '<table width="100%"><tr><td align="right">' + '%0.*f' % (precision_digits, gif.dnk_value) + '(USD)</td></tr></table>'
            else:
                html_table = '<table width="100%"><tr><td align="right"><b>More Than</b></td><td align="right"><b>Cost (USD)</b></td></tr>'
                for volume_line in gif.dnk_volume_cost_line_ids:
                    html_table += '<tr><td align="right">' + '%0.*f' % (2, volume_line.dnk_quantity) + '</td><td align="right">' + '%0.*f' % (precision_digits, volume_line.dnk_value) + '</td></tr>'
                html_table += '</table>'
                gif.dnk_default_value_html = html_table


class VolumeIndirectManufacturingCost(models.Model):
    _name = 'dnk.indirect.manufacturing.cost.volume'
    _description = 'Volume Indirect Manufacturing Costs (GIF Gastos Indirectos de Fabricación por Volumen)'
    _rec_name = 'dnk_quantity'
    _order = 'dnk_quantity desc, id'

    dnk_sequence = fields.Integer('- Sequence')
    dnk_quantity = fields.Float(
        string="- More Than", default=100.00)
    dnk_default_price_usd = fields.Float(
        '- Cost (USD)',
        digits='Product Price',
        help="This cost of this or less volume quantity")
    dnk_indirect_anufacturing_cost_id = fields.Many2one('dnk.indirect.manufacturing.cost', '- GIF Cost')
