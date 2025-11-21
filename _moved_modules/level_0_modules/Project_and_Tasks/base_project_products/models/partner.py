from odoo import api, fields, models


class Partner(models.Model):
    """Partner extension for project products"""
    _inherit = "res.partner"

    project_product_ids = fields.One2many(
        "project.project.products",
        "partner_id",
        string="Project Products",
        help="Products associated with projects for this partner"
    )

    @api.depends("project_id")
    def _compute_project_product_ids(self):
        """Compute project products based on partner's project"""
        for rec in self:
            if rec.project_id:
                rec.project_product_ids = self.env["project.project.products"].search(
                    [("project_id", "=", rec.project_id.id)]
                )
            else:
                rec.project_product_ids = False
