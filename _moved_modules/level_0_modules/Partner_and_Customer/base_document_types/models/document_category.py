from odoo import fields, models


class ResPartnerDocumentCategory(models.Model):
    """Partner Document Category - Base Model
    
    This model defines categories for organizing document types.
    Extracted from client_documents to serve as a base module.
    """
    _name = "res.partner.document.category"
    _description = "Partner Document Category"
    _order = "name"

    name = fields.Char(
        string="Name",
        required=True,
        translate=True,
        help="Name of the document category"
    )
    
    description = fields.Text(
        string="Description",
        translate=True,
        help="Detailed description of the category"
    )
    
    active = fields.Boolean(
        string="Active",
        default=True,
        help="If unchecked, this category will be hidden"
    )
    
    document_ids = fields.One2many(
        comodel_name="res.partner.document",
        inverse_name="category_id",
        string="Documents",
        help="Documents in this category"
    )
    
    type_ids = fields.One2many(
        comodel_name="res.partner.document.type",
        inverse_name="category_id",
        string="Document Types",
        help="Document types in this category"
    )

    _sql_constraints = [
        ('name_unique', 'unique(name)', 'Category name must be unique!')
    ]
