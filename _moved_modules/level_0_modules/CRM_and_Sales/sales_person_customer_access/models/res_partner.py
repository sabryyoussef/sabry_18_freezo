from odoo import _, api, models
from odoo.exceptions import UserError


class ResPartner(models.Model):
    _inherit = "res.partner"

    @api.model
    def _search(self, domain, offset=0, limit=None, order=None):
        restricted_customer = self.env.user.has_group(
            "sales_person_customer_access.group_restricted_customer"
        )
        if restricted_customer:
            domain = [("user_id", "=", self.env.user.id)] + list(domain)
        return super(ResPartner, self)._search(
            domain, offset=offset, limit=limit, order=order
        )

    @api.model_create_multi
    def create(self, vals):
        if not self.env.user.has_group(
            "sales_person_customer_access.group_create_customer"
        ):
            raise UserError(_("You don't have permission to create contacts."))
        res = super(ResPartner, self).create(vals)
        return res
