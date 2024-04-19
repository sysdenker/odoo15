# -*- coding: utf-8 -*-
{
    "name": "Denker - Customer Product Code",

    'author': 'Servicios Corporativos Denker - JBCH',
    'website': 'www.grupodenker.com',
    'version': '13.0.1',
    'license': 'AGPL-3',
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Sales, Invoicing',

    'summary': """
        Módulo para agregar el Código del producto del Cliente.
    """,
    'description': """
        Módulo para agregar el Código del producto del Cliente.
    """,

    # any module necessary for this one to work correctly
    'depends': ['sale', 'account', 'product', 'dnk_groups_categories', 'dnk_sale_order_to_account_move'],

    # always loaded
    'data': [
        'views/product_product.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
    'installable': True,
}
