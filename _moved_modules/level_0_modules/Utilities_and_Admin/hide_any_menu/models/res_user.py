from odoo import _, api, fields, models


class Users(models.Model):
    _inherit = "res.users"

    menu_ids = fields.Many2many(
        "ir.ui.menu",
        "user_menu_rel",
        "user_id",
        "menu_id",
        string="Menu To Hide",
        help="Select Menus To Hide From This User",
    )
    report_ids = fields.Many2many(
        "ir.actions.report",
        "user_report_rel",
        "user_id",
        "report_id",
        "Report To Hide",
        help="Select Report To Hide From This User",
    )

    # Earlier the user needed to restart the server for the change to take
    # effect. After multiple requests from users, we added a cache clear so
    # there is no need to restart the server.
    @api.model_create_multi
    def create(self, vals_list):
        self.env["ir.ui.menu"].clear_caches()
        return super(Users, self).create(vals_list)

    def write(self, values):
        self.env["ir.ui.menu"].clear_caches()
        return super(Users, self).write(values)


class ResGroups(models.Model):
    _inherit = "res.groups"

    menu_ids = fields.Many2many(
        "ir.ui.menu",
        "group_menu_rel",
        "group_id",
        "menu_id",
        string="Menu To Hide",
    )
    report_ids = fields.Many2many(
        "ir.actions.report",
        "group_report_rel",
        "group_id",
        "report_id",
        "Report To Hide",
        help="Select Report To Hide From This User",
    )

    # Earlier the user needed to restart the server for the change to take
    # effect. After multiple requests from users, we added a cache clear so
    # there is no need to restart the server.
    @api.model_create_multi
    def create(self, vals_list):
        self.env["ir.ui.menu"].clear_caches()
        return super(ResGroups, self).create(vals_list)

    def write(self, values):
        self.env["ir.ui.menu"].clear_caches()
        return super(ResGroups, self).write(values)


class IrActionsReport(models.Model):
    _inherit = "ir.actions.report"

    hide_user_ids = fields.Many2many(
        "res.users",
        "user_report_rel",
        "report_id",
        "user_id",
        string="Hide From Users",
    )
    hide_group_ids = fields.Many2many(
        "res.groups",
        "group_report_rel",
        "report_id",
        "group_id",
        string="Hide From Groups",
    )


class IrUiMenu(models.Model):
    _inherit = "ir.ui.menu"

    hide_group_ids = fields.Many2many(
        "res.groups",
        "group_menu_rel",
        "menu_id",
        "group_id",
        string="Hide From Groups",
    )
    hide_user_ids = fields.Many2many(
        "res.users",
        "user_menu_rel",
        "menu_id",
        "user_id",
        string="Hide From Users",
    )

    # Earlier the user needed to restart the server for the change to take
    # effect. After multiple requests from users, we added a cache clear so
    # there is no need to restart the server.
    @api.model_create_multi
    def create(self, vals_list):
        self.env["ir.ui.menu"].clear_caches()
        return super(IrUiMenu, self).create(vals_list)

    def write(self, values):
        self.env["ir.ui.menu"].clear_caches()
        return super(IrUiMenu, self).write(values)

    @api.model
    def search(self, domain, offset=0, limit=None, order=None):
        """Override to hide menus configured on the current user / user groups.

        The former *count* keyword argument has been removed from
        ``BaseModel.search`` in Odoo 18.
        Consequently, we drop it from the signature and no longer attempt to
        emulate it here; callers wanting a count should call
        ``search_count`` instead.
        """

        # Super‐admin (Internal UID 1) should always see all menus untouched.
        if self.env.user == self.env.ref("base.user_root"):
            return super().search(
                domain,
                offset=offset,
                limit=limit,
                order=order,
            )

        # Retrieve all menus first (ignore offset / limit so we can reliably
        # remove hidden ones and re-apply slicing afterwards).
        menus = super().search(domain, offset=0, limit=None, order=order)

        if menus:
            # Menus explicitly hidden on the user or any of its groups.
            hidden_menu_ids = (
                self.env.user.menu_ids  # direct on user
                | self.env.user.groups_id.mapped("menu_ids")  # through groups
            )

            menus -= hidden_menu_ids

        # Re-apply offset/limit as ``search`` would normally do.
        if offset:
            menus = menus[offset:]
        if limit is not None:
            menus = menus[:limit]

        return menus

    @api.model
    def search_count(self, domain, limit=None):
        """Ensure counts also respect menu hiding logic."""
        # For the super‐admin keep the default behaviour.
        if self.env.user == self.env.ref("base.user_root"):
            return super().search_count(domain, limit=limit)

        # Use our custom ``search`` which already applies hiding & slicing.
        return len(
            self.search(
                domain,
                offset=0,
                limit=limit,
            )
        )


class IrModel(models.Model):
    _inherit = "ir.model"

    field_configuration_ids = fields.One2many(
        "field.configuration", "model_id", string="Field Configuration"
    )


class FieldConfiguration(models.Model):
    _name = "field.configuration"
    _description = "Field Configuration"

    model_id = fields.Many2one(
        "ir.model", string="Model", required=True, ondelete="cascade"
    )
    field_id = fields.Many2one(
        "ir.model.fields", string="Field", required=True, ondelete="cascade"
    )
    field_name = fields.Char(
        related="field_id.name", string="Technical Name", readonly=True
    )
    group_ids = fields.Many2many(
        "res.groups",
        "field_config_group_rel",
        "group_id",
        "field_config_id",
        required=True,
        string="Groups",
    )
    readonly = fields.Boolean("ReadOnly", default=False)
    invisible = fields.Boolean("Invisible", default=False)

    _sql_constraints = [
        (
            "field_model_readonly_unique",
            "UNIQUE ( field_id, model_id, readonly)",
            _(
                "Readonly Attribute Is Already Added To This Field, "
                "You Can Add Group To This Field!",
            ),
        ),
        (
            "model_field_invisible_uniq",
            "UNIQUE (model_id, field_id, invisible)",
            _(
                "Invisible Attribute Is Already Added To This Field, "
                "You Can Add Group To This Field",
            ),
        ),
    ]
