# -*- coding: utf-8 -*-
{
    'name': "Denker - Add a sequence on customers' code",

    'summary': """
        Agrega una secuencia en el campo referencia de los clientes.""",

    'author': "Servicios Corporativos Denker - JJCT",
    'development_status': 'Stable',
    'website': "http://www.grupodenker.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Generic Modules/Base',
    'version': '15.0.1.0.0',
    'license': 'AGPL-3',
    # any module necessary for this one to work correctly
    'depends': ['base', 'dnk_groups_categories'],

    # always loaded
    'data': [
        'security/account_security.xml',
        'data/partner_sequence.xml',
        'views/partner_view.xml',
    ],
    # only loaded in demonstration mode
    'installable': True,
    'license': 'AGPL-3',
    'post_init_hook': 'post_init_hook',
}
