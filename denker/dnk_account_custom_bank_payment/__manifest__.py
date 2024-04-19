# -*- coding: utf-8 -*-
# See README.rst file on addons root folder for license details
{
    'name': "Denker - Account Custom Bank Payment",

    'summary': """
        Nombra el pago creado desde un "Extracto bancario" con el consecutivo correspondiente en vez de con el nombre del "Extracto bancario".
        """,

    'description': """
        1. Nombra el pago creado desde un "Extracto bancario" con el consecutivo correspondiente en vez de con el nombre del "Extracto bancario".
        2. Hace que el xml y el pdf de facturas de clientes sea el mismo, con el stadard del módulo de la localización mexicana (l10n_mx_edi).
        3. Hace que el xml y el pdf de pagos de facturas de clientes sea el mismo, con el stadard del módulo de la localización mexicana (l10n_mx_edi).
        4. Transfiere la cuenta bancaria del cliente de la línea del "Extracto bancario" hacia el pago resultante.

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
    'depends': ['account', 'l10n_mx_edi'],

    # always loaded
    'data': [
        # Otra manera de actualizar registros, no borrar
        # 'data/payment_receipt_data.xml',
        # 'data/mail_invoice_template.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        # 'demo/demo.xml',
    ],
    'pre_init_hook': 'pre_init_hook',
}
