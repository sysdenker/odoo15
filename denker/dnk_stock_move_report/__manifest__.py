# -*- coding: utf-8 -*-
{
    "name": "Denker - Stock Move Report",

    'author': 'Servicios Corporativos Denker - JBCH',
    'website': 'www.grupodenker.com',
    'version': '13.0.1',
    'license': 'AGPL-3',
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Sales, Invoicing',

    'summary': """
        Módulo para generar un campo almacenado con el monto total, en dólar,  del total de la factura, orden de compra y oportunidades.
    """,
    'description': """
        Módulo para generar un campo almacenado con el monto total, en dólar del total de la factura,
        orden de compra y sus respectivas líneas, y también a Oportunides.
    """,

    # any module necessary for this one to work correctly
    'depends': ['stock', 'sale', 'account'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/stock_move_report.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
    'installable': True,
}
