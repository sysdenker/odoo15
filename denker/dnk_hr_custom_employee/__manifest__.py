# -*- coding: utf-8 -*-
{
    'name': "Denker - HR Custom Employee",

    'summary': """
        Agrega los campos requeridos para hacer los contratos de los empleados de Grupo Denker y genera los contratos legales de los empleados.
    """,

    'description': """
    """,

    'author': "José Candelas",
    'website': "http://www.grupodenker.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'HR',
    'version': '15.0.1.0.0',
    'license': 'AGPL-3',
    # any module necessary for this one to work correctly
    'depends': ['hr', 'hr_contract', 'hr_recruitment'],

    # always loaded
    'data': [
        'security/res_groups.xml',
        'views/res_company_views.xml',
        'views/hr_employee_checklist_views.xml',
        'views/hr_employee_views.xml',
        'views/hr_contract_views.xml',
        'views/hr_job_views.xml',
        'views/resource_calendar_views.xml',
        # 'views/hr_applicant_views.xml',
        'data/employee_recruitment_source.xml',
        'security/ir.model.access.csv',
        'report/hr_contract_views.xml',
        'report/hr_contract_document.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
    'css': ['static/src/css/file.css'],
    'post_init_hook': 'post_init_hook',
}
