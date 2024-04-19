# -*- coding: utf-8 -*-
{
    'name': "Denker - Sale Order to Account Move",

    'author': 'Servicios Corporativos Denker - JBCH',
    'website': 'www.grupodenker.com',
    'version': '15.0.1.0.0',
    'license': 'AGPL-3',
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Sales, Invoicing',

    'summary': """
        Se agrega la relación para ligar el pedido con la factura.
    """,
    'description': """
        Se agrega la relación para ligar el pedido con la factura.
    """,

    # any module necessary for this one to work correctly
    'depends': ['base', 'sale', 'account'],

    # always loaded
    'data': [
        'views/account_move.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
    'installable': True,
}
