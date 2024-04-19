# -*- coding: utf-8 -*-
{
    'name': "Denker - Account Invoice Payment Report",

    'summary': """
        Genera un reporte basado en los pagos de clientes prorateados en las líneas de facturas.""",

    'author': "Servicios Corporativos Denker - JJCT",
    'website': "http://www.grupodenker.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Accounting',
    'version': '13.0.1.0',
    'license': 'AGPL-3',
    # any module necessary for this one to work correctly
    'depends': ['account', 'sale', 'crm', 'dnk_crm_opportunities'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'security/account_security.xml',
        'report/account_invoice_payment_report_views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        # 'demo/demo.xml',
    ],
}
