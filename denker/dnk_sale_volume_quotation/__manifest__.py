# -*- coding: utf-8 -*-
{
    'name': 'Denker - Quotation by Volume',

    'summary': """
        This module adds automatically Sale Order Lines by Volume.
        The quantity of lines to add are the quantity of times de product appears in the Pricelist.
    """,

    'author': "Servicios Corporativos Denker - JJCT",
    'website': "http://www.grupodenker.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Sale',
    'version': '15.0.1.0.0',
    'license': 'AGPL-3',
    # any module necessary for this one to work correctly
    'depends': [
        'sale',
        'dnk_sale_order_custom_document',
        'dnk_sale_pricelist_fixed_rate',
    ],

    # always loaded
    'data': [
        'views/product_views.xml',
        'views/sale_order_line_views.xml',
        # 'views/sale_order_views.xml',
        'report/sale_report_templates.xml',
    ],
}
