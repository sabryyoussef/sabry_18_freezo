{
    "name": "Base Document Types",
    "version": "18.0.1.0.0",
    "category": "Base",
    "summary": "Document type management base module",
    "description": """
        Base Document Types
        ===================
        Provides core document type models for partner and task documents.
        
        This module extracts shared document type functionality to break
        circular dependencies between Level 3 modules.
        
        Main Features:
        - Partner Document Types (res.partner.document.type)
        - Partner Document Categories (res.partner.document.category)
        - Task Document Required Lines (task.document.required.lines)
    """,
    "author": "Freezoner",
    "website": "https://www.freezoner.com",
    "license": "LGPL-3",
    "depends": [
        "base",
        "contacts",
        "documents",
        "project",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/document_type_views.xml",
    ],
    "installable": True,
    "application": False,
    "auto_install": False,
}
