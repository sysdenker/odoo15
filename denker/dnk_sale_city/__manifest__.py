# -*- coding: utf-8 -*-
{
    "name": "Denker - Sale City",

    'author': 'Servicios Corporativos Denker - JBCH',
    'website': 'www.grupodenker.com',
    'version': '15.0.1.0.0',
    'license': 'AGPL-3',
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Sales, Lead Automation',

    'summary': """
        Módulo para agregar la ciudad en la que se realiza la venta.
    """,
    'description': """
        Módulo para agregar la ciudad en la que se realiza la venta.
    """,

    # any module necessary for this one to work correctly
    'depends': ['base', 'sale', 'account', 'crm'],

    # always loaded
    'data': [
        'data/dnk_sale_city.xml',
        'security/ir.model.access.csv',
        'views/res_users.xml',
        'views/crm_lead.xml',
        'views/sale_order.xml',
        'views/account_move.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
    'installable': True,
}
