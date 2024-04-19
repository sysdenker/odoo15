# -*- coding: utf-8 -*-
{
    "name": "Denker - Profit Margin Color",

    'author': 'Servicios Corporativos Denker - JBCH',
    'website': 'www.grupodenker.com',
    'version': '15.0.1.0.0',
    'license': 'AGPL-3',
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Sales, Invoicing',

    'summary': """
        Módulo para asignar color de acuerdo al margen de utilidad.
    """,
    'description': """
        Módulo para asignar color de acuerdo al margen de utilidad.
    """,

    # any module necessary for this one to work correctly
    'depends': ['sale', 'account', 'dnk_product_cost'],

    # always loaded
    'data': [
        'views/sale_order.xml',
        'views/account_move.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
    'installable': True,
}
