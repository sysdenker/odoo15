# -*- coding: utf-8 -*-
{
    'name': "Denker - Sale Order Line Menu",

    'summary': """
        Muestra el submenú Líneas de Pedidos dentro del menú Pedidos en la aplicación de Ventas, para mostrar una vista de lista de Líneas de Pedidos""",

    'author': "Servicios Corporativos Denker - JJCT",
    'website': "http://www.grupodenker.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Sales',
    'version': '13.0.1.0',
    'license': 'AGPL-3',
    # any module necessary for this one to work correctly
    # 'depends': ['sale', 'sale_stock', 'dnk_sale_order_commitment_date', 'web_tree_dynamic_colored_field'],
    'depends': ['sale', 'sale_stock'],

    # always loaded
    'data': [
        'views/sale_order_line_views.xml',
    ],
}
