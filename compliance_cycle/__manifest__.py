# -*- coding: utf-8 -*-
{
    "name": "Compliance",
    "version": "18.0.1.0.0",
    "author": "Beshoy Wageh",
    # 'version': '16.0',
    "depends": [
        "base",
        "crm",
        "freezoner_custom",
        # "partner_organization",  # Enterprise module - temporarily disabled
        # "documents",  # Enterprise module - temporarily disabled
        # "crm_log",  # Enterprise module - temporarily disabled
        # "client_documents",  # Depends on enterprise modules - temporarily disabled
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
