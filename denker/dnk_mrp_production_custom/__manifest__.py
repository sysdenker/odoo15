# -*- coding: utf-8 -*-
{
    'name': "Denker - MRP Production Custom",

    'summary': """
        Este módulo agrega los campos familia y subfamilia en las MO.""",

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
    'depends': ['mrp', 'stock_barcode', 'sale'],

    # always loaded
    'data': [
        'views/mrp_production_views.xml',
        'wizard/mrp_production_wizard.xml',
        'security/ir.model.access.csv',
        'security/ir.model.access.csv',
        'views/dnk_mrp_manufacturing_status.xml',
        'views/dnk_mrp_manufacturing_delays.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        # 'demo/demo.xml',
    ],
    'post_init_hook': 'post_init_hook',
}
