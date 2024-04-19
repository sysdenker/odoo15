# -*- coding: utf-8 -*-
##############################################################################
#
#    DevIntelle Solution(Odoo Expert)
#    Copyright (C) 2015 Devintelle Soluation (<http://devintelle.com/>)
#
##############################################################################
{
    'name': 'Split Purchase Order',
    'version': '15.0.1.0.0',
    'description': """
         Apps will Split large Purchase Order/Qutataion into sub Purchase Order/Qutataion.
    """,
    "category": 'Purchase',
    'summary': 'Apps will Split large Purchase Order/Qutataion into sub Purchase Order/Qutataion.',
    'author': 'DevIntelle Consulting Service Pvt.Ltd',
    'website': 'http://www.devintellecs.com/',
    'images': ['images/main_screenshot.png'],
    'depends': ['sale_stock', 'purchase'],
    'data': [
        'views/dev_split_view.xml',
        'wizard/split_purchase_order_view.xml',
    ],
    'demo': [],
    'test': [],
    'installable': True,
    'auto_install': False,
    'application': True,
    'price': 16.0,
    'currency': 'EUR',
}
