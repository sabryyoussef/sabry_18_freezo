from odoo import api, fields, models
from odoo.exceptions import ValidationError


class Partner(models.Model):
    _inherit = "res.partner"

    # Fields compliance_shareholder_ids and business_structure_id are now
    # defined in base_business_structure module
    # Keeping only compliance-specific extensions here
    
    partner_address_lines = fields.One2many("res.partner.address", "partner_id")
    nationality_id = fields.Many2one("res.nationality", string="Nationality")
    project_id = fields.Many2one("project.project", string="Project")
    # project_product_ids now defined in base_project_products module

    @api.onchange("parent_id")
    def onchange_parent_id(self):
        # return values in result, as this method is used by _fields_sync()
        if not self.parent_id:
            return
        result = {}
        partner = self._origin
        if partner.parent_id and partner.parent_id != self.parent_id:
            pass
        if partner.type == "contact" or self.type == "contact":
            # for contacts: copy the parent address, if set (aka, at least one
            # value is set in the address: otherwise, keep the one from the
            # contact)
            address_fields = self._address_fields()
            if any(self.parent_id[key] for key in address_fields):

                def convert(value):
                    return value.id if isinstance(value, models.BaseModel) else value

                result["value"] = {
                    key: convert(self.parent_id[key]) for key in address_fields
                }
        return result

    @api.constrains("partner_address_lines")
    def _check_partner_address_lines(self):
        for rec in self:
            types = [line.type for line in rec.partner_address_lines]
            if len(types) != len(set(types)):
                raise ValidationError("The address type already exists .")

    @api.onchange("parent_partner_ids", "business_structure_id")
    def action_shareholder_lines(self):
        """Inherited from base_business_structure - add compliance-specific logic if needed"""
        self.prepare_shareholder_lines()

    def prepare_shareholder_lines(self):
        """Inherited from base_business_structure - add compliance-specific logic if needed"""
        # Call parent method
        return super().prepare_shareholder_lines()

    @api.constrains("compliance_shareholder_ids", "parent_partner_ids")
    def _check_data(self):
        """Inherited from base_business_structure - add compliance-specific logic if needed"""
        # Call parent method
        return super()._check_data()

    @api.depends("project_id")
    def _compute_project_product_ids(self):
        """Compute method now handled by base_project_products module"""
        # This method is defined in base_project_products module
        pass
