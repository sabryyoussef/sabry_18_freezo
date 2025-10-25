from odoo import api, fields, models


class PartnerStage(models.Model):
    _name = "partner.stage"
    _description = "Partner Stages"
    _order = "sequence"

    name = fields.Char(string="Stage Name", required=True)
    sequence = fields.Integer(default=1)
    fold = fields.Boolean(string="Folded in Kanban")
    active = fields.Boolean(default=True)
