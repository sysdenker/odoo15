# -*- coding: utf-8 -*-
{
    "name": "Denker - CRM Opportunities",

    'author': 'Servicios Corporativos Denker - JBCH',
    'website': 'www.grupodenker.com',
    'version': '15.0.1.0.0',
    'license': 'AGPL-3',
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Sales, Lead Automation',

    'summary': """
        Módulo para agregar datos relevantes  y para facilitar análisis de las oportunidades.
    """,
    'description': """
        Módulo para agregar datos relevantes  y para facilitar análisis de las oportunidades.
    """,

    # any module necessary for this one to work correctly
    'depends': [
        'base', 'crm', 'sale', 'sale_crm', 'dnk_groups_categories', 'dnk_sale_order_to_account_move',
        'dnk_account_usd_amount_reports', 'dnk_sale_city', 'dnk_product_category'],

    # always loaded
    'data': [
        'views/crm_view.xml',
        'views/res_partner.xml',
        'views/account_move.xml',
        'views/sale_order.xml',
        'security/res_groups.xml',
        'security/ir.model.access.csv',
        'wizard/dnk_crm_dealer.xml',
        'views/rating_template.xml',
        'data/update_data.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
    'installable': True,
}
