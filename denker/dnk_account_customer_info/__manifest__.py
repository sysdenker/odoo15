# -*- coding: utf-8 -*-
{
    "name": "Denker - Update Customer Fields on Invoice",

    'author': 'Servicios Corporativos Denker - JBCH',
    'website': 'www.grupodenker.com',
    'version': '15.0.1.0.0',
    'license': 'AGPL-3',
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Sales, Invoicing',

    'summary': """
        Actualizar los campos CDFI del cliente al crear una factura.
    """,
    'description': """
        Actualizar los campos CDFI del cliente al crear una factura.
    """,

    # any module necessary for this one to work correctly
    'depends': ['account', 'sale', 'l10n_mx_edi'],

    # always loaded
    'data': [
        'views/res_partner.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
    'installable': True,
}
