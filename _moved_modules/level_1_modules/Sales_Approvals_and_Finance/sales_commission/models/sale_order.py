from odoo import models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    # Remove conflicting sov_ids field - freezoner_custom already provides it
    # sov_ids = fields.One2many("commission.sale.sov", "sale_id", ...)
