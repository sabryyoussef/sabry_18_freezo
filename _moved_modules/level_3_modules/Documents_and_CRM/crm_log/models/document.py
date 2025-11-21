from odoo import models, fields

class ResPartnerDocumentType(models.Model):
    _inherit = 'res.partner.document.type'
    # Extended functionality for partner document type
    # Base model defined in base_document_types module
    # Removed duplicate model definition - now inherits from base 