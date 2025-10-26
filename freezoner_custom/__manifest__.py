{
    "name": "freezoner_custom",
    "version": "18.0.1.0.0",
    "author": "BeshoyWageh, Sabry Youssef",
    "category": "Custom",
    "summary": "Customizations for Freezoner",
    "description": "Module for Freezoner-specific customizations.",
    "depends": [
        "base",
        "mail",
        "account",
        "sale",
        "project",
        "web",
        "event_stub",  # ALTERNATIVE 1: Stub event module to resolve KeyError
        # TRIAL 4: Minimal dependencies - removed documents, hr_expense, crm
        # "documents",  # TRIAL 4: Removed for minimal test
        # "sale_project",  # TRIAL 4: Removed for minimal test
        # "client_documents",  # TRIAL 5: Removed - checking if it has event references
        # "hr_expense",  # TRIAL 4: Removed for minimal test
        # "crm",  # TRIAL 4: Removed for minimal test
        # "cabinet_directory",  # TRIAL 6: Removed - depends on calendar which references event
        # "mass_mailing",  # TRIAL 2: Removed - might have event/calendar integration
        # "survey",  # TRIAL 1: Removed - might require event/calendar functionality
    ],
    "data": [
        "security/ir.model.access.csv",
        "security/res_groups.xml",
        # TRIAL 4: Commented out most data files for minimal test
        # "data/ir_sequence_data.xml",
        # "data/cron.xml",
        # "data/action.xml",
        # "data/action_configure_email_servers.xml",
        # "wizard/required_document_wizard.xml",
        # "wizard/task_assignees_wizard.xml",
        # "wizard/return_project_wizard.xml",
        # "wizard/remarks_wizard.xml",
        # === GROUP 1: Document Views ===
        # "views/document_request.xml",
        # "views/documents.xml",  # Enabled - but problematic kanban views remain commented
        # "views/document.xml",
        # === GROUP 2: Core Partner/Account/Product ===
        # "views/partner.xml",
        # "views/account_move.xml",
        # "views/product.xml",
        # === GROUP 3: Project/Task/Expense ===
        # "views/expense.xml",
        # "views/project.xml",  # Complex - large file with many customizations
        # "views/task.xml",     # Complex - large file with many customizations
        # === GROUP 4: CRM/Sale ===
        # "views/crm.xml",
        # "views/sale.xml",     # Complex - form inheritance with SOV and analytic items
        # "views/sale_portal.xml",
        # "views/rating.xml",
        # === Data/Mail Files ===
        # "data/mails.xml",
        # "data/data.xml",
        # "data/survey_mail.xml",  # TRIAL 1: Commented out - survey dependency removed
        # "data/crm_mails.xml",
        # === Wizards ===
        # "wizard/task_wizard.xml",
        # "wizard/task_next_wizard.xml",
        # "wizard/sale_crm.xml",
        # "wizard/update_fields.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "freezoner_custom/static/src/js/fix_documents.js",
        ],
        "web.assets_frontend": [
            "freezoner_custom/static/src/css/rating.css",
            "freezoner_custom/static/src/js/rating.js",
        ],
    },
    "installable": True,
    "application": False,
    "auto_install": False,
}
