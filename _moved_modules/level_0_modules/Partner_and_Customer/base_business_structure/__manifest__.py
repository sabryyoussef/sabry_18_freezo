{
    "name": "Base Business Structure",
    "version": "18.0.1.0.0",
    "category": "Base",
    "summary": "Business structure and shareholder management base module",
    "description": """
        Base Business Structure
        =======================
        Provides core business structure and shareholder management models.
        
        This module extracts shared business structure functionality to break
        circular dependencies between Level 3 modules.
        
        Main Features:
        - Business Structure definitions
        - Business Relationships management
        - Shareholder tracking (res.partner.business.shareholder)
        - Ultimate Beneficial Owner (UBO) management
    """,
    "author": "Freezoner",
    "website": "https://www.freezoner.com",
    "license": "LGPL-3",
    "depends": [
        "base",
        "contacts",
        "project",
        "partner_organization",
        "base_document_types",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/business_structure_views.xml",
        "views/shareholder_views.xml",
    ],
    "installable": True,
    "application": False,
    "auto_install": False,
}
