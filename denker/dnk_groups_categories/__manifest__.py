# -*- coding: utf-8 -*-
{
    "name": "Denker - Groups Categories",

    'author': 'Servicios Corporativos Denker - JBCH',
    'website': 'www.grupodenker.com',
    'version': '15.0.1.0.0',
    'license': 'AGPL-3',

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Administration',

    'summary': """
        Módulo para generar categorías de grupos.
    """,
    'description': """
        Módulo para generar categorías que utilizarán los grupos que se irán creando con los módulos.
    """,

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/categories.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
    'installable': True,
}
