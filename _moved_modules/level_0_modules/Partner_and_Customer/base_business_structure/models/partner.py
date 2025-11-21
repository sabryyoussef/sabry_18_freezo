from odoo import api, fields, models
from odoo.exceptions import ValidationError


class Partner(models.Model):
    """Partner extension for business structure"""
    _inherit = "res.partner"

    compliance_shareholder_ids = fields.One2many(
        "res.partner.business.shareholder",
        "partner_id",
        string="Shareholders",
        help="Shareholders of this partner"
    )
    
    business_structure_id = fields.Many2one(
        "business.structure",
        string="Business Structure",
        help="Type of business structure"
    )

    @api.onchange("parent_partner_ids", "business_structure_id")
    def action_shareholder_lines(self):
        """Prepare shareholder lines based on parent partners"""
        self.prepare_shareholder_lines()

    def prepare_shareholder_lines(self):
        """Create shareholder records from parent partners"""
        for rec in self:
            # Only process if parent_partner_ids field exists (from partner_organization)
            if not hasattr(rec, 'parent_partner_ids'):
                continue
                
            existing_partner_ids = rec.compliance_shareholder_ids.mapped(
                "contact_id.id"
            )
            for partner in rec.parent_partner_ids:
                partner_id = partner._origin.id or partner.id
                if partner_id not in existing_partner_ids:
                    rec.compliance_shareholder_ids = [
                        (
                            0,
                            0,
                            {
                                "partner_id": rec.id,
                                "contact_id": partner_id,
                                "relationship_ids": rec.business_structure_id.relationships_ids.ids,
                            },
                        )
                    ]

    @api.constrains("compliance_shareholder_ids", "parent_partner_ids")
    def _check_data(self):
        """Validate shareholder data consistency"""
        for rec in self:
            # Only validate if parent_partner_ids field exists
            if not hasattr(rec, 'parent_partner_ids'):
                continue
                
            parent_ids = set(rec.parent_partner_ids.ids)
            shareholder_contact_ids = set(
                rec.compliance_shareholder_ids.mapped("contact_id.id")
            )
            if parent_ids != shareholder_contact_ids and not rec.project_id:
                raise ValidationError("Please remove the shareholder item first.")
