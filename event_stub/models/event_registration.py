# -*- coding: utf-8 -*-

from odoo import models, fields, api


class EventRegistration(models.Model):
    """Stub model for event.registration to resolve KeyError on Odoo.sh"""
    _name = 'event.registration'
    _description = 'Event Registration Stub'
    
    name = fields.Char('Registration Name')
    event_id = fields.Many2one('event.event', 'Event')
    partner_id = fields.Many2one('res.partner', 'Partner')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirm', 'Confirmed'),
        ('done', 'Done'),
        ('cancel', 'Cancelled')
    ], default='draft', string='Status')
