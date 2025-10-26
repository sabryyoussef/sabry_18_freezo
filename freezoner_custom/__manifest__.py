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
        # INCREMENT 1: Minimal base module - testing basic structure
        # "account",  # Will add in Increment 2
        # "documents",  # Will add in Increment 4
        # "sale",  # Will add in Increment 2
        # "sale_project",  # Will add in Increment 5
        # "web",  # Will add in Increment 2
        # "client_documents",  # Will add in Increment 6
        # "hr_expense",  # Will add in Increment 7
        # "project",  # Will add in Increment 2
        # "crm",  # Will add in Increment 7
        # "cabinet_directory",  # Will add in Increment 6
        # "mass_mailing",  # Will add in Increment 8
        # "calendar",  # Will add later - suspected cause of KeyError
        # "survey",  # Will add in Increment 9
        # "base_address_extended",  # Will add later - not available on Odoo.sh
    ],
    "data": [
        # INCREMENT 1: No data files - testing basic module structure
        # "security/ir.model.access.csv",  # Will add in Increment 3
        # "security/res_groups.xml",  # Will add in Increment 3
        # "data/ir_sequence_data.xml",  # Will add in Increment 10
        # "data/cron.xml",  # Will add in Increment 10
        # "data/ir_sequence_data.xml",  # Will add in Increment 10
        # "data/cron.xml",  # Will add in Increment 10
        # "data/action.xml",  # Will add in Increment 10
        # "data/action_configure_email_servers.xml",  # Will add in Increment 10
        # "wizard/required_document_wizard.xml",  # Will add in Increment 10
        # "wizard/task_assignees_wizard.xml",  # Will add in Increment 10
        # "wizard/return_project_wizard.xml",  # Will add in Increment 10
        # "wizard/remarks_wizard.xml",  # Will add in Increment 10
        # === GROUP 1: Document Views ===
        # "views/document_request.xml",  # Will add in Increment 10
        # "views/documents.xml",  # Will add in Increment 10
        # "views/document.xml",  # Will add in Increment 10
        # === GROUP 2: Core Partner/Account/Product ===
        # "views/partner.xml",  # Will add in Increment 10
        # "views/account_move.xml",  # Will add in Increment 10
        # "views/product.xml",  # Will add in Increment 10
        # === GROUP 3: Project/Task/Expense ===
        # "views/expense.xml",  # Will add in Increment 10
        # "views/project.xml",  # Will add in Increment 10
        # "views/task.xml",  # Will add in Increment 10
        # === GROUP 4: CRM/Sale ===
        # "views/crm.xml",  # Will add in Increment 10
        # "views/sale.xml",  # Will add in Increment 10
        # "views/sale_portal.xml",  # Will add in Increment 10
        # "views/rating.xml",  # Will add in Increment 10
        # === Data/Mail Files ===
        # "data/mails.xml",  # Will add in Increment 10
        # "data/data.xml",  # Will add in Increment 10
        # "data/survey_mail.xml",  # Will add in Increment 10
        # "data/crm_mails.xml",  # Will add in Increment 10
        # === Wizards ===
        # "wizard/task_wizard.xml",  # Will add in Increment 10
        # "wizard/task_next_wizard.xml",  # Will add in Increment 10
        # "wizard/sale_crm.xml",  # Will add in Increment 10
        # "wizard/update_fields.xml",  # Will add in Increment 10
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
