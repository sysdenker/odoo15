# -*- coding: utf-8 -*-
{
    "name": "Denker - Product Category on Reports",

    'author': 'Servicios Corporativos Denker - JBCH',
    'website': 'www.grupodenker.com',
    'version': '13.0.1',
    'license': 'AGPL-3',
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Manufacturing',

    'summary': """
        Módulo para agregar la familia, subfamilia y color a modelos y reportes.
    """,
    'description': """
        Módulo para agregar la familia, subfamilia y color a modelos y reportes.
    """,

    # any module necessary for this one to work correctly
    'depends': ['account', 'product', 'sale'],

    # always loaded
    'data': [
        'views/product_category.xml',
        # 'views/account_payment.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
    'installable': True,
}
