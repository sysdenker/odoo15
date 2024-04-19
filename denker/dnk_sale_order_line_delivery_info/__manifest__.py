# -*- coding: utf-8 -*-
{
    'name': "Denker - Sale Delivery Information",

    'summary': """
        Agregar el campo "Fecha de Entrega" a las líneas del pedido, calculando la fecha dependiendo de la rutas de abastecimiento del producto.
        """,

    'description': """
        Agregar el campo "Fecha de Entrega" a las líneas del pedido, calculando la fecha dependiendo de la rutas de abastecimiento del producto, toma en cuenta las reglas de la ruta.
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
    'depends': ['sale', 'sale_stock', 'dnk_sale_order_custom_document'],

    # always loaded
    'data': [
        'views/sale_order_views.xml',
        'report/sale_report_templates.xml',
    ],
}
