#!/usr/bin/python
# -*- coding: utf-8 -*-
{
    'name': "Denker - Product Hide Cost and Sale Price",

    'summary': """
        This module hide cost and sale price based in user groups.
    """,

    'description': """
        Con este módulo es posible esconder el costo y el precio de los productos de los productos basándose en grupos de usuarios.
    """,

    'author': "Servicios Corporativos Denker - JJCT",
    'website': "http://www.grupodenker.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Product',
    'version': '13.0.1.0',
    'license': 'AGPL-3',
    # any module necessary for this one to work correctly
    'depends': ['product', 'stock_account', 'dnk_groups_categories', 'dnk_product_price_currency'],

    # always loaded
    'data': [
        'security/security.xml',
        'views/product_hide_cost.xml'
    ],
}
