# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import requests


class GitHubConfig(models.TransientModel):
    _name = 'github.config'
    _description = 'GitHub Configuration'
    
    github_token = fields.Char(
        string='GitHub Personal Access Token',
        help='Generate a token at: https://github.com/settings/tokens\nRequired permissions: repo (Full control of private repositories)'
    )
    github_repo = fields.Char(
        string='GitHub Repository',
        help='Format: username/repository-name (e.g., john-doe/odoo-errors)',
        placeholder='username/repository-name'
    )
    
    @api.model
    def default_get(self, fields_list):
        """Load current configuration from system parameters"""
        res = super().default_get(fields_list)
        
        if 'github_token' in fields_list:
            res['github_token'] = self.env['ir.config_parameter'].sudo().get_param('github.api_token', '')
        
        if 'github_repo' in fields_list:
            res['github_repo'] = self.env['ir.config_parameter'].sudo().get_param('github.repo', '')
            
        return res
    
    def save_configuration(self):
        """Save GitHub configuration to system parameters"""
        self.ensure_one()
        
        # Validate repository format
        if self.github_repo and '/' not in self.github_repo:
            raise ValidationError(_('Repository format should be: username/repository-name'))
        
        # Test GitHub connection if both fields are provided
        if self.github_token and self.github_repo:
            if not self._test_github_connection():
                raise ValidationError(_('Failed to connect to GitHub. Please check your token and repository.'))
        
        # Save to system parameters
        self.env['ir.config_parameter'].sudo().set_param('github.api_token', self.github_token or '')
        self.env['ir.config_parameter'].sudo().set_param('github.repo', self.github_repo or '')
        
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Configuration Saved!',
                'message': 'GitHub configuration has been saved successfully.',
                'type': 'success',
            }
        }
    
    def _test_github_connection(self):
        """Test GitHub API connection"""
        try:
            headers = {
                'Authorization': f'token {self.github_token}',
                'Accept': 'application/vnd.github.v3+json',
            }
            
            # Test repository access
            response = requests.get(
                f'https://api.github.com/repos/{self.github_repo}',
                headers=headers,
                timeout=10
            )
            
            return response.status_code == 200
            
        except Exception:
            return False
    
    def test_connection(self):
        """Test GitHub connection and show result"""
        self.ensure_one()
        
        if not self.github_token or not self.github_repo:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Missing Configuration',
                    'message': 'Please provide both GitHub token and repository.',
                    'type': 'warning',
                }
            }
        
        if self._test_github_connection():
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Connection Successful!',
                    'message': f'Successfully connected to GitHub repository: {self.github_repo}',
                    'type': 'success',
                }
            }
        else:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Connection Failed',
                    'message': 'Failed to connect to GitHub. Please check:\n- Token has "repo" permissions\n- Repository exists and is accessible\n- Repository format is correct (username/repo)',
                    'type': 'danger',
                }
            }
    
    def open_github_token_help(self):
        """Open GitHub token creation page"""
        return {
            'type': 'ir.actions.act_url',
            'url': 'https://github.com/settings/tokens/new?description=Odoo%20Error%20Reporter&scopes=repo',
            'target': 'new',
        }
