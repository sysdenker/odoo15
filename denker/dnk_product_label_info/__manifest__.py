# -*- coding: utf-8 -*-
{
    'name': "Denker - Product Label Info",

    'summary': """
        Módulo para agregar el campo Material la Plantilla de Producto, además de los campos Talla y Cure en las MOs.
    """,

    'description': """
    """,

    'author': "Servicios Corporativos Denker - JJCT",
    'website': "http://www.grupodenker.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Products',
    'version': '15.0.1.0.0',
    'license': 'AGPL-3',
    # any module necessary for this one to work correctly
    # Validar si el módulo dnk_mrp_production_custom es necesario para este módulo
    # 'depends': ['base', 'product', 'mrp', 'dnk_mrp_production_custom', 'dnk_printing_labels'],
    'depends': ['base', 'product', 'mrp', 'dnk_printing_labels'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/product_material_views.xml',
        'views/product_template_views.xml',
        'views/mrp_production_views.xml',
        'views/product_product_views.xml',
        'data/product_material_data.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        # 'demo/demo.xml',
    ],
    'post_init_hook': 'post_init_hook',
}
