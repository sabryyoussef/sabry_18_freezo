{
    'name': 'Error Reporter Enterprise',
    'version': '18.0.1.0.0',
    'category': 'Tools',
    'summary': 'Professional error reporting and tracking system for Odoo',
    'description': """
        Automatic Error Reporter - Complete Error Management Solution
        
        This module provides comprehensive automatic error tracking from multiple sources:
        • Automatic JavaScript error capture from Odoo UI
        • Server log integration with real-time monitoring
        • Manual error reporting API for external tools and tests
        • Rich analytics dashboard with filtering and search
        • Professional PDF reports for error analysis
        • Multi-environment support (local, server, Odoo.sh)
        • Log file linking and line number tracking
        • Real-time error monitoring and management
        • Watch the full video demo: https://youtu.be/wXnRhGiVZF4
    """,
    'author': 'Sabry Youssef',
    'website': 'https://edu-sabry.odoo.com/error-reporter-enterprise',
    'license': 'LGPL-3',
    'price': 500.00,
    'currency': 'USD',
    'live_test_url': 'https://youtu.be/wXnRhGiVZF4',
    'depends': ['base', 'web', 'mail'],
    'external_dependencies': {
        'python': ['requests'],
    },
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/qa_error_event_views.xml',
        'views/qa_error_event_actions.xml',
        'views/github_config_views.xml',
        'views/qa_error_event_menus.xml',
        'views/qa_error_reports.xml',
        'views/log_handler_views.xml',
        'data/qa_error_data.xml',
        'data/log_demo_data.xml',
        'data/shortcuts.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'error_reporter_enterprise/static/src/js/error_tap.js',
        ],
        'web.assets_backend': [
            'error_reporter_enterprise/static/src/js/systray_error_button.js',
            'error_reporter_enterprise/static/src/xml/systray_error_button.xml',
        ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
}