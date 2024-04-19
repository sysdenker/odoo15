# -*- coding: utf-8 -*-
{
    "name": "Google Drive Odoo Integration",
    "version": "13.0.1.1.9",
    "category": "Document Management",
    "author": "faOtools",
    "website": "https://faotools.com/apps/13.0/google-drive-odoo-integration-426",
    "license": "Other proprietary",
    "application": True,
    "installable": True,
    "auto_install": False,
    "depends": [
        "cloud_base"
    ],
    "data": [
        "data/data.xml",
        "security/ir.model.access.csv",
        "views/res_config_settings.xml"
    ],
    "qweb": [
        
    ],
    "js": [
        
    ],
    "demo": [
        
    ],
    "external_dependencies": {
        "python": []
},
    "summary": "The tool to automatically synchronize Odoo attachments with Google Drive files in both ways",
    "description": """

For the full details look at static/description/index.html

* Features * 

- Selectable documents types for sync

- Automatic and bilateral integration

- Direct access to Google Drive items

- Individual and team drives

- Fully integrated and compatible with Enterprise Documents

- Google Drive Sync logs in Odoo

- Default folders for documents
 
* Extra Notes *

- Typical use cases

- How files and folders are synced from Odoo to Google Drive

- How items are retrieved from Google Drive to Odoo

- &lt;i class='fa fa-folder-open'&gt;&lt;/i&gt; How Odoo Enterprise Documents are synced

- A few important peculiarities to take into account



#odootools_proprietary

    """,
    "images": [
        "static/description/main.png"
    ],
    "price": "264.0",
    "currency": "EUR",
    "live_test_url": "https://faotools.com/my/tickets/newticket?&url_app_id=80&ticket_version=13.0&url_type_id=3",
}