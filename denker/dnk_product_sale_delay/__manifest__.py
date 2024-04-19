# -*- coding: utf-8 -*-
{
    "name": "Denker - Variant Lead Time",

    'author': 'Servicios Corporativos Denker - JBCH',
    'website': 'www.grupodenker.com',
    'version': '13.0.1',
    'license': 'AGPL-3',
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Sales, Lead Automation',

    'summary': """
        Módulo para cambiar el tiempo de entrega de los productos, para que sea por variante.
    """,
    'description': """
        Módulo para cambiar el tiempo de entrega de los productos, para que sea por variante.
    """,

    # any module necessary for this one to work correctly
    'depends': ['product', 'stock'],

    # always loaded
    'data': [
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
    'installable': True,
}
