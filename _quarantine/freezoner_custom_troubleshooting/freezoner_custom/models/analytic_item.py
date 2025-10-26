from odoo import models, fields, api, _

class SaleOrderAnalyticItem(models.Model):
    _name = 'sale.order.analytic.item'
    _description = 'Sale Order Analytic Item'
    _order = 'sequence, id'

    name = fields.Char(string='Description', required=True)
    sequence = fields.Integer(string='Sequence', default=10)
    sale_order_id = fields.Many2one('sale.order', string='Sale Order', required=True, ondelete='cascade')
    analytic_account_id = fields.Many2one('account.analytic.account', string='Analytic Account', required=True)
    amount = fields.Float(string='Amount', required=True)
    date = fields.Date(string='Date', required=True, default=fields.Date.context_today)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('posted', 'Posted'),
        ('cancelled', 'Cancelled')
    ], string='Status', default='draft', required=True)
    notes = fields.Text(string='Notes')
    company_id = fields.Many2one('res.company', string='Company', related='sale_order_id.company_id', store=True)
    currency_id = fields.Many2one('res.currency', string='Currency', related='sale_order_id.currency_id', store=True)

    def action_post(self):
        self.write({'state': 'posted'})

    def action_cancel(self):
        self.write({'state': 'cancelled'})

    def action_draft(self):
        self.write({'state': 'draft'}) 