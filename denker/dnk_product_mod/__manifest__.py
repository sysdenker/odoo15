# -*- coding: utf-8 -*-
{
    "name": "Denker - Product Mod",

    'author': 'Servicios Corporativos Denker - JBCH',
    'website': 'www.grupodenker.com',
    'version': '13.0.1',
    'license': 'AGPL-3',
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Manufacturing',

    'summary': """
        Módulo para registrar detalles y especificaciones al producto.
    """,
    'description': """
        Módulo para registrar detalles y especificaciones al producto.
    """,

    # any module necessary for this one to work correctly
    'depends': ['product', 'mrp'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/dnk_bag_options.xml',
        'views/product_product.xml',
         'views/product_template.xml',

    ],
    # only loaded in demonstration mode
    'demo': [
    ],
    'installable': True,
}
