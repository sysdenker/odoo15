# -*- coding: utf-8 -*-
{
    'name': "Denker - Account Move Custom",

    'summary': """
        Este módulo agrega los campos Referencia interna del producto en las Pólizas y Asientos Contables.""",

    'description': """
        Este módulo agrega los campos Referencia interna del producto en las Pólizas y Asientos Contables.""",

    'author': "Servicios Corporativos Denker - JJCT",
    'website': "http://www.grupodenker.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Accounting',
    'version': '15.0.1.0.0',
    'license': 'AGPL-3',
    # any module necessary for this one to work correctly
    'depends': ['account', 'stock_account', 'dnk_groups_categories', 'l10n_mx_edi'],

    # always loaded
    'data': [
        'views/account_move_views.xml',
        'security/res_groups.xml',
        'security/ir.model.access.csv',
        'wizard/account_move_wizard.xml',
        'wizard/account_move_line_wizard.xml',

    ],
    # only loaded in demonstration mode
    'demo': [
        # 'demo/demo.xml',
    ],
}
