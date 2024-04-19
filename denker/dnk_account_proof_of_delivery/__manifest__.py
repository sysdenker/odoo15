# -*- coding: utf-8 -*-
{
    "name": "Denker - Proof of Delivery",

    'author': 'Servicios Corporativos Denker - JBCH',
    'website': 'www.grupodenker.com',
    'version': '15.0.1.0.0',
    'license': 'AGPL-3',
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Sales, Invoicing',

    'summary': """
        This module adds an image field to invoice as proof of delivery.
    """,
    'description': """
        This module adds an image field to invoice as proof of delivery.
    """,

    # any module necessary for this one to work correctly
    'depends': ['account', 'stock'],

    # always loaded
    'data': [
        'views/account_move.xml',
        # 'views/stock_picking_views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
    'installable': True,
}
