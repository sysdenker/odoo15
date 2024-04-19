# -*- coding: utf-8 -*-
{
    'name': "Denker - Purchase Mod",

    'summary': """
        Módulo genérico para modificaciones varias, por el momento solo agrego grupos.
        """,

    'description': """
    """,

    'author': "Servicios Corporativos Denker - JBCH",
    'website': "http://www.grupodenker.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Purchase',
    'version': '15.0.1.0',
    'license': 'AGPL-3',
    # any module necessary for this one to work correctly
    'depends': ['purchase_stock'],

    # always loaded
    'data': [
        'security/res_groups.xml',
    ],
}
