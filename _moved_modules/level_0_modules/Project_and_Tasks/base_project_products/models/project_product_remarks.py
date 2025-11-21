from odoo import fields, models


class ProjectProductRemarks(models.Model):
    """Project Product Remarks - Base Model
    
    Manages remarks for project-product associations.
    Extracted from freezoner_custom to serve as a base module.
    """
    _name = "project.project.products.remarks"
    _description = "Project Product Remarks"
    _order = "create_date desc"

    name = fields.Char(
        string="Remark",
        required=True,
        help="Remark text"
    )
    
    description = fields.Text(
        string="Description",
        help="Detailed description of the remark"
    )
    
    project_product_ids = fields.Many2many(
        "project.project.products",
        string="Project Products",
        help="Project products this remark applies to"
    )
    
    user_id = fields.Many2one(
        "res.users",
        string="User",
        default=lambda self: self.env.user,
        help="User who created this remark"
    )
    
    date = fields.Datetime(
        string="Date",
        default=fields.Datetime.now,
        help="Date of the remark"
    )
    
    active = fields.Boolean(
        default=True,
        help="If unchecked, this remark will be hidden"
    )
