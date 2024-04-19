# -*- coding: utf-8 -*-
{
    "name": "Denker - Printing Labels",

    'summary': """
    This module prints labels of any odoo model in a label printer like Zebra Printer.""",

    'description': """
    """,

    "author": "Servicios Corporativos Denker - JJCT",
    "website": "http://www.grupodenker.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    "category": "Labels",
    'version': '15.0.1.0.0',
    'license': 'AGPL-3',
    # any module necessary for this one to work correctly
    'depends': ['base', 'mrp', 'stock'],

    # always loaded
    'data': [
        'security/res_groups.xml',
        'security/ir.model.access.csv',
        'data/labels/dnk_mrp_production_acuity_label.xml',
        'data/labels/dnk_mrp_production_argentina_label.xml',
        'data/labels/dnk_mrp_production_classic_label.xml',
        'data/labels/dnk_mrp_production_estashoe_label.xml',
        'data/labels/dnk_mrp_production_jabil_label.xml',
        'data/labels/dnk_mrp_production_prudential_label.xml',
        'data/labels/dnk_mrp_production_talonera_argentina_label.xml',
        'data/labels/dnk_mrp_production_talonera_label.xml',
        'data/labels/dnk_stock_picking_label.xml',
        'data/printing_label_group.xml',
        'views/ir_ui_view_views.xml',
        'views/printing_label_group_views.xml',
        'wizard/print_record_label.xml',
    ],
    'installable': True,
    'auto_install': False,
}
