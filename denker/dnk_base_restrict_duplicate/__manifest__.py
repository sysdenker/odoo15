# -*- coding: utf-8 -*-
{
    'name': "Denker - Restrict Duplicate",

    'summary': """
        Este módulo restringe la acción "Duplicar" en la vista de formulario algunos modelos.
        """,

    'description': """
        Este módulo restringe la acción "Duplicar" en la vista de formulario para los siguientes modelos:
            1) Manufacturing Order (mrp.production)
            2) Transfer (stock.picking)
            3) Out Invoice (account.move)
            4) Out Refunds (account.move)
    """,

    'author': "Servicios Corporativos Denker - JJCT",
    'website': "http://www.grupodenker.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Tools',
    'version': '15.0.1.0.0',
    'license': 'AGPL-3',
    # any module necessary for this one to work correctly
    'depends': ['account', 'mrp', 'stock', 'purchase', 'dnk_groups_categories'],

    # always loaded
    'data': [
        'security/security.xml',
        'views/mrp_production_views.xml',
        'views/stock_picking_views.xml',
        'views/account_invoice_views.xml',
        'views/purchase_order_views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
}
