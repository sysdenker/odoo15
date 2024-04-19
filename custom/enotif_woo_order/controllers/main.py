
from odoo import http
from odoo.http import request

class Customer(http.Controller):

                        
    @http.route(['/enotif_woo_order/import_orders/'], type="json", methods=['POST', 'GET'], auth="user", website=True)
    def import_customers(self, **kw):
 
        result = request.env['enotif_woo_order.order'].import_orders()

        return result

        