# -*- coding: utf-8 -*-
# See README.rst file on addons root folder for license details
{
    'name': "Denker - Sale Pricelist Fixed Rate",

    'summary': """
        Es posible configurar listas de precios para que en vez de convertirla en un tipo de cambio del día, la convierta en un tipo de cambio fijo.
        """,

    'description': """
        Este módulo agrega el campo "Tasa Fija (USD)" en la configuración de Contabilidad para colocar ahí una tasa fija de conversión de Precios de Listas que estén configuradas para hacer esto.
    """,

    'author': "Servicios Corporativos Denker - JJCT",
    'website': "http://www.grupodenker.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Product',
    'version': '15.0.1.0.0',
    'license': 'AGPL-3',
    # any module necessary for this one to work correctly
    'depends': ['sale', 'dnk_groups_categories'],

    # always loaded
    'data': [
        'security/pricelist_security.xml',
        'views/res_config_settings_views.xml',
        'views/pricelist_views.xml',
        'views/sale_views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        # 'demo/demo.xml',
    ],
}
