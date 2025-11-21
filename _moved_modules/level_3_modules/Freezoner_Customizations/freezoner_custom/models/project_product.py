from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


from odoo import models, fields


class ProjectProduct(models.Model):
    """Project Product Extension
    Base model defined in base_project_products module
    """
    _inherit = "project.project.products"
    # Base model now defined in base_project_products
    # Keep only freezoner-specific extensions here
    
    # Action Methods
    def action_add_remarks(self):
        self.ensure_one()
        return {
            "name": _("Add Remarks"),
            "type": "ir.actions.act_window",
            "view_mode": "form",
            "res_model": "remarks.wizard",
            "context": {
                "default_line_id": self.id,
                "default_project_id": self.project_id.id,
                "default_product_id": self.product_id.id,
            },
            "view_id": self.env.ref("freezoner_custom.remarks_wizard_form_view").id,
            "target": "new",
        }
