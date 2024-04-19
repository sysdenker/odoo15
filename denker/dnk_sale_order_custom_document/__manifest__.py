# -*- coding: utf-8 -*-
{
    'name': 'Denker - Sale Order custom document',

    'summary': """
        This module modify the format of the sale order document to be sent to the customer.
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
    'depends': ['sale_management', 'l10n_mx_edi','base'],

    # always loaded
    'data': [
        'report/sale_report_templates.xml',
        'views/base_document_layout_views.xml',
    ],
}
