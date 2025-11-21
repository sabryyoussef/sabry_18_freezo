# -*- coding: utf-8 -*-
{
    "name": "Compliance",
    "version": "18.0.1.0.0",
    "author": "BeshoyWageh - Level 3",
    # 'version': '16.0',
    "depends": [
        "base",
        "crm",
        "partner_organization",
        "documents",
        "crm_log",
        "client_documents",
        "base_document_types",      # Base module for document types
        "base_business_structure",  # Base module for business structure
        "base_project_products",    # Base module for project products
    ],
    "data": [
        "security/security.xml",
        "security/ir.model.access.csv",
        "views/business_structure.xml",
        "views/compliance.xml",
        "views/partner.xml",
        "views/config.xml",
        "views/onboarding.xml",
    ],
    "installable": True,
    "application": False,
}
