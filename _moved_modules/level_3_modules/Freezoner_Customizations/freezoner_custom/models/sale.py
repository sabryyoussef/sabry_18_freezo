# Part of Odoo. See LICENSE file for full copyright and licensing details.

from collections import defaultdict
from datetime import timedelta
from itertools import chain, starmap, zip_longest

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError
from odoo.tools import is_html_empty


class SaleOrder(models.Model):
    _inherit = "sale.order"

    sequence = fields.Integer(string="Sequence", default=10)
    analytic_account_id = fields.Many2one(
        "account.analytic.account",
        string="Analytic Account",
        copy=False,
        check_company=True,
        domain=lambda self: [
            "|",
            ("company_id", "=", False),
            ("company_id", "=", self.company_id.id),
        ],
    )
    amount = fields.Float(
        string="Amount",
        compute="_compute_amount",
        store=True,
        digits=(16, 2),
    )
    date = fields.Date(
        string="Date",
        default=fields.Date.context_today,
        copy=False,
    )
    sale_order_template_id = fields.Many2one(
        comodel_name="sale.order.template",
        string="Quotation Template",
        compute="_compute_sale_order_template_id",
        store=True,
        readonly=False,
        check_company=True,
        precompute=True,
        domain="[('company_id', '=', False), ('company_id', '=', company_id)]",
    )
    sale_order_option_ids = fields.One2many(
        comodel_name="sale.order.option",
        inverse_name="order_id",
        string="Optional Products Lines",
        copy=True,
    )
    payment_status = fields.Selection(
        [
            ("pending", "Pending"),
            ("paid", "Paid"),
            ("failed", "Failed"),
        ],
        string="Payment Status",
        default="pending",
        help="Indicates the payment status of the sale order.",
    )
    sov_ids = fields.One2many(
        comodel_name="sale.sov",
        inverse_name="sale_id",
        string="SOV Lines",
    )
    analytic_item_ids = fields.One2many(
        comodel_name="sale.order.analytic.item",
        inverse_name="sale_order_id",
        string="Analytic Items",
    )
    date_confirmed = fields.Date(
        string="Confirmed Date",
        compute="_compute_date_confirmed",
        store=True,
    )

    # === MISSING FIELDS FROM ODOO 16 === #
    active = fields.Boolean(default=True, copy=False, tracking=True)
    system_expiry_date = fields.Date(string="System Expiry Date", copy=False)

    # Override state field with custom selection
    state = fields.Selection(
        selection=[
            ("draft", "Pro-forma Invoice"),
            ("sent", "Pro-forma Invoice Sent"),
            ("sale", "Pro-forma Confirm"),
            ("done", "Locked"),
            ("cancel", "Cancelled"),
        ],
        string="Status",
        readonly=True,
        copy=False,
        index=True,
        tracking=3,
        default="draft",
    )

    payment_method = fields.Selection(
        selection=[
            ("bank", "Bank"),
            ("visa", "Stripe"),
        ],
        string="Payment Method",
        tracking=3,
        default="bank",
        required=True,
    )

    total_revenue = fields.Float(
        string="Total Revenue", compute="get_total_revenue", store=True
    )
    total_planned_expenses = fields.Float(
        string="Total Planned Expenses",
        compute="get_total_planned_expenses",
        store=True,
    )
    total_net_achievement = fields.Float(
        string="Total Net Achievement", compute="get_total_net_achievement", store=True
    )

    # Override validity_date with custom compute
    validity_date = fields.Date(
        string="Expiration",
        compute="_compute_validity_date_custom",
        store=True,
        readonly=True,
        copy=False,
        precompute=True,
    )

    is_expired = fields.Boolean(compute="check_is_expired")

    # Task Management
    tasks_ids = fields.Many2many(
        "project.task",
        string="Related Tasks",
        compute="_compute_tasks_ids",
        help="All tasks related to this sale order through projects",
    )
    tasks_count = fields.Integer(
        string="Tasks Count",
        compute="_compute_tasks_ids",
        help="Number of tasks related to this sale order",
    )
    closed_task_count = fields.Integer(
        string="Closed Tasks Count",
        compute="_compute_tasks_ids",
        help="Number of closed tasks related to this sale order",
    )

    # === COMPUTE METHODS === #

    @api.depends("analytic_item_ids.amount")
    def _compute_amount(self):
        for order in self:
            order.amount = sum(order.analytic_item_ids.mapped("amount"))

    def _compute_sale_order_template_id(self):
        for order in self:
            company_template = order.company_id.sale_order_template_id
            has_diff_template = (
                company_template and order.sale_order_template_id != company_template
            )
            if has_diff_template:
                if hasattr(order, "website_id") and order.website_id:
                    continue
                order.sale_order_template_id = company_template.id

    @api.depends("partner_id", "sale_order_template_id")
    def _compute_note(self):
        super()._compute_note()
        for order in self.filtered("sale_order_template_id"):
            template = order.sale_order_template_id.with_context(
                lang=order.partner_id.lang
            )
            order.note = (
                template.note if not is_html_empty(template.note) else order.note
            )

    @api.depends("sale_order_template_id")
    def _compute_require_signature(self):
        super()._compute_require_signature()
        for order in self.filtered("sale_order_template_id"):
            order.require_signature = order.sale_order_template_id.require_signature

    @api.depends("sale_order_template_id")
    def _compute_require_payment(self):
        super()._compute_require_payment()
        for order in self.filtered("sale_order_template_id"):
            order.require_payment = order.sale_order_template_id.require_payment

    @api.depends("sale_order_template_id")
    def _compute_prepayment_percent(self):
        super()._compute_prepayment_percent()
        for order in self.filtered("sale_order_template_id"):
            if order.require_payment:
                order.prepayment_percent = (
                    order.sale_order_template_id.prepayment_percent
                )

    @api.depends("sale_order_template_id")
    def _compute_validity_date(self):
        super()._compute_validity_date()
        for order in self.filtered("sale_order_template_id"):
            validity_days = order.sale_order_template_id.number_of_days
            if validity_days > 0:
                order.validity_date = fields.Date.context_today(order) + timedelta(
                    validity_days
                )

    @api.depends("sale_order_template_id")
    def _compute_journal_id(self):
        super()._compute_journal_id()
        for order in self.filtered("sale_order_template_id"):
            order.journal_id = order.sale_order_template_id.journal_id

    @api.depends("state", "date_order")
    def _compute_date_confirmed(self):
        for order in self:
            # Set confirmed date if order is confirmed (state 'sale' or 'done')
            order.date_confirmed = (
                order.date_order if order.state in ["sale", "done"] else False
            )

    @api.depends("validity_date")
    def check_is_expired(self):
        for rec in self:
            if (
                rec.validity_date
                and rec.state in ["draft", "sent"]
                and rec.validity_date < fields.Date.context_today(self)
            ):
                rec.is_expired = True
            else:
                rec.is_expired = False

    @api.depends("create_date")
    def _compute_validity_date_custom(self):
        for order in self:
            if order.create_date:
                order.validity_date = order.create_date + timedelta(days=30)
            else:
                order.validity_date = False

    @api.depends("message_ids")
    def get_first_confirmed_date(self):
        for rec in self:
            first_confirmed_date = None
            for line in rec.message_ids:
                is_confirmed = line.subtype_id.description == "Quotation confirmed"
                if is_confirmed and (
                    not first_confirmed_date or line.date < first_confirmed_date
                ):
                    first_confirmed_date = line.date
            rec.date_confirmed = first_confirmed_date

    def get_analytic_item_ids(self):
        for rec in self:
            analytic_item_ids = (
                self.env["account.analytic.line"]
                .sudo()
                .search([("account_id.name", "ilike", rec.name)])
                .ids
            )
            if analytic_item_ids:
                rec.analytic_item_ids = analytic_item_ids
            else:
                rec.analytic_item_ids = []

    @api.depends("sov_ids", "sov_ids.revenue")
    def get_total_revenue(self):
        for rec in self:
            rec.total_revenue = sum(line.revenue for line in rec.sov_ids)

    @api.depends("sov_ids", "sov_ids.planned_expenses")
    def get_total_planned_expenses(self):
        for rec in self:
            rec.total_planned_expenses = sum(
                line.planned_expenses for line in rec.sov_ids
            )

    @api.depends("sov_ids", "sov_ids.net")
    def get_total_net_achievement(self):
        for rec in self:
            rec.total_net_achievement = sum(line.net for line in rec.sov_ids)

    @api.depends("project_ids", "project_ids.task_ids")
    def _compute_tasks_ids(self):
        for order in self:
            all_tasks = self.env["project.task"]
            for project in order.project_ids:
                all_tasks |= project.task_ids
            order.tasks_ids = all_tasks
            order.tasks_count = len(all_tasks)
            # Count closed tasks (tasks in done/closed states)
            closed_tasks = all_tasks.filtered(lambda t: t.stage_id.fold)
            order.closed_task_count = len(closed_tasks)

    # === CONSTRAINT METHODS === #

    @api.constrains("company_id", "sale_order_option_ids")
    def _check_optional_product_company_id(self):
        for order in self:
            companies = order.sale_order_option_ids.mapped("product_id.company_id")
            if companies and any(c != order.company_id for c in companies):
                bad_products = order.sale_order_option_ids.mapped(
                    "product_id"
                ).filtered(lambda p: p.company_id and p.company_id != order.company_id)
                raise ValidationError(
                    _(
                        "Your quotation contains products from company %(product_company)s whereas your quotation belongs to company %(quote_company)s.\n"
                        "Please change the company of your quotation or remove the products from other companies (%(bad_products)s).",
                        product_company=", ".join(companies.mapped("display_name")),
                        quote_company=order.company_id.display_name,
                        bad_products=", ".join(bad_products.mapped("display_name")),
                    )
                )

    # === MISSING CONSTRAINT METHODS FROM ODOO 16 === #

    @api.constrains("partner_id")
    def check_partner(self):
        for rec in self:
            user = self.env.user
            team = self.env["crm.team"].sudo().search([("id", "=", 1)])
            if team and user.id in team.member_ids.ids:
                partner = rec.partner_id
                if partner and partner.create_date:
                    create_date = partner.create_date.date()
                    if create_date < (
                        fields.Date.context_today(self) - timedelta(days=180)
                    ):
                        msg = (
                            "Customer Profile has been created more than six (6) "
                            "months ago. As a member of Sales Team, you are not "
                            "allowed to create an invoice for this contact. "
                            "Please contact your Line Manager for assistance."
                        )
                        raise ValidationError(msg)

    # === ONCHANGE METHODS === #

    @api.onchange("company_id")
    def _onchange_company_id(self):
        """Trigger quotation template recomputation on unsaved records company change"""
        super()._onchange_company_id()
        if self._origin.id:
            return
        self._compute_sale_order_template_id()

    @api.onchange("sale_order_template_id")
    def _onchange_sale_order_template_id(self):
        if not self.sale_order_template_id:
            return

        sale_order_template = self.sale_order_template_id.with_context(
            lang=self.partner_id.lang
        )

        order_lines_data = [fields.Command.clear()]
        order_lines_data += [
            fields.Command.create(line._prepare_order_line_values())
            for line in sale_order_template.sale_order_template_line_ids
        ]

        # set first line to sequence -99, so a resequence on first page doesn't cause following page
        # lines (that all have sequence 10 by default) to get mixed in the first page
        if len(order_lines_data) >= 2:
            order_lines_data[1][2]["sequence"] = -99

        self.order_line = order_lines_data

        option_lines_data = [fields.Command.clear()]
        option_lines_data += [
            fields.Command.create(option._prepare_option_line_values())
            for option in sale_order_template.sale_order_template_option_ids
        ]

        self.sale_order_option_ids = option_lines_data

    @api.onchange("partner_id")
    def _onchange_partner_id(self):
        """Reload template for unsaved orders with unmodified lines & options."""
        if self._origin or not self.sale_order_template_id:
            return

        def line_eqv(line, t_line):
            return (
                line
                and t_line
                and (
                    line.product_id == t_line.product_id
                    and line.display_type == t_line.display_type
                    and line.product_uom == t_line.product_uom_id
                    and line.product_uom_qty == t_line.product_uom_qty
                )
            )

        def option_eqv(option, t_option):
            return (
                option
                and t_option
                and all(
                    option[fname] == t_option[fname]
                    for fname in ["product_id", "uom_id", "quantity"]
                )
            )

        lines = self.order_line
        options = self.sale_order_option_ids
        t_lines = self.sale_order_template_id.sale_order_template_line_ids
        t_options = self.sale_order_template_id.sale_order_template_option_ids

        if all(
            chain(
                starmap(line_eqv, zip_longest(lines, t_lines)),
                starmap(option_eqv, zip_longest(options, t_options)),
            )
        ):
            self._onchange_sale_order_template_id()

    # === ACTION METHODS === #

    def _get_confirmation_template(self):
        self.ensure_one()
        return (
            self.sale_order_template_id.mail_template_id
            or super()._get_confirmation_template()
        )

    def action_confirm(self):
        res = super().action_confirm()

        if self.env.context.get("send_email"):
            return res

        for order in self:
            if order.sale_order_template_id.mail_template_id:
                order._send_order_notification_mail(
                    order.sale_order_template_id.mail_template_id
                )
        return res

    def _recompute_prices(self):
        super()._recompute_prices()
        self.sale_order_option_ids.discount = 0.0
        self.sale_order_option_ids._compute_price_unit()
        self.sale_order_option_ids._compute_discount()

    def _can_be_edited_on_portal(self):
        """
        Check if the sale order can be edited on the portal.
        """
        self.ensure_one()
        return self.state in ("draft", "sent")

    # === MISSING ACTION METHODS FROM ODOO 16 === #

    def compute_validity_date(self):
        query = """
            UPDATE sale_order
            SET validity_date = create_date + INTERVAL '30 days'
            WHERE create_date IS NOT NULL
        """
        self.env.cr.execute(query)

    def action_sale_expiration(self):
        today = fields.Date.context_today(self)
        sale_orders = (
            self.env["sale.order"]
            .sudo()
            .search(
                [
                    ("state", "in", ["draft", "sent"]),
                    (
                        "validity_date",
                        "<=",
                        today,
                    ),  # Get orders where validity_date is past
                ]
            )
        )
        print("Expired Sales Orders:", sale_orders)
        if sale_orders:
            for so in sale_orders:
                if so.validity_date and so.is_expired and so.validity_date <= today:
                    self.env.cr.execute(
                        "UPDATE sale_order SET state = %s, system_expiry_date = %s WHERE id = %s",
                        ("cancel", today, so.id),
                    )

    def action_sale_expiration_archive(self):
        today = fields.Date.context_today(self)
        sale_orders = (
            self.env["sale.order"]
            .sudo()
            .search(
                [
                    ("state", "=", "cancel"),
                    (
                        "system_expiry_date",
                        "<=",
                        today,
                    ),  # Get orders where validity_date is past
                ]
            )
        )
        if sale_orders:
            for so in sale_orders:
                sub = (
                    (today - so.system_expiry_date).days if so.system_expiry_date else 0
                )  # Ensure no NoneType error
                if so.validity_date and sub >= 30:
                    self.env.cr.execute(
                        "UPDATE sale_order set active = False WHERE id=%s" % (so.id)
                    )

    def action_cancel(self):
        res = super(SaleOrder, self).action_cancel()
        for rec in self:
            for task in rec.tasks_ids:
                task.document_type_ids.unlink()
                task.document_required_type_ids.unlink()
        return res

    def _prepare_invoice(self):
        invoice_vals = super(SaleOrder, self)._prepare_invoice()
        invoice_vals.update(
            {
                "sale_id": self.id,
                "payment_method": self.payment_method,
            }
        )
        return invoice_vals

    def action_update_manager(self):
        for rec in self:
            for project in rec.project_ids:
                project.write({"user_id": rec.user_id.id})

    @api.depends("order_line.product_id", "order_line.project_id")
    def _compute_project_ids(self):
        is_project_manager = self.env.user.has_group("project.group_project_manager")
        projects = self.env["project.project"].search(
            [("sale_order_id", "in", self.ids)]
        )
        projects_per_so = defaultdict(lambda: self.env["project.project"])
        for project in projects:
            projects_per_so[project.sale_order_id.id] |= project

        for order in self:
            # Fetch projects from various sources
            projects = order.order_line.mapped("product_id.project_id")
            projects |= order.order_line.mapped("project_id")
            projects |= order.project_id
            projects |= projects_per_so[order.id or order._origin.id]

            # Add additional projects with domain ('sale_id', '=', order.id)
            additional_projects = self.env["project.project"].search(
                [("sale_id", "=", order.id)]
            )
            projects |= additional_projects

            # Restrict projects if user is not a project manager
            if not is_project_manager:
                projects = projects._filter_access_rules("read")

            # Assign computed projects and count
            order.project_ids = projects
            order.project_count = len(projects)

    def action_create_project_tasks(self):
        for rec in self:
            # Collect products with `service_tracking == 'new_workflow'`
            products_to_process = rec.order_line.filtered(
                lambda line: line.product_id.service_tracking == "new_workflow"
            ).mapped("product_id")

            if products_to_process:
                # Create a new project if it doesn't exist
                project = self.env["project.project"].search(
                    [("sale_id", "=", rec.id)], limit=1
                )
                if not project:
                    project = self.env["project.project"].create(
                        {
                            "name": f"{rec.name} - {rec.partner_id.name}",
                            "state": "b_new",
                            "sale_id": rec.id,
                            "user_id": rec.user_id.id,
                            "partner_id": rec.partner_id.id,
                            "product_ids": [
                                (6, 0, rec.order_line.mapped("product_id").ids)
                            ],
                        }
                    )
                    if project:
                        ProjectProduct = self.env["project.project.products"]
                        for prod in project.product_ids:
                            ProjectProduct.sudo().create(
                                {
                                    "project_id": project.id,
                                    "product_id": prod.id,
                                }
                            )
                    stages = self.env["project.task.type"].sudo().search([])
                    for stage_id in [243, 65, 28, 29, 67]:
                        stage = stages.filtered(lambda s: s.id == stage_id)
                        if stage:
                            stage.project_ids = [(4, project.id)]

                # Track created tasks to avoid duplication
                existing_task_names = set(project.task_ids.mapped("name"))

                # Prepare tasks to be created
                tasks_to_create = []
                merged_tasks = defaultdict(lambda: defaultdict(list))

                # Group tasks by name and merge child_ids
                for product in products_to_process:
                    for task in product.task_ids:
                        task_data = merged_tasks[task.name]
                        task_data["description"] = task.description
                        task_data["sequence"] = task.sequence
                        task_data["allocated_hours"] = getattr(
                            task, "allocated_hours", 0.0
                        )
                        task_data["user_ids"] = task.user_ids.ids
                        task_data["child_ids"] += [
                            self._prepare_child_task_data(child, project)
                            for child in task.child_ids
                        ]

                # Create tasks with unique children
                for task_name, task_data in merged_tasks.items():
                    if task_name not in existing_task_names:
                        unique_children = {
                            child["name"]: child for child in task_data["child_ids"]
                        }.values()

                        tasks_to_create.append(
                            self._prepare_parent_task_data(
                                task_name, task_data, project, rec, unique_children
                            )
                        )
                        existing_task_names.add(task_name)

                # Create tasks in bulk
                if tasks_to_create:
                    self.env["project.task"].create(tasks_to_create)

    def _prepare_child_task_data(self, child, project):
        """Helper method to prepare child task data"""
        return {
            "is_subtask": True,
            "name": child.name,
            "project_id": project.id,
            "description": child.description,
            "sequence": child.sequence,
            "allocated_hours": getattr(child, "allocated_hours", 0.0),
            "user_ids": [(6, 0, child.user_ids.ids)] if child.user_ids else [],
            "checkpoint_ids": [
                (
                    0,
                    0,
                    {
                        "reached_checkpoint_ids": [
                            (6, 0, cp.reached_checkpoint_ids.ids)
                        ],
                        "stage_id": cp.stage_id.id,
                        "milestone_id": cp.milestone_id.id,
                        "sequence": cp.sequence,
                    },
                )
                for cp in child.checkpoint_ids
            ],
        }

    def _prepare_parent_task_data(self, name, data, project, rec, children):
        """Helper method to prepare parent task data"""
        return {
            "name": name,
            "project_id": project.id,
            "sale_order_id": rec.id,
            "user_ids": [(6, 0, [rec.user_id.id] + (data["user_ids"] or []))],
            "description": data["description"],
            "allocated_hours": data["allocated_hours"],
            "sequence": data["sequence"],
            "child_ids": [
                (0, 0, self._prepare_child_task_data(child, project))
                for child in children
            ],
        }

    def remove_duplicate_tasks(self):
        for rec in self:
            seen_names = set()
            duplicate_tasks = self.env["project.task"]  # Adjust the model if necessary

            for task in rec.tasks_ids:
                if task.name in seen_names:
                    duplicate_tasks |= task
                else:
                    seen_names.add(task.name)

            # Unlink the duplicate tasks
            if duplicate_tasks:
                duplicate_tasks.unlink()
                print("Removed duplicate tasks:", duplicate_tasks)

    def check_crm_payment(self):
        for rec in self:
            return {
                "res_model": "sale.crm.wizard",
                "type": "ir.actions.act_window",
                "view_mode": "form",
                "view_type": "form",
                "context": {"default_sale_id": rec.id},
                "view_id": self.env.ref(
                    "freezoner_custom.sale_crm_wizard_form_view"
                ).id,
                "target": "new",
            }

    @api.onchange("payment_method", "order_line")
    def action_visa(self):
        self.add_visa_line()

    @api.onchange("order_line")
    def action_calculate(self):
        self.prepare_lines()

    def prepare_lines(self):
        sov_lines = []
        self.sov_ids = None
        for rec in self:
            if rec.order_line:
                for line in rec.order_line:
                    tax = 0.0
                    for t in line.tax_id:
                        tax += t.amount
                    sov_lines.append(
                        (
                            0,
                            0,
                            {
                                "product_id": line.product_id.id,
                                "qty": line.product_uom_qty,
                                "unit_cost": 0.0,
                                "name": line.name,
                                "unit_price": line.price_unit
                                + ((tax * line.price_unit) / 100),
                            },
                        )
                    )

                # Add commission line only if the product exists
                commission_product = (
                    self.env["product.product"]
                    .sudo()
                    .search([("is_service_commission", "=", True)], limit=1)
                )
                if commission_product:
                    sov_lines.append(
                        (
                            0,
                            0,
                            {
                                "product_id": commission_product.id,
                                "qty": 1,
                                "unit_cost": 0.0,
                                "unit_price": 0.0,
                                "name": "Service Commission",
                            },
                        )
                    )

                self.write({"sov_ids": sov_lines})

    def add_visa_line(self):
        for rec in self:
            lines = []
            if rec.payment_method == "visa":
                total = 0.0
                product = (
                    self.env["product.product"]
                    .sudo()
                    .search([("stripe_visa", "=", True)], limit=1)
                )
                for line in rec.order_line:
                    if not line.product_id.product_tmpl_id.stripe_visa:
                        total += line.price_total
                product.lst_price = total * 0.04
                if product not in rec.order_line.mapped("product_id"):
                    msg = (
                        "Kindly note that an additional charge of 4% is applicable "
                        "to the total invoice amount to cover online payment "
                        "processing fees. Your attention to this matter is appreciated."
                    )
                    # Ensure we get a valid UoM with proper rounding
                    uom = None

                    # First try product's UoM if it has valid rounding
                    if product.uom_id and product.uom_id.rounding > 0:
                        uom = product.uom_id

                    # Fallback to standard 'Units' UoM
                    if not uom:
                        uom = self.env["uom.uom"].search(
                            [("name", "=", "Units"), ("rounding", ">", 0)], limit=1
                        )

                    # Fallback to any valid UoM with proper rounding
                    if not uom:
                        uom = self.env["uom.uom"].search(
                            [("rounding", ">", 0)], limit=1
                        )

                    # Last resort: get the default UoM category and find a valid one
                    if not uom:
                        unit_category = self.env.ref(
                            "uom.product_uom_categ_unit", raise_if_not_found=False
                        )
                        if unit_category:
                            uom = self.env["uom.uom"].search(
                                [
                                    ("category_id", "=", unit_category.id),
                                    ("rounding", ">", 0),
                                ],
                                limit=1,
                            )

                    # Final fallback: create a simple UoM if none exists
                    if not uom:
                        uom = self.env["uom.uom"].create(
                            {
                                "name": "Unit",
                                "category_id": self.env.ref(
                                    "uom.product_uom_categ_unit"
                                ).id,
                                "factor": 1.0,
                                "rounding": 0.01,
                                "uom_type": "reference",
                            }
                        )

                    # Ensure the product has this UoM set
                    if not product.uom_id or product.uom_id.rounding <= 0:
                        product.uom_id = uom

                    lines.append(
                        (
                            0,
                            0,
                            {
                                "product_id": product.id,
                                "name": msg,
                                "product_uom_qty": 1,
                                "product_uom": uom.id,
                                "price_unit": total * 0.04,
                            },
                        )
                    )
                    self.write({"order_line": lines})
            if rec.payment_method == "bank":
                product = (
                    self.env["product.product"]
                    .sudo()
                    .search([("stripe_visa", "=", True)], limit=1)
                )
                for line in rec.order_line:
                    if product and product.id == line.product_id.id:
                        line.unlink()

    # Override action_confirm method
    def action_confirm_custom(self):
        """Override the standard confirm action to add custom workflow"""
        # First prepare SOV lines if not already done
        if not self.sov_ids:
            self.prepare_lines()

        # Call standard confirmation
        res = super(SaleOrder, self).action_confirm()

        # Run custom workflow
        self.check_crm_payment()

        # Create/update projects
        for project in self.project_ids:
            project.write({"state": "b_new", "user_id": self.user_id.id})

            # Update project name and documents
            for line in self.order_line:
                if line.id == project.sale_line_id.id:
                    date_ref = "{:02d}{:02d}".format(
                        self.create_date.year % 100, self.create_date.month
                    )
                    project.name = f"{self.name} - {date_ref} - {line.product_id.name}"

                    # Create document lines
                    for doc in line.product_id.product_tmpl_id.document_type_ids:
                        if (
                            hasattr(doc, "document_id")
                            and doc.document_id
                            and hasattr(doc.document_id, "id")
                        ):
                            self.env["task.document.lines"].sudo().create(
                                {
                                    "project_id": project.id,
                                    "document_id": doc.document_id.id,
                                    "name": f"{doc.document_id.name} - {self.partner_id.name}",
                                    "is_required": doc.is_required,
                                    "issue_date": False,
                                    "expiration_date": False,
                                }
                            )

                    # Create required document lines
                    if line.product_id.product_tmpl_id.document_required_type_ids:
                        for (
                            req_doc
                        ) in line.product_id.product_tmpl_id.document_required_type_ids:
                            if (
                                hasattr(req_doc, "document_id")
                                and req_doc.document_id
                                and hasattr(req_doc.document_id, "id")
                            ):
                                self.env["task.document.required.lines"].sudo().create(
                                    {
                                        "project_id": project.id,
                                        "document_id": req_doc.document_id.id,
                                        "name": f"{req_doc.document_id.name} - {self.partner_id.name}",
                                        "is_required": req_doc.is_required,
                                        "issue_date": False,
                                        "expiration_date": False,
                                    }
                                )

            # Set project stages
            stages = self.env["project.task.type"].sudo().search([])
            for stage_id in [64, 65, 66, 67, 29, 30]:
                stage = stages.filtered(lambda s: s.id == stage_id)
                if stage:
                    stage.project_ids = [project.id]

        # Create tasks and remove duplicates
        self.action_create_project_tasks()
        self.remove_duplicate_tasks()

        return res

    # === MISSING MODEL METHODS FROM ODOO 16 === #

    def write(self, vals):
        res = super(SaleOrder, self).write(vals)
        for rec in self:
            if rec.partner_id and rec.partner_id.company_type == "company":
                if not rec.partner_id.phone:
                    raise ValidationError("Please add phone number for the customer")
                if not rec.partner_id.email:
                    raise ValidationError("Please add email for the customer")
                if (
                    hasattr(rec.partner_id, "license_authority_id")
                    and not rec.partner_id.license_authority_id
                ):
                    raise ValidationError(
                        "Please add license authority for the customer"
                    )
                if (
                    hasattr(rec.partner_id, "incorporation_date")
                    and not rec.partner_id.incorporation_date
                ):
                    raise ValidationError(
                        "Please add incorporation date for the customer"
                    )
                if (
                    hasattr(rec.partner_id, "license_number")
                    and not rec.partner_id.license_number
                ):
                    raise ValidationError("Please add license number for the customer")
            if rec.partner_id and rec.partner_id.company_type == "person":
                if not rec.partner_id.phone:
                    raise ValidationError("Please add phone number for the customer")
                if not rec.partner_id.email:
                    raise ValidationError("Please add email for the customer")
                if hasattr(rec.partner_id, "gender") and not rec.partner_id.gender:
                    raise ValidationError("Please add gender for the customer")
                if (
                    hasattr(rec.partner_id, "nationality_id")
                    and not rec.partner_id.nationality_id
                ):
                    raise ValidationError("Please add nationality for the customer")
        return res

    @api.model
    def create(self, values):
        res = super(SaleOrder, self).create(values)
        if self.partner_id and self.partner_id.company_type == "company":
            if not self.partner_id.phone:
                raise ValidationError(" Please add phone number for the customer ")
            if not self.partner_id.email:
                raise ValidationError(" Please add email for the customer ")
            # Check if license_authority_id field exists before accessing
            if (
                hasattr(self.partner_id, "license_authority_id")
                and not self.partner_id.license_authority_id
            ):
                raise ValidationError(" Please add license authority for the customer ")
            # Check if incorporation_date field exists before accessing
            if (
                hasattr(self.partner_id, "incorporation_date")
                and not self.partner_id.incorporation_date
            ):
                raise ValidationError(
                    " Please add incorporation date for the customer "
                )
            # Check if license_number field exists before accessing
            if (
                hasattr(self.partner_id, "license_number")
                and not self.partner_id.license_number
            ):
                raise ValidationError(" Please add license number for the customer ")
        if self.partner_id and self.partner_id.company_type == "person":
            if not self.partner_id.phone:
                raise ValidationError(" Please add phone number for the customer ")
            if not self.partner_id.email:
                raise ValidationError(" Please add email for the customer ")
            # Check if gender field exists before accessing
            if hasattr(self.partner_id, "gender") and not self.partner_id.gender:
                raise ValidationError(" Please add gender for the customer ")
            # Check if nationality_id field exists before accessing
            if (
                hasattr(self.partner_id, "nationality_id")
                and not self.partner_id.nationality_id
            ):
                raise ValidationError(" Please add nationality for the customer ")
        return res
