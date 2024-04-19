# -*- coding: utf-8 -*-
###################################################################################
#
#    This program is free software: you can modify
#    it under the terms of the GNU Affero General Public License (AGPL) as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###################################################################################
{
    'name': 'Denker Biometric Device Integration PyZk',
    'version': '15.0.1.0.0',
    'summary': """Integrating Biometric Device With HR Attendance (Face + Thumb)""",
    'description': 'This module integrates Odoo with the biometric device. (Check below or README.md for compatible devices.)',
    'category': 'Generic Modules/Human Resources',
    'author': '10 Orbits',
    'company': '10 Orbits',
    'website': "https://erp.10orbits.com",
    'depends': ['base_setup', 'hr_attendance'],
    'data': [
        'security/ir.model.access.csv',
        'views/dnk_machine_view.xml',
        'views/dnk_machine_attendance_view.xml',
        'views/dnk_hr_employee.xml',
        'views/dnk_attendance.xml',
        'views/dnk_attendance_report.xml',
        'data/download_data.xml',
        'data/dnk_zk_machine.xml',
        'wizard/print_attendance_rep.xml',

    ],
    'images': ['static/description/banner.png'],
    'license': 'AGPL-3',
    'demo': [],
    'installable': True,
    'auto_install': False,
    'application': False,
}
