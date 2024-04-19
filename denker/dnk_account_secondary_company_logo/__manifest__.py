# -*- coding: utf-8 -*-
{
    'name': "Denker - Secondary Company Logo",

    'summary': """
        Agrega otro campo de logo en "compañías".
    """,

    'description': """
        Agrega otro campo de logo en "compañías" para poderlo agregar en el encabezado de los documentos externos como cotizaciones y facturas.
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
    'depends': ['base', 'web'],

    # always loaded
    'data': [
        'views/company_views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
}
