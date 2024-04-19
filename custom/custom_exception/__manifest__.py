#   © 2019 Kevin Kamau
#   License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl)

{
    'name': 'Custom Exception',
    'version': '15.0.1.0.1',
    'author': 'Kevin Kamau',
    'license': 'LGPL-3',
    'category': 'Extra',
    'support': 'kevkamaa@gmail.com',
    'depends': ['web'],
    'assets': {
        'web.assets_backend': [
            '/custom_exception/static/src/lib/sweetalert.min.js',
            '/custom_exception/static/src/js/custom_exception.js',
        ],
    },
    'images': ['images/main_screenshot.png'],
    'installable': True,
}
