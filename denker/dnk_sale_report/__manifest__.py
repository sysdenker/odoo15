# -*- coding: utf-8 -*-
{
    "name": "Denker - Sale Reports",

    'author': 'Servicios Corporativos Denker - JBCH',
    'website': 'www.grupodenker.com',
    'version': '13.0.1',
    'license': 'AGPL-3',
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Sales, Invoicing',

    'summary': """
        Módulo para generar Vista/Reporte de Ventas.
    """,
    'description': """
        Módulo para generar Vista/Repoprte de Ventas.
    """,

    # any module necessary for this one to work correctly
    'depends': ['sale', 'account', 'stock'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        # 'views/dnk_sale_report.xml',
        # 'views/dnk_stock_quant_report.xml'
        'views/dnk_sm_service_level.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
    'installable': True,
}
