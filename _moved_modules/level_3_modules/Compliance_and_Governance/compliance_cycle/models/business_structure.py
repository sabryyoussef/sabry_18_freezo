from odoo import fields, models


class BusinessStructure(models.Model):
    _name = "business.structure"

    name = fields.Char(required=True)
    relationships_ids = fields.Many2many(
        "business.relationships", string="Business Relationships"
    )


class BusinessRelationships(models.Model):
    _name = "business.relationships"

    name = fields.Char(required=True)


class PartnerUbo(models.Model):
    _name = "res.partner.ubo"

    name = fields.Char(required=True)


class BusinessShareholder(models.Model):
    _name = "res.partner.business.shareholder"
    _description = "Business Shareholder"

    # Project and partner relations
    project_id = fields.Many2one("project.project", string="Project")
    customer_id = fields.Many2one("res.partner", string="Customer")
    partner_id = fields.Many2one("res.partner", string="Partner")
    contact_id = fields.Many2one("res.partner", string="Contact")
    ubo_id = fields.Many2one("res.partner.ubo", string="UBO")

    # Shareholding information
    shareholding = fields.Float(string="Shareholding")
    relationship_ids = fields.Many2many("business.relationships", string="Relationship")

    # Contact information
    email = fields.Char(string="Email")
    mobile = fields.Char(string="Mobile")
    company_type = fields.Selection(
        [("person", "Individual"), ("company", "Company")],
        string="Company Type",
        default="person",
    )

    # Individual information
    nationality_id = fields.Many2one("res.country", string="Nationality")
    gender = fields.Selection([("male", "Male"), ("female", "Female")], string="Gender")

    # Corporate information
    license_authority_id = fields.Many2one(
        "product.attribute.value", string="License Authority"
    )
    incorporation_date = fields.Date(string="Incorporation Date")
    license_number = fields.Char(string="License Number")
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
    )

    # Document references
    # documents_folder_id = fields.Many2one(
    #     "documents.folder", string="Documents Folder"
    # )
    passport = fields.Many2one("res.partner.document", string="Passport")
    uae_resident = fields.Boolean(string="UAE Resident")
    eid_copy = fields.Many2one("res.partner.document", string="EID Copy")
    residence_visa_copy = fields.Many2one(
        "res.partner.document", string="Residence Visa Copy"
    )
    current_visa = fields.Many2one("res.partner.document", string="Current Visa")
    entry_stamp = fields.Many2one("res.partner.document", string="Entry Stamp")
    trade_license = fields.Many2one("res.partner.document", string="Trade License")
    memorandum_association = fields.Many2one(
        "res.partner.document", string="Memorandum of Association"
    )
    apply_visa = fields.Boolean(string="Apply Visa")
