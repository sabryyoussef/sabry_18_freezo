{
    'name': "Project Custom",
    'author': "BeshoyWageh - Level 3",
    # 'version': '16.0',
    'depends': [
        'base',
        'mail',  # Required by return_project_wizard.py for mail.notification
        'project',  # Required by views for project.edit_project, project.view_task_form2
        'sale',  # Required by project.py for sale actions and views
        'account',  # Required by project.py for account.action_move_out_invoice_type
        'rating',  # Required by project.py for rating_data import
        'documents',  # Required by document.xml for documents.document_view_form
        'freezoner_custom',
        'compliance_cycle',
        'partner_custom',
        'client_documents',
        'partner_custom_fields',
    ],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/data.xml',
        'views/document.xml',
        'views/partner.xml',
        'views/project.xml',
        'views/project_fields.xml',
        'views/task.xml',
        'views/milestone.xml',
        'views/views.xml',
    ],
}
