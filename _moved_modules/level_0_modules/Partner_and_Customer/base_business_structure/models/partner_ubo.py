from odoo import fields, models


class PartnerUbo(models.Model):
    """Partner UBO (Ultimate Beneficial Owner) - Base Model
    
    Defines Ultimate Beneficial Owner types for compliance tracking.
    Extracted from compliance_cycle to serve as a base module.
    """
    _name = "res.partner.ubo"
    _description = "Ultimate Beneficial Owner"
    _order = "name"

    name = fields.Char(
        string="Name",
        required=True,
        translate=True,
        help="Name of the UBO type or category"
    )
    
    description = fields.Text(
        string="Description",
        translate=True,
        help="Detailed description of the UBO type"
    )
    
    active = fields.Boolean(
        string="Active",
        default=True,
        help="If unchecked, this UBO type will be hidden"
    )
    
    code = fields.Char(
        string="Code",
        help="Short code for the UBO type"
    )

    _sql_constraints = [
        ('name_unique', 'unique(name)', 'UBO type name must be unique!')
    ]
