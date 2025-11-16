from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import hashlib
import traceback


def log_server_exception(env, exc, context=None):
    """Server-side helper to log an exception as a qa.error.event.

    Signature: log_server_exception(env, exc, context={})

    - env: Odoo environment (env)
    - exc: exception instance
    - context: optional dict with keys like severity, project, scenario, user_login

    This function will create a `qa.error.event` record with source='odoo_server'.
    It uses sudo() to ensure the exception is recorded regardless of caller permissions.
    """
    ctx = context or {}
    try:
        message = str(exc)
    except Exception:
        message = repr(exc)

    details = traceback.format_exc()

    vals = {
        'source': 'odoo_server',
        'severity': ctx.get('severity', 'error'),
        'project': ctx.get('project', False),
        'scenario': ctx.get('scenario', False),
        'user_login': ctx.get('user_login', False),
        'url': ctx.get('url', False),
        'browser': False,
        'trace_url': ctx.get('trace_url', False),
        'message': message,
        'details': details,
        'tags': ctx.get('tags', False),
    }

    try:
        event = env['qa.error.event'].sudo().create(vals)
        return event
    except Exception:
        # If logging fails, don't propagate logging errors; fail silently
        return None



class QAErrorEvent(models.Model):
    _name = 'qa.error.event'
    _description = 'QA Error Event'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'
    _rec_name = 'name'

    source = fields.Selection([
        ('odoo_ui', 'Odoo UI'),
        ('odoo_server', 'Odoo Server'),
        ('server', 'Server'),
        ('playwright', 'Playwright'),
        ('manual', 'Manual Report')
    ], required=True, index=True)
    
    # User-friendly manual reporting fields
    name = fields.Char(
        string='Error Title', 
        help='Brief title for the error',
        compute='_compute_name', 
        store=True
    )
    description = fields.Html(
        string='What Happened?', 
        help='Describe what you were trying to do'
    )
    error_location = fields.Char(
        string='Location/Menu', 
        help='Where did the error occur? (e.g., Sales > Orders, Accounting > Invoices)'
    )
    steps_to_reproduce = fields.Html(
        string='Steps to Reproduce', 
        help='How to recreate this error step by step'
    )
    record_reference = fields.Char(
        string='Record Reference', 
        help='Related record info (e.g., Invoice INV/2023/001, Project ABC)'
    )
    reporter_id = fields.Many2one(
        'res.users', 
        string='Reporter', 
        default=lambda self: self.env.user,
        tracking=True
    )
    report_date = fields.Datetime(
        string='Report Date', 
        default=fields.Datetime.now,
        tracking=True
    )

    # Workflow management fields
    status = fields.Selection([
        ('new', 'New'),
        ('in_progress', 'In Progress'),
        ('fixed', 'Fixed'),
        ('wont_fix', 'Won\'t Fix'),
        ('duplicate', 'Duplicate'),
    ], string='Status', default='new', tracking=True, index=True)

    assigned_to = fields.Many2one(
        'res.users', 
        string='Assigned To', 
        tracking=True,
        help='Developer assigned to fix this issue'
    )
    fix_notes = fields.Html(
        string='Fix Notes', 
        tracking=True,
        help='Details about the fix implemented'
    )
    fix_commit = fields.Char(
        string='Git Commit', 
        tracking=True,
        help='Git commit hash for the fix'
    )
    fixed_date = fields.Datetime(
        string='Fixed Date', 
        tracking=True
    )

    # Priority and impact
    impact = fields.Selection([
        ('critical', '🔴 CRITICAL - Blocks work completely'),
        ('high', '🟡 HIGH - Major feature broken'),
        ('medium', '🟢 MEDIUM - Workaround available'),
        ('low', '⚪ LOW - Minor issue'),
    ], string='Impact Level', default='medium', tracking=True, index=True)

    priority = fields.Selection([
        ('0', 'Low'),
        ('1', 'Normal'),
        ('2', 'High'),
        ('3', 'Urgent'),
    ], string='Priority', default='1', tracking=True, index=True)

    # Screenshot/attachment support
    screenshot_ids = fields.Many2many(
        'ir.attachment', 
        'qa_error_attachment_rel',
        'error_id', 'attachment_id',
        string='Screenshots/Attachments',
        help='Upload screenshots or files related to this error'
    )

    # Color coding for kanban
    color = fields.Integer(
        string='Color Index', 
        compute='_compute_color', 
        store=True
    )
    severity = fields.Selection([
        ('info', 'Info'),
        ('warning', 'Warning'),
        ('error', 'Error'),
        ('critical', 'Critical')
    ], required=True, index=True, default='error')
    project = fields.Char(index=True)
    scenario = fields.Char(index=True)
    user_login = fields.Char()
    url = fields.Char()
    browser = fields.Char()
    trace_url = fields.Char()
    message = fields.Text(required=True)
    details = fields.Text()
    fingerprint = fields.Char(index=True, compute='_compute_fingerprint', store=True)
    
    # Log file integration fields
    log_file_path = fields.Char(
        string='Log File Path',
        help='Full path to the log file where this error was recorded'
    )
    log_file_url = fields.Char(
        string='Log File URL',
        help='URL to access the log file (for Odoo.sh or remote servers)'
    )
    log_line_number = fields.Integer(
        string='Log Line Number',
        help='Line number in the log file where this error appears'
    )
    log_level = fields.Selection([
        ('DEBUG', 'Debug'),
        ('INFO', 'Info'), 
        ('WARNING', 'Warning'),
        ('ERROR', 'Error'),
        ('CRITICAL', 'Critical'),
    ], string='Log Level', help='Log level from Odoo server logs')
    
    tags = fields.Char()
    # auxiliary fields referenced by views
    date = fields.Datetime(default=fields.Datetime.now, index=True)
    occurrences = fields.Integer(default=1)

    _sql_constraints = [
        ('positive_occurrences', 'CHECK (occurrences > 0)', 'Occurrences must be positive'),
    ]

    @api.depends('message', 'source', 'error_location')
    def _compute_name(self):
        """Compute a user-friendly name for the error"""
        for record in self:
            if record.source == 'manual' and record.error_location:
                # For manual reports, use location if available
                record.name = f"Error in {record.error_location}"
            elif record.message:
                # Use first line of message, truncated
                first_line = record.message.splitlines()[0] if record.message else ''
                record.name = first_line[:100] + '...' if len(first_line) > 100 else first_line
            else:
                record.name = f"Error #{record.id or 'New'}"

    @api.depends('status', 'impact', 'priority')
    def _compute_color(self):
        """Set color based on status and impact for kanban view"""
        for record in self:
            if record.status == 'fixed':
                record.color = 10  # Green
            elif record.status == 'wont_fix':
                record.color = 7   # Gray
            elif record.status == 'duplicate':
                record.color = 8   # Light gray
            elif record.impact == 'critical':
                record.color = 1   # Red
            elif record.impact == 'high':
                record.color = 3   # Orange
            elif record.priority == '3':  # Urgent
                record.color = 2   # Yellow
            else:
                record.color = 0   # White

    def action_mark_fixed(self):
        """Quick action to mark as fixed"""
        self.ensure_one()
        self.write({
            'status': 'fixed',
            'fixed_date': fields.Datetime.now(),
        })
        return True

    def action_mark_in_progress(self):
        """Quick action to mark as in progress"""
        self.ensure_one()
        self.write({
            'status': 'in_progress',
            'assigned_to': self.env.user.id if not self.assigned_to else self.assigned_to.id,
        })
        return True

    def action_assign_to_me(self):
        """Quick action to assign to current user"""
        self.ensure_one()
        self.write({
            'assigned_to': self.env.user.id,
            'status': 'in_progress' if self.status == 'new' else self.status,
        })
        return True

    def action_mark_duplicate(self):
        """Quick action to mark as duplicate"""
        self.ensure_one()
        self.write({'status': 'duplicate'})
        return True

    def action_mark_wont_fix(self):
        """Quick action to mark as won't fix"""
        self.ensure_one()
        self.write({'status': 'wont_fix'})
        return True

    @api.constrains('url', 'trace_url')
    def _check_urls(self):
        """Validate URL formats"""
        for record in self:
            if record.url and not record.url.startswith(('http://', 'https://', '/')):
                raise ValidationError(_('URL must be a valid web address'))
            if record.trace_url and not record.trace_url.startswith(('http://', 'https://', '/')):
                raise ValidationError(_('Trace URL must be a valid web address'))

    @api.constrains('message')
    def _check_message_length(self):
        """Ensure message is not empty and within reasonable length"""
        for record in self:
            if not record.message or not record.message.strip():
                raise ValidationError(_('Error message cannot be empty'))
            if len(record.message) > 5000:  # reasonable limit
                raise ValidationError(_('Error message is too long (max 5000 characters)'))

    @api.depends('source', 'scenario', 'url', 'message')
    def _compute_fingerprint(self):
        for record in self:
            first_line = ''
            if record.message:
                first_line = record.message.splitlines()[0]
            key = (record.source or '') + (record.scenario or '') + (record.url or '') + first_line
            record.fingerprint = hashlib.sha1(key.encode('utf-8')).hexdigest() if key else False

    @api.model_create_multi
    def create(self, vals_list):
        # Compute fingerprint from provided vals to ensure it's available on create
        for vals in vals_list:
            src = vals.get('source') or ''
            scn = vals.get('scenario') or ''
            url = vals.get('url') or ''
            msg = vals.get('message') or ''
            first_line = msg.splitlines()[0] if msg else ''
            key = src + scn + url + first_line
            if key:
                vals['fingerprint'] = hashlib.sha1(key.encode('utf-8')).hexdigest()
            # Ensure date exists (views reference `date`)
            if 'date' not in vals:
                vals['date'] = fields.Datetime.now()
            # occurrences default handled by field default
        return super(QAErrorEvent, self).create(vals_list)

    def action_open_trace(self):
        self.ensure_one()
        if not self.trace_url:
            return True
        return {
            'type': 'ir.actions.act_url',
            'url': self.trace_url,
            'target': 'new',
        }

    def action_open_url(self):
        self.ensure_one()
        if not self.url:
            return True
        return {
            'type': 'ir.actions.act_url',
            'url': self.url,
            'target': 'new',
        }
        
    @api.model
    def register_log_handler(self):
        """Register log handler for automatic server log capture"""
        try:
            log_manager = self.env['qa.log.handler.manager']
            return log_manager.register_log_handler()
        except Exception:
            return False
            
    @api.model
    def unregister_log_handler(self):
        """Unregister log handler"""
        try:
            log_manager = self.env['qa.log.handler.manager'] 
            return log_manager.unregister_log_handler()
        except Exception:
            return False
    
    @api.model 
    def get_report_data(self):
        """Get all error data for reports"""
        return self.search([])
    
    @api.model
    def export_errors_to_github_issues(self):
        """Export errors as GitHub issues"""
        import requests
        import json
        from datetime import datetime
        
        # GitHub configuration (from system parameters)
        github_token = self.env['ir.config_parameter'].sudo().get_param('github.api_token')
        github_repo = self.env['ir.config_parameter'].sudo().get_param('github.repo')
        
        if not github_token or not github_repo:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Configuration Missing',
                    'message': 'Please configure GitHub token and repository in System Parameters:\n- github.api_token\n- github.repo (format: username/repository)',
                    'type': 'warning',
                    'sticky': True,
                }
            }
        
        headers = {
            'Authorization': f'token {github_token}',
            'Accept': 'application/vnd.github.v3+json',
            'Content-Type': 'application/json',
        }
        
        # Get errors to export (only critical/error severity to avoid spam)
        errors = self.search([
            ('severity', 'in', ['critical', 'error'])
        ], order='severity desc, create_date desc', limit=20)  # Limit to avoid API rate limits
        
        if not errors:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'No Errors to Export',
                    'message': 'No critical or error severity errors found to export.',
                    'type': 'info',
                }
            }
        
        created_issues = 0
        failed_issues = 0
        
        for error in errors:
            # Create issue title
            title = f"[{error.severity.upper()}] {error.source}: {(error.message or '')[:80]}"
            if len(error.message or '') > 80:
                title += "..."
            
            # Create issue body
            body = f"""## Error Details
            
**ID:** {error.id}
**Date:** {error.create_date}
**Source:** {error.source}
**Severity:** {error.severity}
**Occurrences:** {error.occurrences}

## Message
```
{error.message or 'No message'}
```

## Details
```
{error.details or 'No details'}
```

## Context
- **Project:** {error.project or 'N/A'}
- **Scenario:** {error.scenario or 'N/A'}
- **User:** {error.user_login or 'N/A'}
- **URL:** {error.url or 'N/A'}
- **Browser:** {error.browser or 'N/A'}

## Log Information
- **Log File:** {getattr(error, 'log_file_path', 'N/A')}
- **Log URL:** {getattr(error, 'log_file_url', 'N/A')}
- **Log Line:** {getattr(error, 'log_line_number', 'N/A')}
- **Log Level:** {getattr(error, 'log_level', 'N/A')}

## Technical
- **Fingerprint:** {error.fingerprint or 'N/A'}
- **Tags:** {error.tags or 'N/A'}
- **Trace URL:** {error.trace_url or 'N/A'}

---
*Auto-exported from Odoo Error Reporter on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""
            
            # Create GitHub issue
            issue_data = {
                'title': title,
                'body': body,
                'labels': [
                    f'severity:{error.severity}',
                    f'source:{error.source}',
                    'auto-export',
                    'odoo-error'
                ]
            }
            
            try:
                response = requests.post(
                    f'https://api.github.com/repos/{github_repo}/issues',
                    headers=headers,
                    data=json.dumps(issue_data),
                    timeout=30
                )
                
                if response.status_code == 201:
                    created_issues += 1
                else:
                    failed_issues += 1
                    self.env['ir.logging'].sudo().create({
                        'name': 'GitHub Export Error',
                        'type': 'server',
                        'level': 'WARNING',
                        'message': f'Failed to create GitHub issue for error {error.id}: {response.status_code} - {response.text}',
                        'path': 'automatic_error_reporter',
                        'func': 'export_errors_to_github_issues',
                        'line': '1',
                    })
                    
            except Exception as e:
                failed_issues += 1
                self.env['ir.logging'].sudo().create({
                    'name': 'GitHub Export Error',
                    'type': 'server', 
                    'level': 'ERROR',
                    'message': f'Error creating GitHub issue for error {error.id}: {str(e)}',
                    'path': 'automatic_error_reporter',
                    'func': 'export_errors_to_github_issues',
                    'line': '1',
                })
        
        # Return result notification
        if created_issues > 0:
            message = f'Successfully created {created_issues} GitHub issues'
            if failed_issues > 0:
                message += f' ({failed_issues} failed)'
            message += f' from {len(errors)} errors.\n\nCheck your GitHub repository: https://github.com/{github_repo}/issues'
            
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'GitHub Export Complete!',
                    'message': message,
                    'type': 'success',
                    'sticky': True,
                }
            }
        else:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'GitHub Export Failed',
                    'message': f'Failed to create any GitHub issues. Check system logs for details.',
                    'type': 'danger',
                    'sticky': True,
                }
            }
    
    @api.model
    def export_errors_to_github_files(self):
        """Export errors as files to GitHub repository"""
        import requests
        import json
        import base64
        from datetime import datetime
        
        try:
            # GitHub configuration
            github_token = self.env['ir.config_parameter'].sudo().get_param('github.api_token')
            github_repo = self.env['ir.config_parameter'].sudo().get_param('github.repo')
            
            if not github_token or not github_repo:
                return {
                    'type': 'ir.actions.client',
                    'tag': 'display_notification',
                    'params': {
                        'title': 'Configuration Missing',
                        'message': 'Please configure GitHub token and repository in System Parameters',
                        'type': 'warning',
                        'sticky': True,
                    }
                }
            
            # Get errors to export (only critical/error severity)
            errors = self.search([
                ('severity', 'in', ['critical', 'error'])
            ], order='severity desc, create_date desc', limit=10)  # Reduced limit for testing
            
            if not errors:
                return {
                    'type': 'ir.actions.client',
                    'tag': 'display_notification',
                    'params': {
                        'title': 'No Errors to Export',
                        'message': 'No critical or error severity errors found to export.',
                        'type': 'info',
                    }
                }
            
            # Test GitHub connection first
            headers = {
                'Authorization': f'token {github_token}',
                'Accept': 'application/vnd.github.v3+json',
                'Content-Type': 'application/json',
            }
            
            # Test repository access
            test_response = requests.get(
                f'https://api.github.com/repos/{github_repo}',
                headers=headers,
                timeout=10
            )
            
            if test_response.status_code != 200:
                return {
                    'type': 'ir.actions.client',
                    'tag': 'display_notification',
                    'params': {
                        'title': 'GitHub Connection Failed',
                        'message': f'Cannot access repository. Status: {test_response.status_code}\nResponse: {test_response.text[:200]}',
                        'type': 'danger',
                        'sticky': True,
                    }
                }
            
            # Create a simple test file first
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            test_content = f"""# Error Export Test
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Total Errors Found: {len(errors)}
Repository: {github_repo}

This is a test file to verify GitHub API access is working.
"""
            
            file_data = {
                'message': f'Test error export - {len(errors)} errors found on {timestamp}',
                'content': base64.b64encode(test_content.encode('utf-8')).decode('utf-8')
            }
            
            # Try to create the test file
            response = requests.put(
                f'https://api.github.com/repos/{github_repo}/contents/errors/test_{timestamp}.md',
                headers=headers,
                data=json.dumps(file_data),
                timeout=30
            )
            
            if response.status_code in [200, 201]:
                return {
                    'type': 'ir.actions.client',
                    'tag': 'display_notification',
                    'params': {
                        'title': 'GitHub File Export Success!',
                        'message': f'Successfully created test file!\n\nFound {len(errors)} errors ready for export.\nView at: https://github.com/{github_repo}/blob/main/errors/test_{timestamp}.md',
                        'type': 'success',
                        'sticky': True,
                    }
                }
            else:
                return {
                    'type': 'ir.actions.client',
                    'tag': 'display_notification',
                    'params': {
                        'title': 'GitHub API Error',
                        'message': f'Failed to create file. Status: {response.status_code}\nResponse: {response.text[:300]}',
                        'type': 'danger',
                        'sticky': True,
                    }
                }
                
        except Exception as e:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Export Error',
                    'message': f'Error during export: {str(e)}',
                    'type': 'danger',
                    'sticky': True,
                }
            }