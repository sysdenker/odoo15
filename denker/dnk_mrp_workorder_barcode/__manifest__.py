# -*- coding: utf-8 -*-
{
    'name': "Denker - MRP Work Order Barcode",

    'summary': """
        Este módulo habilita un scanner de códigos de barras para incrementar la cantidad hecha de una Orden de Trabajo escaneando el código de barras del producto de la WO.""",

    'description': """
    """,

    'author': "Servicios Corporativos Denker - JJCT",
    'website': "http://www.grupodenker.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Manufacturing',
    'version': '15.0.1.0.0',
    'license': 'AGPL-3',
    # any module necessary for this one to work correctly
    'depends': ['mrp', 'mrp_workorder', 'custom_exception'],

    # always loaded
    'data': [
        'views/mrp_workorder_views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        # 'demo/demo.xml',
    ],
}
