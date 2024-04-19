# -*- coding: utf-8 -*-
{
    'name': "Denker - Sale Pricelist Level",

    'summary': """
        Restringe, en pedidos de venta, utilizar tarifas más baratas a la definida por defecto para el cliente.
        """,

    'description': """
        Este módulo agrega el campo "Nivel" a las listas de precio, para ordenar las listas de más caras a más baratas,
        esto para que al cotizar a un cliente se restrinja el uso de Listas de Precios más baratas a la definida por el cliente.
    """,

    'author': "Servicios Corporativos Denker - JJCT",
    'website': "http://www.grupodenker.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Sales',
    'version': '15.0.1.0.0',
    'license': 'AGPL-3',
    # any module necessary for this one to work correctly
    'depends': ['sale', 'product', 'dnk_groups_categories'],

    # always loaded
    'data': [
        'security/pricelist_security.xml',
        'views/pricelist_views.xml',
    ],
}
