from odoo import api, fields, models


class Documents(models.Model):
    _inherit = "documents.document"

    onboarding_id = fields.Many2one("initial.client.onboarding", string="Onboarding")

    # Field expected by frontend DocumentsTypeIcon component
    is_request = fields.Boolean(
        string="Is Request",
        default=False,
        help="Indicates if this is a document request",
    )

    def isRequest(self):
        """Method expected by frontend DocumentsTypeIcon component."""
        self.ensure_one()
        return self.is_request


class ProductDocuments(models.Model):
    _inherit = "product.template.required.documents"

    rating_id = fields.Many2one("risk.rating", string="Rating")


class TaskRequiredLines(models.Model):
    _inherit = "task.document.required.lines"

    onboarding_id = fields.Many2one("initial.client.onboarding", string="Onboarding")
    document = fields.Binary(string="Document")

    def fitch_document(self):
        # Implement the logic for fetching documents
        for record in self:
            # Example logic: Fetch documents based on some criteria
            documents = self.env["documents.document"].search(
                [("onboarding_id", "=", record.onboarding_id.id)]
            )
            record.write({"document": documents.mapped("datas")})
