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
        "documents",
        "sale",
        "sale_project",
        "web",
        "client_documents",
        "hr_expense",
        "project",
        "crm",
        "cabinet_directory",
        "mass_mailing",
        "calendar",  # Required: Some dependency module references calendar fields during initialization
        "survey",  # Required for rating functionality used by bwa_survey
    ],
    "data": [
        "security/ir.model.access.csv",
        "security/res_groups.xml",
        "data/ir_sequence_data.xml",
        "data/cron.xml",
        "data/action.xml",
        "data/action_configure_email_servers.xml",
        "wizard/required_document_wizard.xml",
        "wizard/task_assignees_wizard.xml",
        "wizard/return_project_wizard.xml",
        "wizard/remarks_wizard.xml",
        # === GROUP 1: Document Views ===
        "views/document_request.xml",
        "views/documents.xml",  # Enabled - but problematic kanban views remain commented
        "views/document.xml",
        # === GROUP 2: Core Partner/Account/Product ===
        "views/partner.xml",
        "views/account_move.xml",
        "views/product.xml",
        # === GROUP 3: Project/Task/Expense ===
        "views/expense.xml",
        "views/project.xml",  # Complex - large file with many customizations
        "views/task.xml",     # Complex - large file with many customizations
        # === GROUP 4: CRM/Sale ===
        "views/crm.xml",
        "views/sale.xml",     # Complex - form inheritance with SOV and analytic items
        "views/sale_portal.xml",
        "views/rating.xml",
        # === Data/Mail Files ===
        "data/mails.xml",
        "data/data.xml",
        "data/survey_mail.xml",
        "data/crm_mails.xml",
        # === Wizards ===
        "wizard/task_wizard.xml",
        "wizard/task_next_wizard.xml",
        "wizard/sale_crm.xml",
        "wizard/update_fields.xml",
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
