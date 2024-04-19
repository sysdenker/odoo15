# -*- coding: utf-8 -*-
{
    'name': "Denker - Purchase No Merge Lines",

    'summary': """
        Cuando se crea automáticamente una PO, odoo por defecto combina las línes que tienen el mismo producto, aunque sea diferente la fecha planeada.
        Este módulo hace que no haga esa combinación y que respete la fecha plaeada por cada línea.
        """,

    'description': """
    """,

    'author': "Servicios Corporativos Denker - JJCT",
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
    ],
}
