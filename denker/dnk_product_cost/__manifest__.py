# -*- coding: utf-8 -*-
{
    "name": "Denker - Product Cost",

    'author': 'Servicios Corporativos Denker - JBCH',
    'website': 'www.grupodenker.com',
    'version': '13.0.1',
    'license': 'AGPL-3',
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Manufacturing',

    'summary': """
        Módulo para detallar precio y tiempo de productos.
    """,
    'description': """
        Módulo para detallar precio y tiempo de productos.
    """,

    # any module necessary for this one to work correctly
    'depends': ['product', 'mrp', 'sale', 'dnk_product_category'],

    # always loaded
    'data': [
        'security/res_groups.xml',
        'security/ir.model.access.csv',
        'views/res_company.xml',
        'views/product_attribute_value.xml',
        'views/dnk_indirect_manufacturing_cost.xml',
        'views/dnk_labour_cost.xml',
        'views/mrp_production.xml',
        'views/product_product.xml',
        'views/product_template.xml',
        'views/dnk_product_cost.xml',
        'views/product_category.xml',
        'wizard/product_dnk_std_cost.xml',
        'wizard/dnk_new_product_cost.xml',
        'wizard/dnk_mrp_production_val.xml',
        'wizard/dnk_commercial_cost.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
    'installable': True,
}
