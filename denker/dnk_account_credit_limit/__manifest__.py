# -*- coding: utf-8 -*-
{
    "name": "Denker - Credit Limit",

    'author': 'Servicios Corporativos Denker - JBCH',
    'website': 'www.grupodenker.com',
    'version': '15.0.1.0.0',
    'license': 'AGPL-3',
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Sales, Invoicing',

    'summary': """
        Módulo para registrar un límite de crédito por cliente y para bloquear ventas y entregas.
    """,
    'description': """
        Módulo para registrar un límite de crédito por cliente y para bloquear ventas y entregas.
    """,

    # any module necessary for this one to work correctly
    'depends': ['base', 'sale', 'account', 'dnk_groups_categories'],

    # always loaded
    'data': [
        'security/res_groups.xml',
        'views/res_partner.xml',
        'views/sale_order.xml',
        'views/res_config_settings.xml',
        'views/stock_picking.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
    'installable': True,
}
