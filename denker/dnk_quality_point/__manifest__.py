# -*- coding: utf-8 -*-
{
    'name': "Denker - Quality Points",

    'author': 'Servicios Corporativos Denker - JBCH',
    'website': 'www.grupodenker.com',
    'version': '15.0.1.0.0',
    'license': 'AGPL-3',
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Manufacturing',

    'summary': """
        Módulo para la crear Alertas de Calidad.
    """,
    'description': """
        Módulo para la crear alertas de calidad.
    """,

    # any module necessary for this one to work correctly
    'depends': ['product', 'quality', 'mrp'],

    # always loaded
    'data': [
        'wizard/dnk_quality_point_wizard.xml',
        'security/ir.model.access.csv',
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
    'installable': True,
}
