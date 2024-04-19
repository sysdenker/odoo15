# -*- coding: utf-8 -*-
{
    'name': "Denker - Account Invoice Overwrite Addenda",

    'summary': """
        Crea la addenda y la sobreescrive al archivo xml de la factura.
    """,

    'description': """
    """,

    'author': "Servicios Corporativos Denker - JJCT",
    'website': "http://www.grupodenker.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Accounting',
    'version': '15.0.1.0.0',
    'license': 'AGPL-3',
    # any module necessary for this one to work correctly
    'depends': ['account', 'l10n_mx_edi', 'dnk_groups_categories'],

    # always loaded
    'data': [
        'security/res_groups.xml',
        'views/account_invoice_views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        # 'demo/demo.xml',
    ],
}
