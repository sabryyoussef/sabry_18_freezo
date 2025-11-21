{
    "name": "Base Project Products",
    "version": "18.0.1.0.0",
    "category": "Base",
    "summary": "Project-product relationship management base module",
    "description": """
        Base Project Products
        =====================
        Provides core project-product relationship management.
        
        This module extracts shared project-product functionality to break
        circular dependencies between Level 3 modules.
        
        Main Features:
        - Project Product association (project.project.products)
        - Product remarks tracking
        - Partner-product relationships
    """,
    "author": "Freezoner",
    "website": "https://www.freezoner.com",
    "license": "LGPL-3",
    "depends": [
        "base",
        "project",
        "product",
        "mail",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/project_product_views.xml",
    ],
    "installable": True,
    "application": False,
    "auto_install": False,
}
