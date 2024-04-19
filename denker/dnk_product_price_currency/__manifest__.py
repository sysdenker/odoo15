#!/usr/bin/python
# -*- coding: utf-8 -*-
{
    'name': "Denker - Product Price Currency",

    'summary': """
        Este módulo permite definir en los productos una moneda diferente de la predeterminada (que es la moneda de la compañía donde se define este producto).
    """,

    'description': """
        This module allow to define on products a different currency from the default one (which is company currency were this product is defined).
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
    'depends': ['product'],

    # always loaded
    'data': [
        'views/product_template_views.xml',
        'security/product_currency_security.xml',
    ],
}
