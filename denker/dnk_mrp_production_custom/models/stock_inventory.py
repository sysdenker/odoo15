# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, models
import logging

_logger = logging.getLogger(__name__)

class BarcodeEventsMixin(models.AbstractModel):
# class StockInventory(models.Model):
    # _name = 'stock.inventory'
    _inherit = ['barcodes.barcode_events_mixin']

    def on_barcode_scanned(self, barcode):
        super(BarcodeEventsMixin, self).on_barcode_scanned(barcode)

        stock_quant_package = self.env['stock.quant.package'].search([('name', '=', barcode)])
        _logger.info('Scanned: %s', barcode)

        if stock_quant_package:
            _logger.info('Scanned: %s Stock Quant Package', stock_quant_package)
            # stock.quant
            for quant_id in stock_quant_package.quant_ids:
                _logger.info('Add Product: %s with Quantity: %s', quant_id.product_id.name, quant_id.quantity)
                self._add_product(quant_id.product_id, quant_id.quantity)

            return
