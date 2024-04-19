# -*- coding: utf-8 -*-
{
    'name': "Denker - Sale Product Configurator Custom",

    'summary': """
        """,

    'description': """
    """,

    'author': "Servicios Corporativos Denker - JJCT",
    'website': "http://www.grupodenker.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Sales',
    'version': '13.0.1.0',
    'license': 'AGPL-3',
    # any module necessary for this one to work correctly
    'depends': ['sale_product_configurator', 'dnk_groups_categories'],

    # always loaded
    'data': [
        'security/product_configurator_security.xml',
        'views/sale_views.xml',
    ],
}
