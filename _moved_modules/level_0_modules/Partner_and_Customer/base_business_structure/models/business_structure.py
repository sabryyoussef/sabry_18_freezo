from odoo import fields, models


class BusinessStructure(models.Model):
    """Business Structure - Base Model
    
    Defines the organizational structure types for businesses.
    Extracted from compliance_cycle to serve as a base module.
    """
    _name = "business.structure"
    _description = "Business Structure"
    _order = "name"

    name = fields.Char(
        string="Name",
        required=True,
        translate=True,
        help="Name of the business structure type (e.g., LLC, Corporation)"
    )
    
    description = fields.Text(
        string="Description",
        translate=True,
        help="Detailed description of the business structure"
    )
    
    relationships_ids = fields.Many2many(
        "business.relationships",
        string="Business Relationships",
        help="Types of relationships allowed in this structure"
    )
    
    active = fields.Boolean(
        string="Active",
        default=True,
        help="If unchecked, this structure type will be hidden"
    )
    
    code = fields.Char(
        string="Code",
        help="Short code for the business structure"
    )

    _sql_constraints = [
        ('name_unique', 'unique(name)', 'Business structure name must be unique!')
    ]
