from odoo import api, fields, models


class AccountAnalyticLine(models.Model):
    _inherit = "account.analytic.line"

    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('done', 'Done'),
        ('cancel', 'Cancelled')
    ], string='Status', default='draft')
    sale_id = fields.Many2one(
        "sale.order",
        string="Pro-forma Invoice",
        ondelete="cascade",
        index=True  # This improves query performance
    )
    is_proforma_related = fields.Boolean(
        string="Is Proforma Related",
        default=False,
        help="Technical field to filter analytic items related to proforma invoices"
    )
    product_id = fields.Many2one('product.product', string='Product')
    name = fields.Char('Description')
    qty = fields.Float('Quantity', default=1.0)
    is_access_price = fields.Boolean('Access Price')
    unit_price = fields.Float('Unit Price')
    unit_cost = fields.Float('Unit Cost')
    revenue = fields.Float("Revenue", compute="_compute_revenue", store=True)
    planned_expenses = fields.Float("Planned Expenses", compute="_compute_expenses", store=True)
    profit = fields.Float(compute="_compute_profit", store=True)
    tax = fields.Float("Tax")
    net = fields.Float(compute="_compute_net", store=True)
    commission_attribute = fields.Selection([
        ("license", "Cross/Up Sell License"),
        ("value", "Cross/Up Sell Value Added Service"),
        ("renewals", "Renewals"),
        ("network", "Personal Network"),
        ("annual", "Annual Contract"),
        ("bank", "Banking Deals"),
        ("accounting", "Accounting Deals"),
        ("misc", "Miscellaneous Deals"),
    ], string="Commission Attribute")
    date_order = fields.Date(
        "Order Date",
        related="sale_id.date_order",
        store=True
    )
    partner_id = fields.Many2one(
        "res.partner",
        string="Customer",
        related="sale_id.partner_id",
        store=True
    )
    sale_commission_user_ids = fields.Many2many(
        'res.users', 
        string='Commission Users'
    )

    @api.depends("qty", "unit_price")
    def _compute_revenue(self):
        for rec in self:
            rec.revenue = rec.qty * rec.unit_price

    @api.depends("qty", "unit_cost")
    def _compute_expenses(self):
        for rec in self:
            rec.planned_expenses = rec.qty * rec.unit_cost

    @api.depends("revenue", "planned_expenses")
    def _compute_profit(self):
        for rec in self:
            rec.profit = rec.revenue - rec.planned_expenses

    @api.depends("profit", "tax")
    def _compute_net(self):
        for rec in self:
            rec.net = rec.profit - rec.tax
