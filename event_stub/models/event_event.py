# -*- coding: utf-8 -*-

from odoo import models, fields, api


class EventEvent(models.Model):
    """Stub model for event.event to resolve KeyError on Odoo.sh"""
    _name = 'event.event'
    _description = 'Event Stub'
    
    name = fields.Char('Event Name', required=True)
    date_begin = fields.Datetime('Start Date')
    date_end = fields.Datetime('End Date')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirm', 'Confirmed'),
        ('done', 'Done'),
        ('cancel', 'Cancelled')
    ], default='draft', string='Status')