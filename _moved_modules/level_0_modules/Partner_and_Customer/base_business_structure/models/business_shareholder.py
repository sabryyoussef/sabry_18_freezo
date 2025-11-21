from odoo import api, fields, models


class BusinessShareholder(models.Model):
    """Business Shareholder - Base Model
    
    Manages shareholder information for business entities.
    Extracted from compliance_cycle to serve as a base module.
    """
    _name = "res.partner.business.shareholder"
    _description = "Business Shareholder"
    _order = "project_id, shareholding desc"

    # Project and partner relations
    project_id = fields.Many2one(
        "project.project",
        string="Project",
        help="Related project"
    )
    
    customer_id = fields.Many2one(
        "res.partner",
        string="Customer",
        help="Customer associated with this shareholder"
    )
    
    partner_id = fields.Many2one(
        "res.partner",
        string="Partner",
        help="Partner (business entity) this shareholder belongs to"
    )
    
    contact_id = fields.Many2one(
        "res.partner",
        string="Contact",
        help="Contact person for this shareholder"
    )
    
    ubo_id = fields.Many2one(
        "res.partner.ubo",
        string="UBO",
        help="Ultimate Beneficial Owner designation"
    )

    # Shareholding information
    shareholding = fields.Float(
        string="Shareholding %",
        help="Percentage of ownership (0-100)"
    )
    
    relationship_ids = fields.Many2many(
        "business.relationships",
        string="Relationship",
        help="Types of relationships with the business"
    )

    # Contact information
    email = fields.Char(
        string="Email",
        help="Email address of the shareholder"
    )
    
    mobile = fields.Char(
        string="Mobile",
        help="Mobile phone number"
    )
    
    company_type = fields.Selection(
        [("person", "Individual"), ("company", "Company")],
        string="Company Type",
        default="person",
        help="Whether this is an individual or corporate shareholder"
    )

    # Individual information
    nationality_id = fields.Many2one(
        "res.country",
        string="Nationality",
        help="Nationality of the individual shareholder"
    )
    
    gender = fields.Selection(
        [("male", "Male"), ("female", "Female")],
        string="Gender",
        help="Gender of the individual shareholder"
    )

    # Corporate information
    license_authority_id = fields.Many2one(
        "product.attribute.value",
        string="License Authority",
        help="Licensing authority for corporate shareholders"
    )
    
    incorporation_date = fields.Date(
        string="Incorporation Date",
        help="Date of incorporation for corporate shareholders"
    )
    
    license_number = fields.Char(
        string="License Number",
        help="Business license number"
    )
    
    license_validity = fields.Selection(
        [
            ("1", "1 Year"),
            ("2", "2 Years"),
            ("3", "3 Years"),
            ("4", "4 Years"),
            ("5", "5 Years"),
            ("6", "6 Years"),
            ("7", "7 Years"),
            ("8", "8 Years"),
            ("9", "9 Years"),
            ("10", "10 Years"),
        ],
        string="License Validity",
        help="Duration of license validity"
    )

    # Document references
    passport = fields.Many2one(
        "res.partner.document",
        string="Passport",
        help="Passport document reference"
    )
    
    uae_resident = fields.Boolean(
        string="UAE Resident",
        help="Whether the shareholder is a UAE resident"
    )
    
    eid_copy = fields.Many2one(
        "res.partner.document",
        string="EID Copy",
        help="Emirates ID copy reference"
    )
    
    residence_visa_copy = fields.Many2one(
        "res.partner.document",
        string="Residence Visa Copy",
        help="Residence visa document reference"
    )
    
    current_visa = fields.Many2one(
        "res.partner.document",
        string="Current Visa",
        help="Current visa document reference"
    )
    
    entry_stamp = fields.Many2one(
        "res.partner.document",
        string="Entry Stamp",
        help="Entry stamp document reference"
    )
    
    trade_license = fields.Many2one(
        "res.partner.document",
        string="Trade License",
        help="Trade license document reference"
    )
    
    memorandum_association = fields.Many2one(
        "res.partner.document",
        string="Memorandum of Association",
        help="Memorandum of Association document reference"
    )
    
    apply_visa = fields.Boolean(
        string="Apply Visa",
        help="Whether to apply for a visa"
    )

    active = fields.Boolean(
        string="Active",
        default=True,
        help="If unchecked, this shareholder record will be hidden"
    )

    @api.onchange('contact_id')
    def _onchange_contact_id(self):
        """Auto-fill contact information from partner"""
        if self.contact_id:
            self.email = self.contact_id.email
            self.mobile = self.contact_id.mobile
            self.nationality_id = self.contact_id.country_id

    @api.constrains('shareholding')
    def _check_shareholding(self):
        """Validate shareholding percentage"""
        for record in self:
            if record.shareholding < 0 or record.shareholding > 100:
                from odoo.exceptions import ValidationError
                raise ValidationError("Shareholding must be between 0 and 100%")
