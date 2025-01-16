# -*- coding: utf-8 -*-
{
    "name": "Denker - Stock Quant Mod",

    'author': 'Servicios Corporativos Denker - JBCH',
    'website': 'www.grupodenker.com',
    'version': '15.0.1.0.0',
    'license': 'AGPL-3',
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Operations/Maintenance',

    'summary': """
        Módulo para agregar o modificar campos/funciones nativos.
    """,
    'description': """
        Módulo para agregar o modificar campos/funciones nativos.
    """,

    # any module necessary for this one to work correctly
    'depends': ['stock', 'base'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/dnk_stock_quant_log.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
    'installable': True,
}
