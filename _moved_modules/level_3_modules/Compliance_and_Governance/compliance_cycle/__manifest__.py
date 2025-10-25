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
        "partner_organization",
        "documents",
        "crm_log",
        "client_documents",
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
