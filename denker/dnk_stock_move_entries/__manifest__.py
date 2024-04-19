# -*- coding: utf-8 -*-
{
    "name": "Denker - Journal Items and Entries On Stock View",

    'author': 'Servicios Corporativos Denker - JBCH',
    'website': 'www.grupodenker.com',
    'version': '15.0.1.0.0',
    'license': 'AGPL-3',
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Accounting',

    'summary': """
        'Módulo para agregar las vistas de los asientos y apuntes contables.
    """,
    'description': """
        'Módulo para agregar las vistas de los asientos y apuntes contables.
    """,

    # any module necessary for this one to work correctly
    'depends': ['stock', 'account'],

    # always loaded
    'data': [
        'views/stock_picking.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
    'installable': True,
}
