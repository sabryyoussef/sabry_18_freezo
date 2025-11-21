# -*- coding: utf-8 -*-
{
    'name': "Crm Log",
    'author': "BeshoyWageh - Level 3",
    'version': '0.1',
    'depends': [
        'base',
        'crm',
        'sale',
        'sales_team',
        'base_document_types',  # Base module for document types
    ],
    'data': [
        'data/data.xml',
        'security/lead_security.xml',
        'security/ir.model.access.csv',
        'views/source.xml',
        'views/crm.xml',
        'views/sale.xml',
        'wizard/wizard.xml',
        'wizard/call.xml',
    ],
}
