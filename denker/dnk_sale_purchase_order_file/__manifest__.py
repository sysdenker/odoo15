# -*- coding: utf-8 -*-
{
    "name": "Denker - Purchase Order in Sale Order",

    'author': 'Servicios Corporativos Denker - JBCH',
    'website': 'www.grupodenker.com',
    'version': '15.0.1.0.0',
    'license': 'AGPL-3',
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Sales, Invoicing',

    'summary': """
        Se agregan los campos para guardar un documento para la orden de compra y en el pedido de venta
        para que se adjunte en el correo de la factura.
    """,
    'description': """
        Se agregan los campos para guardar un documento para la orden de compra y en el pedido de venta
        para que se adjunte en el correo de la factura.
    """,

    # any module necessary for this one to work correctly
    'depends': ['account', 'sale', 'dnk_sale_order_to_account_move'],

    # always loaded
    'data': [
        'views/res_partner.xml',
        'views/sale_order.xml',
        'views/account_move.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
    'installable': True,
}
