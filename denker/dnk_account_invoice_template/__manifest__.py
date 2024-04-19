# -*- coding: utf-8 -*-
{
    'name': 'Denker - Account Invoice Template',

    'summary': """
        Este módulo modifica el diseño de la factura para que cumpla con las características necesarias para Grupo Denker.
    """,

    'description': """
        1. Al facturar a un contacto de un cliente, eliminar el nombre del contacto para dejar solamente el nombre de la empresa.
        2. Compactar los más posible la factura para mostrar más líneas de factura en cada página.
        3. Agrega el dato "Lugar Expedición" como lo requieren las facturas en México.
        4. Agrega la columna "Partida" en la líneas de factura.
        5. Agrega la columna "Código de Unidad" del SAT en la líneas de factura.
        6. Agrega la moneda y el tipo de cambio en caso de que la factura sea en una moneda extranjera.
        7. Cambia la etiqueta "Referencia" por "Orden de Compra" del cliente.
        8. Agrega el texto correspondiente a un cheque válido con un pago por retraso del 5% mensual, además de un espacio para firma.
    """,

    'author': "Servicios Corporativos Denker - JJCT",
    'website': "http://www.grupodenker.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Accounting',
    'version': '15.0.1.0.0',
    'license': 'AGPL-3',
    # any module necessary for this one to work correctly
    # 'depends': ['account', 'dnk_product_customer_code'], Módulo por migrar
    'depends': ['account'],

    # always loaded
    'data': [
        'views/report_invoice.xml',
    ],
}
