# -*- coding: utf-8 -*-
# © 2016 OdooMRP team
# © 2016 AvanzOSC
# © 2016 Serv. Tecnol. Avanzados - Pedro M. Baeza
# © 2016 Eficent Business and IT Consulting Services, S.L.
# Copyright 2017 Serpent Consulting Services Pvt. Ltd.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    'name': "Denker - MRP Workorder Custom",

    'summary': """
        Este módulo hace varias personalizaciones a las Órdenes de Trabajo en del módulo de Manufactura.""",

    'description': """
        Este módulo hace la siguientes personalizaciones a las Órdenes de Trabajo en del módulo de Manufactura:
            1) Ajusta el texto del nombre del producto para que se vea completo en la vista de tablet de Órdenes de Trabajo.
            2) Agrega el campo html_color al modelo mrp.workorder para mostrarlo en la vista de tablet de Órdenes de Trabajo.""",

    'author': "Servicios Corporativos Denker - JJCT",
    'website': "http://www.grupodenker.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Manufacturing',
    'version': '15.0.1.0.0',
    'license': 'AGPL-3',
    # any module necessary for this one to work correctly
    'depends': ['mrp', 'mrp_workorder', 'quality', 'quality_mrp', 'dnk_groups_categories'],

    # always loaded
    'data': [
        'security/account_security.xml',
        'views/mrp_workorder_views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        # 'demo/demo.xml',
    ],
}
