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
    
    document_ids = fields.One2many(
        comodel_name="res.partner.document",
        inverse_name="type_id",
        string="Documents",
        help="Documents using this type"
    )
    
    main_document_ids = fields.Many2many(
        "documents.document",
        compute="_compute_main_document_ids",
        string="Main Documents",
        help="Related documents from the documents module"
    )

    def _compute_main_document_ids(self):
        """Compute related documents from documents module"""
        for rec in self:
            lst = []
            if 'documents.document' in self.env:
                try:
                    documents = self.env["documents.document"].search([
                        '|',
                        ('name', 'ilike', rec.name),
                        ('partner_id', 'in', rec.document_ids.mapped('partner_id').ids)
                    ])
                    lst = documents.ids
                except Exception:
                    lst = []
            rec.main_document_ids = lst

    _sql_constraints = [
        ('code_unique', 'unique(code)', 'Document type code must be unique!')
    ]
