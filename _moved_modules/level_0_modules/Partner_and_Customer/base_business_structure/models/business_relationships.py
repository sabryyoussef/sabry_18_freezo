from odoo import fields, models


class BusinessRelationships(models.Model):
    """Business Relationships - Base Model
    
    Defines relationship types between business entities.
    Extracted from compliance_cycle to serve as a base module.
    """
    _name = "business.relationships"
    _description = "Business Relationships"
    _order = "name"

    name = fields.Char(
        string="Name",
        required=True,
        translate=True,
        help="Name of the relationship type (e.g., Parent Company, Subsidiary)"
    )
    
    description = fields.Text(
        string="Description",
        translate=True,
        help="Detailed description of the relationship"
    )
    
    active = fields.Boolean(
        string="Active",
        default=True,
        help="If unchecked, this relationship type will be hidden"
    )
    
    code = fields.Char(
        string="Code",
        help="Short code for the relationship"
    )

    _sql_constraints = [
        ('name_unique', 'unique(name)', 'Relationship name must be unique!')
    ]
