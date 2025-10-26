# -*- coding: utf-8 -*-
{
    'name': 'Event Stub',
    'version': '18.0.1.0.0',
    'author': 'Freezoner Team',
    'category': 'Hidden',
    'summary': 'Stub module to provide event model placeholder for Odoo.sh compatibility',
    'description': """
        This is a minimal stub module that provides event model placeholder
        to resolve KeyError: 'event' issues on Odoo.sh staging environment.
        
        The Odoo.sh environment appears to be missing the event module,
        causing CSV import failures in other modules.
    """,
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
