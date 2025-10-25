from odoo import models, fields

class ResPartnerDocumentType(models.Model):
    _name = 'res.partner.document.type'
    _description = 'Partner Document Type'

    name = fields.Char(string='Name', required=True)
    code = fields.Char(string='Code')
    description = fields.Text(string='Description')
    active = fields.Boolean(default=True) 