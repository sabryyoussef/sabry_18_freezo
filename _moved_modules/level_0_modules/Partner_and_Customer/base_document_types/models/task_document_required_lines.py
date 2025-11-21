from odoo import fields, models


class TaskDocumentRequiredLines(models.Model):
    """Task Document Required Lines - Base Model
    
    This model manages mandatory documents for tasks.
    Extracted from freezoner_custom to serve as a base module.
    """
    _name = "task.document.required.lines"
    _description = "Task Document Required Lines"
    _order = "sequence, id"

    sequence = fields.Integer(
        string="Sequence",
        default=10,
        help="Order of document in the list"
    )
    
    name = fields.Char(
        string="Name",
        help="Name of the document line"
    )

    task_ids = fields.Many2one(
        "project.task",
        string="Task",
        ondelete="cascade",
        help="Related task"
    )
    
    document_id = fields.Many2one(
        "documents.document",
        string="Document",
        required=True,
        help="Related document"
    )
    
    issue_date = fields.Date(
        string="Issue Date",
        help="Date the document was issued"
    )
    
    project_id = fields.Many2one(
        "project.project",
        string="Project",
        required=True,
        ondelete="cascade",
        index=True,
        help="Related project"
    )
    
    attachment_ids = fields.Many2many(
        "ir.attachment",
        string="Attachments",
        help="Attached files for this document line"
    )
    
    document_type_id = fields.Many2one(
        "res.partner.document.type",
        string="Document Type",
        help="Type of document required"
    )
    
    is_required = fields.Boolean(
        string="Required",
        default=True,
        help="Whether this document is mandatory"
    )
    
    description = fields.Text(
        string="Description",
        help="Additional information about the document requirement"
    )
    
    validity_days = fields.Integer(
        string="Validity (Days)",
        help="Number of days the document remains valid"
    )

    is_required_expiration = fields.Boolean(
        string="Required Expiration",
        help="If true, the expiration date is required"
    )

    expiration_date = fields.Date(
        string="Expiration Date",
        help="Date the document expires"
    )

    is_verify = fields.Boolean(
        string="Verified",
        help="Indicates if the document has been verified"
    )

    partner_id = fields.Many2one(
        "res.partner",
        string="Partner",
        help="Related partner for this document line"
    )

    is_moved = fields.Boolean(
        string="Is Moved",
        help="Indicates if the document line has been moved or processed"
    )

    is_ready = fields.Boolean(
        string="Is Ready",
        help="Indicates if the document is ready for processing or verification"
    )
