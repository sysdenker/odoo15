# -*- coding: utf-8 -*-
{
    'name': "Cancellation reason, CFDI patch 2022 (Mexican Localization)",

    'summary': """
        Mexican Localization - CFDI 4.0
        This module is complaint to the cancellation process of CFDI 2022.
    """,

    'description': """
    """,

    'author': 'José Candelas',
    'support': 'support@candelassoftware.com',
    'license': 'OPL-1',
    'website': 'http://www.candelassoftware.com',
    'currency': 'USD',
    'price': 50.00,
    'maintainer': 'José Candelas',
    'images': ['static/description/banner_cnd_l10n_mx_edi_restrict_sign.png'],

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Accounting',
    'version': '14.0.1.1',

    # any module necessary for this one to work correctly
    'depends': ['account', 'l10n_mx_edi'],

    # always loaded
    'data': [
        'views/account_move_views.xml',
    ],
    'installable': True,
    'auto_install': False,
    'pre_init_hook': 'pre_init_check',
}
