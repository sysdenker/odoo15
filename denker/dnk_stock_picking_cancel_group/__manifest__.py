# -*- coding: utf-8 -*-
{
    'name': "Denker - Stock Picking Cancel Group",

    'summary': """
        This module adds a group of users called Cancel Transfers,
        only users in this group can cancel Transfers (Stock Pikcings)""",

    'author': "Servicios Corporativos Denker - JJCT",
    'website': "http://www.grupodenker.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Stock',
    'version': '15.0.1.0.0',
    'license': 'AGPL-3',
    # any module necessary for this one to work correctly
    'depends': ['stock', 'dnk_groups_categories'],

    # always loaded
    'data': [
        'security/account_security.xml',
        'views/stock_picking_views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
}
