from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class ClientDocumentsCategory(models.Model):
    _name = "res.partner.document.category"
    _description = "Client Document Category"
    _rec_name = "name"

    name = fields.Char()
    document_ids = fields.One2many(
        comodel_name="res.partner.document", inverse_name="category_id"
    )


class ClientDocumentsType(models.Model):
    _name = "res.partner.document.type"
    _description = "Client Document Type"

    name = fields.Char()
    category_id = fields.Many2one(comodel_name="res.partner.document.category")
    document_ids = fields.One2many(
        comodel_name="res.partner.document", inverse_name="type_id"
    )
    main_document_ids = fields.Many2many(
        "documents.document", compute="_compute_main_document_ids"
    )

    def _compute_main_document_ids(self):
        for rec in self:
            lst = []
            # Check if documents module is installed before trying to access it
            if 'documents.document' in self.env:
                try:
                    # Note: documents.document doesn't have type_id field by default
                    # This would need custom integration if you want to link them
                    # For now, we'll look for documents that might be related by name or other means
                    documents = self.env["documents.document"].search([
                        '|',
                        ('name', 'ilike', rec.name),
                        ('partner_id', 'in', rec.document_ids.mapped('partner_id').ids)
                    ])
                    lst = documents.ids
                except Exception:
                    # If there's any error with the documents module, just set empty list
                    lst = []
            rec.main_document_ids = lst


class ClientDocuments(models.Model):
    _name = "res.partner.document"
    _description = "Client Document"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char(required=True, tracking=True)
    number = fields.Char(
        string="Number",
        required=True,
        copy=False,
        readonly=True,
        index=True,
        default=lambda self: _("New"),
        tracking=True,
    )
    attachment_ids = fields.Many2many(
        "ir.attachment", string="Document", required=True, tracking=True
    )
    issue_date = fields.Date(
        required=False,
        default=fields.Date.today,
        tracking=True,
        help="Date when the document was issued",
    )
    type_id = fields.Many2one(comodel_name="res.partner.document.type", tracking=True)
    expiration_date = fields.Date(tracking=True)

    category_id = fields.Many2one(
        comodel_name="res.partner.document.category", string="Category"
    )

    partner_id = fields.Many2one(
        comodel_name="res.partner", required=True, tracking=True
    )
    expiration_reminder = fields.Boolean(default=False, tracking=True)
    document = fields.Char(tracking=True)
    expiration_reminder_sent = fields.Boolean(default=False, tracking=True)
    is_verify = fields.Boolean("Is Verify", tracking=True)
    show_verified_ribbon = fields.Boolean("Show Verified Ribbon", compute="_compute_show_verified_ribbon", store=True)
    document_create_date = fields.Datetime(
        readonly=True,
        string="Document Create Date",
        default=fields.datetime.now(),
        tracking=True,
    )

    # Field expected by frontend DocumentsTypeIcon component
    is_request = fields.Boolean(
        string="Is Request",
        default=False,
        help="Indicates if this is a document request " "(False for regular documents)",
    )

    def action_numbers(self):
        docs = self.env["res.partner.document"].sudo().search([])
        for doc in docs:
            doc.number = self.env["ir.sequence"].next_by_code(
                "res.partner.document"
            ) or _("New")

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if "number" not in vals:
                vals["number"] = self.env["ir.sequence"].next_by_code(
                    "res.partner.document"
                ) or _("New")
        return super(ClientDocuments, self).create(vals_list)

    @api.constrains("partner_id", "issue_date", "type_id")
    def check_duplicate_document(self):
        if self.env.context.get("bypass_duplicate_check"):
            return
        for rec in self:
            duplicate_document = self.search(
                [
                    ("partner_id", "=", rec.partner_id.id),
                    ("issue_date", "=", rec.issue_date),
                    ("type_id", "=", rec.type_id.id),
                    ("id", "!=", rec.id),
                ]
            )
            if duplicate_document:
                raise ValidationError("This document already exists!")

    def write(self, vals):
        res = super(ClientDocuments, self).write(vals)
        if vals.get("expiration_date"):
            self.write({"expiration_reminder_sent": False})
        if vals.get("attachment_ids"):
            self.write({"document_create_date": fields.Datetime.today()})
        return res

    @api.depends('is_verify')
    def _compute_show_verified_ribbon(self):
        """Compute whether to show the verified ribbon"""
        for record in self:
            record.show_verified_ribbon = record.is_verify

    def isRequest(self):
        """
        Method expected by frontend DocumentsTypeIcon component.
        Returns the value of is_request field.
        """
        self.ensure_one()
        return self.is_request


class Client(models.Model):
    _inherit = "res.partner"

    document_ids = fields.One2many(
        comodel_name="res.partner.document", inverse_name="partner_id"
    )
    documents_count = fields.Integer(compute="_compute_total_documents")

    @api.depends("document_ids")
    def _compute_total_documents(self):
        for rec in self:
            rec.documents_count = len(rec.document_ids.ids)

    def action_view_documents(self):
        action = {
            "type": "ir.actions.act_window",
            "domain": [("partner_id", "=", self.id)],
            "context": {"default_partner_id": self.id},
            "view_mode": "list,kanban,form",
            "name": f"{self.name}'s Documents",
            # Note: view_ids format: [(kanban_view, 'kanban'), (tree_view, 'tree'), (False, 'form')]
            "res_model": "res.partner.document",
        }
        return action

    def action_see_documents(self):
        self.ensure_one()
        return {
            "name": _("Documents"),
            "domain": [("partner_id", "=", self.id)],
            "res_model": "documents.document",
            "type": "ir.actions.act_window",
            "views": [(False, "kanban")],
            "view_mode": "kanban",
            "context": {
                "default_partner_id": self.id,
                "searchpanel_default_folder_id": True,
                # Fix: Ensure documents_unique_folder_id is not a boolean
                "no_documents_unique_folder_id": True,
            },
        }


class DocumentsDocumentFix(models.Model):
    """
    Fix for documents_unique_folder_id context issue
    This prevents the RPC error when the context contains a boolean instead of integer
    """
    _inherit = 'documents.document'

    @api.model
    def search_panel_select_range(self, field_name, **kwargs):
        """Override to fix documents_unique_folder_id context issue"""
        if field_name == 'folder_id':
            # Fix the documents_unique_folder_id context issue
            context = self.env.context.copy()
            unique_folder_id = context.get('documents_unique_folder_id')
            
            # If unique_folder_id is a boolean, remove it from context
            if isinstance(unique_folder_id, bool):
                context.pop('documents_unique_folder_id', None)
                self = self.with_context(context)
            
            # Call the original method with fixed context
            return super(DocumentsDocumentFix, self).search_panel_select_range(field_name, **kwargs)
        
        return super().search_panel_select_range(field_name, **kwargs)
