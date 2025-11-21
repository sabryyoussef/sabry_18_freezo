from odoo import fields, models


class BusinessStructure(models.Model):
    """Business Structure Extension
    Base model defined in base_business_structure module
    """
    _inherit = "business.structure"
    # Add compliance-specific extensions here if needed


class BusinessRelationships(models.Model):
    """Business Relationships Extension
    Base model defined in base_business_structure module
    """
    _inherit = "business.relationships"
    # Add compliance-specific extensions here if needed


class PartnerUbo(models.Model):
    """Partner UBO Extension
    Base model defined in base_business_structure module
    """
    _inherit = "res.partner.ubo"
    # Add compliance-specific extensions here if needed


class BusinessShareholder(models.Model):
    """Business Shareholder Extension
    Base model defined in base_business_structure module
    """
    _inherit = "res.partner.business.shareholder"
    # Add compliance-specific extensions here if needed
