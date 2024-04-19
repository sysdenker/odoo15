# -*- coding: utf-8 -*-
{
    "name": "Denker - Product Development",

    'author': 'Servicios Corporativos Denker - JBCH',
    'website': 'www.grupodenker.com',
    'version': '13.0.1',
    'license': 'AGPL-3',
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Sales, Lead Automation',

    'summary': """
        Módulo para el registro los Desarrollos de Producto.
    """,
    'description': """
        Módulo para el registro los Desarrollos de Producto.
    """,

    # any module necessary for this one to work correctly
    'depends': ['crm', 'sale_crm'],

    # always loaded
    'data': [

        'data/ir_sequence.xml',
        'security/res_groups.xml',
        'security/ir.model.access.csv',
        'views/dnk_pdev_line.xml',
        'views/product_development.xml',
        'views/dnk_product_dev_menu_views.xml',
        'views/product.xml',
        'data/dnk_crm_pd_stage.xml',
        'data/dnk_crm_pd_type.xml',
        'views/crm.xml',
        'views/dnk_pdav.xml',
        'views/product_attribute_value.xml',
        'views/dnk_pdev_line.xml',
        'report/dnk_pdev_report_views.xml',
        'report/dnk_pdev_document.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
    'installable': True,
}
