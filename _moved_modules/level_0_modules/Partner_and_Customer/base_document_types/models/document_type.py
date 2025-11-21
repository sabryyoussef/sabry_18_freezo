from odoo import fields, models


class ResPartnerDocumentType(models.Model):
    """Partner Document Type - Base Model
    
    This model defines document types that can be associated with partners.
    It's extracted from client_documents and crm_log to serve as a base
    for other modules without creating circular dependencies.
    """
    _name = "res.partner.document.type"
    _description = "Partner Document Type"
    _order = "name"

    name = fields.Char(
        string="Name",
        required=True,
        translate=True,
        help="Name of the document type"
    )
    
    code = fields.Char(
        string="Code",
        help="Short code for the document type"
    )
    
    description = fields.Text(
        string="Description",
        translate=True,
        help="Detailed description of the document type"
    )
    
    active = fields.Boolean(
        string="Active",
        default=True,
        help="If unchecked, this document type will be hidden"
    )
    
    category_id = fields.Many2one(
        comodel_name="res.partner.document.category",
        string="Category",
        help="Category this document type belongs to"
    )

    _sql_constraints = [
        ('code_unique', 'unique(code)', 'Document type code must be unique!')
    ]
