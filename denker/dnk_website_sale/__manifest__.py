# -*- coding: utf-8 -*-
{
    "name": "Denker - Website Sale Custom",

    'author': 'Servicios Corporativos Denker - JBCH',
    'website': 'www.grupodenker.com',
    'version': '13.0.1',
    'license': 'AGPL-3',
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Sales, Lead Automation',

    'summary': """
        Módulo para modifcar campos en el website.
    """,
    'description': """
        Módulo para modifcar campos en el website.
    """,

    # any module necessary for this one to work correctly
    'depends': ['website_sale', 'sale', 'website'],

    # always loaded
    'data': [
        'views/product_views.xml',
        # 'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
    'installable': True,
}
