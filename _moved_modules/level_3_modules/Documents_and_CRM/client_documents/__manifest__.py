# -*- coding: utf-8 -*-
{
    "name": "Client Documents",
    "author": "Beshoy Wageh",
    "category": "Productivity/Documents",
    "version": "18.0.1.0.0",
    # any module necessary for this one to work correctly
    "depends": ["base", "contacts", "project", "stock", "sale_subscription", "documents"],
    # always loaded
    "data": [
        "security/security.xml",
        "security/ir.model.access.csv",
        "data/data.xml",
        "data/mail.xml",
        'data/cron.xml',
        "views/documents.xml",
        "views/menu_items_actions.xml",
        "views/project.xml",
        "views/employee.xml",
        "views/product_template.xml",
        "wizard/merge_type.xml",
        "wizard/merge_document.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "client_documents/static/src/widget.js",
            "client_documents/static/src/xml/pdf_preview_template.xml",
        ],
    },
    "installable": True,
    "application": False,
    "post_init_hook": "post_init_hook",
    "demo": [
        "demo_data_loader/demo_data.xml",
    ],
}
