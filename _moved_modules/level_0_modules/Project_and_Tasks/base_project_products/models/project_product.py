from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class ProjectProduct(models.Model):
    """Project Product - Base Model
    
    Manages product associations with projects.
    Extracted from freezoner_custom to serve as a base module.
    """
    _name = "project.project.products"
    _description = "Project Products"
    _order = "project_id, product_id"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    # Basic Fields
    name = fields.Char(
        compute="_compute_name",
        store=True,
        string="Name",
        help="Computed name from project and product"
    )
    
    active = fields.Boolean(
        default=True,
        tracking=True,
        help="If unchecked, this product association will be hidden"
    )

    # Related Fields
    product_id = fields.Many2one(
        "product.product",
        string="Product",
        required=True,
        tracking=True,
        index=True,
        help="Product associated with the project"
    )
    
    project_id = fields.Many2one(
        "project.project",
        string="Project",
        required=True,
        tracking=True,
        index=True,
        help="Project this product is associated with"
    )
    
    partner_id = fields.Many2one(
        "res.partner",
        string="Customer",
        store=True,
        tracking=True,
        help="Customer for this project-product association"
    )

    # Related Records
    remarks_ids = fields.Many2many(
        "project.project.products.remarks",
        string="Remarks",
        tracking=True,
        help="Remarks related to this project-product"
    )

    # Computed Methods
    @api.depends("product_id", "project_id")
    def _compute_name(self):
        """Compute display name from project and product"""
        for record in self:
            if record.product_id and record.project_id:
                record.name = f"{record.project_id.name} - {record.product_id.name}"
            else:
                record.name = False

    # CRUD Methods
    @api.model_create_multi
    def create(self, vals_list):
        """Validate project-product combinations on create"""
        for vals in vals_list:
            if vals.get("project_id") and vals.get("product_id"):
                existing = self.search(
                    [
                        ("project_id", "=", vals["project_id"]),
                        ("product_id", "=", vals["product_id"]),
                        ("active", "=", True),
                    ]
                )
                if existing:
                    # Log warning but don't raise - allow duplicate for flexibility
                    _logger = __import__('logging').getLogger(__name__)
                    _logger.warning(
                        "Product %s already associated with project %s",
                        vals.get("product_id"),
                        vals.get("project_id")
                    )
        return super().create(vals_list)

    def write(self, vals):
        """Validate project-product combinations on update"""
        if "project_id" in vals or "product_id" in vals:
            for record in self:
                project_id = vals.get("project_id", record.project_id.id)
                product_id = vals.get("product_id", record.product_id.id)
                existing = self.search(
                    [
                        ("project_id", "=", project_id),
                        ("product_id", "=", product_id),
                        ("active", "=", True),
                        ("id", "!=", record.id),
                    ]
                )
                if existing:
                    # Log warning but don't raise
                    _logger = __import__('logging').getLogger(__name__)
                    _logger.warning(
                        "Product %s already associated with project %s",
                        product_id,
                        project_id
                    )
        return super().write(vals)

    @api.onchange("project_id")
    def _onchange_project_id(self):
        """Auto-fill partner from project"""
        for record in self:
            if record.project_id:
                record.partner_id = record.project_id.partner_id
            else:
                record.partner_id = False

    _sql_constraints = [
        (
            'project_product_unique',
            'unique(project_id, product_id)',
            'This product is already associated with this project!'
        )
    ]
