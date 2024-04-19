# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
import odoo.addons.decimal_precision as dp
# from openerp.exceptions import UserError, RedirectWarning, ValidationError
import logging

_logger = logging.getLogger(__name__)


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    dnk_minimum_quantity = fields.Text(string='- Min. Qty.', store=True)
    dnk_volume_prices = fields.Text(string='- Volume Prices', store=True)
    dnk_has_volume_prices = fields.Boolean(string='- Has Volume Prices?', store=True)

    @api.onchange('product_id', 'product_uom_qty')
    def _get_volume_prices(self):
        for sale_order_line in self:
            if sale_order_line.product_id.dnk_volume_quotation:
                dnk_minimum_quantity, dnk_volume_prices = self._get_volume_prices_per_sale_line(sale_order_line.order_id, sale_order_line.product_id, self.product_uom, self.product_uom_qty, self.price_unit)

                sale_order_line.dnk_minimum_quantity = dnk_minimum_quantity
                sale_order_line.dnk_volume_prices = dnk_volume_prices
                if dnk_minimum_quantity == '' and dnk_volume_prices == '':
                    sale_order_line.dnk_has_volume_prices = False
                else:
                    sale_order_line.dnk_has_volume_prices = True

    @api.model
    def write(self, vals):
        for rec in self:
            if rec.product_id.dnk_volume_quotation:
                dnk_minimum_quantity, dnk_volume_prices = rec._get_volume_prices_per_sale_line(rec.order_id, rec.product_id, rec.product_uom, rec.product_uom_qty, rec.price_unit)
                vals_append = {
                    'dnk_minimum_quantity': dnk_minimum_quantity,
                    'dnk_volume_prices': dnk_volume_prices,
                }
                vals.update(vals_append)
        return super(SaleOrderLine, self).write(vals)

    @api.model
    def create(self, vals):
        product = self.env['product.product'].browse(vals.get('product_id'))

        if product.dnk_volume_quotation:
            sale_order = self.env['sale.order'].browse(vals.get('order_id'))
            product_uom = self.env['uom.uom'].browse(vals.get('product_uom'))
            product_uom_qty = vals.get('product_uom_qty')
            price_unit = vals.get('price_unit')
            if price_unit is None:
                price_unit = 0.0
            dnk_minimum_quantity, dnk_volume_prices = self._get_volume_prices_per_sale_line(sale_order, product, product_uom, product_uom_qty, price_unit)

            vals_append = {
                'dnk_minimum_quantity': dnk_minimum_quantity,
                'dnk_volume_prices': dnk_volume_prices,
            }
            vals.update(vals_append)

        return super(SaleOrderLine, self).create(vals)

    def _formatLang(self, value, show_currency=True):
        lang = self.order_id.partner_id.lang
        lang_objs = self.env['res.lang'].search([('code', '=', lang)])
        if not lang_objs:
            lang_objs = self.env['res.lang'].search([], limit=1)
        lang_obj = lang_objs[0]

        decimals_quantity = self.env['decimal.precision'].search([('name', '=', 'Product Price')])
        if decimals_quantity:
            decimals_quantity = decimals_quantity[0].digits
        else:
            decimals_quantity = 2

        res = lang_obj.format('%.' + str(decimals_quantity) + 'f', value, grouping=True, monetary=True)
        currency_obj = self.order_id.currency_id

        if show_currency and currency_obj and currency_obj.symbol:
            if currency_obj.position == 'after':
                res = '%s%s' % (res, currency_obj.symbol)
            elif currency_obj and currency_obj.position == 'before':
                res = '%s%s' % (currency_obj.symbol, res)
        return res

    def _search_pricelist_item_product(self, product_id, pricelist_id):
        _logger.info('Call _search_pricelist_item_product(%s, %s)', product_id, pricelist_id)
        found_pricelist_id = False
        applied_on = False
        applied_on_value = False
        ProductPriceListItem = self.env['product.pricelist.item']
        # Buscar por Variante del Producto en las Líneas de la Lista de precios
        price_list_item_ids = ProductPriceListItem.search(
            [('pricelist_id', '=', pricelist_id.id),
             ('applied_on', '=', '0_product_variant'),
             ('product_id', '=', product_id.id)])
        if len(price_list_item_ids) >= 1:
            found_pricelist_id = price_list_item_ids[0].pricelist_id
            applied_on = 'product_id'
            applied_on_value = product_id.id
        else:
            # Buscar por Producto Template en las Líneas de la Lista de precios
            price_list_item_ids = ProductPriceListItem.search(
                [('pricelist_id', '=', pricelist_id.id),
                 ('applied_on', '=', '1_product'),
                 ('product_tmpl_id', '=', product_id.product_tmpl_id.id)])
            if len(price_list_item_ids) >= 1:
                found_pricelist_id = price_list_item_ids[0].pricelist_id
                applied_on = 'product_tmpl_id'
                applied_on_value = product_id.product_tmpl_id.id
            else:
                # Buscar por Categoría de Producto en las Líneas de la Lista de precios
                price_list_item_ids = ProductPriceListItem.search(
                    [('pricelist_id', '=', pricelist_id.id),
                     ('applied_on', '=', '2_product_category'),
                     ('categ_id', '=', product_id.categ_id.id)])
                if len(price_list_item_ids) >= 1:
                    found_pricelist_id = price_list_item_ids[0].pricelist_id
                    applied_on = 'categ_id'
                    applied_on_value = product_id.categ_id.id
                else:
                    # Si no se encontró ninguna línea de tarifa relacionada directamente con: Variante del Producto, Produto, ni Categoría del Producto,
                    # buscar alguna línea de tarifa que se base en otra tarifa
                    price_list_item_ids = ProductPriceListItem.search(
                        [('pricelist_id', '=', pricelist_id.id),
                         ('applied_on', '=', '3_global'),
                         ('base', '=', 'pricelist')])
                    for price_list_item_id in price_list_item_ids:
                        found_pricelist_id, applied_on, applied_on_value = self._search_pricelist_item_product(product_id, price_list_item_id.base_pricelist_id)

                        if found_pricelist_id:
                            break

        if found_pricelist_id:
            return found_pricelist_id, applied_on, applied_on_value
        else:
            return False, applied_on, applied_on_value

    def _get_volume_prices_per_sale_line(self, order_id, product_id, product_uom, product_uom_qty, price_unit):
        if not (product_id and order_id.partner_id and order_id.pricelist_id and product_id.dnk_volume_quotation):
            return('', '')
        found_pricelist_id, applied_on, applied_on_value = self._search_pricelist_item_product(product_id, order_id.pricelist_id)

        str_prices = ''
        str_mininimum_quantity = ''
        if found_pricelist_id:
            # Recorrer las líneas de la tarifa para encontrar los mínimos
            ProductPriceListItem = self.env['product.pricelist.item']
            price_list_item_ids = ProductPriceListItem.search(
                [('pricelist_id', '=', found_pricelist_id.id),
                 (applied_on, '=', applied_on_value)], order="min_quantity DESC")

            context_partner = dict(self.env.context, partner_id=order_id.partner_id.id, date=order_id.date_order)
            pricelist_context = dict(context_partner, uom=product_uom.id)

            unit_price = ''
            for price_list_item_id in price_list_item_ids:
                if price_list_item_id.id and price_list_item_id.min_quantity:
                    unit_price, rule_id = order_id.pricelist_id.with_context(pricelist_context).get_product_price_rule(product_id, price_list_item_id.min_quantity, order_id.partner_id)

                    """
                    #############################################################################################
                    # Aquí es donde debo calcular con la Tasa Fija en USD si la Lista de Precio está configurada.
                    if order_id.pricelist_id.dnk_use_usd_fixed_rate:
                        usd_current_exchange_rate = self.env.ref("base.USD").rate
                        print("usd_current_exchange_rate: ", usd_current_exchange_rate)
                        usd_fixed_rate = self.order_id.company_id.dnk_usd_fixed_rate
                        print("usd_fixed_rate: ", usd_fixed_rate)

                        # Calcular el precio basado en la Tasa Fija de USD configurada en la compañía
                        unit_price = round(unit_price * usd_current_exchange_rate * usd_fixed_rate, 4)
                    #############################################################################################
                    """

                    str_prices += self._formatLang(unit_price, show_currency=False) + "\n"
                    str_mininimum_quantity += '{:0,.2f}'.format(price_list_item_id.min_quantity) + "\n"

        return(str_mininimum_quantity, str_prices)
