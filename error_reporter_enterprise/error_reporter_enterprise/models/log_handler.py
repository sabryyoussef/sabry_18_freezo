# -*- coding: utf-8 -*-
import logging
import os
import traceback
from datetime import datetime
from odoo import api, models, fields

_logger = logging.getLogger(__name__)


class OdooLogHandler(logging.Handler):
    """Custom log handler to capture Odoo server logs and create error events"""
    
    def __init__(self, env):
        super().__init__()
        self.env = env
        self.setLevel(logging.WARNING)  # Only capture WARNING and above
        
    def emit(self, record):
        """Process log record and create error event if needed"""
        try:
            # Skip if not a warning or error
            if record.levelno < logging.WARNING:
                return
                
            # Get log file information
            log_file_path = self._get_log_file_path()
            log_line_number = self._get_current_log_line(log_file_path)
            
            # Map log levels to our severity levels
            severity_map = {
                logging.WARNING: 'warning',
                logging.ERROR: 'error', 
                logging.CRITICAL: 'critical'
            }
            
            # Create error event
            with self.env.registry.cursor() as cr:
                env = api.Environment(cr, 1, {})  # Use admin user
                try:
                    env['qa.error.event'].create({
                        'source': 'server',
                        'scenario': 'odoo_log',
                        'severity': severity_map.get(record.levelno, 'error'),
                        'message': record.getMessage(),
                        'details': self._format_log_details(record),
                        'log_file_path': log_file_path,
                        'log_line_number': log_line_number,
                        'log_level': record.levelname,
                        'project': self._extract_project_from_record(record),
                        'tags': f'logger:{record.name}',
                    })
                    cr.commit()
                except Exception as e:
                    _logger.debug(f"Failed to create error event from log: {e}")
                    
        except Exception:
            # Don't let log handler errors break the system
            pass
    
    def _get_log_file_path(self):
        """Get the current Odoo log file path"""
        # Try common log file locations
        possible_paths = [
            '/var/log/odoo/odoo.log',
            '/var/log/odoo/odoo-server.log', 
            '/home/odoo/odoo.log',
            './odoo.log',
            os.path.expanduser('~/odoo.log')
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                return path
                
        # Check environment variables
        log_file = os.environ.get('ODOO_LOG_FILE')
        if log_file and os.path.exists(log_file):
            return log_file
            
        return 'odoo.log'  # fallback
    
    def _get_current_log_line(self, log_file_path):
        """Estimate current line number in log file"""
        try:
            if os.path.exists(log_file_path):
                with open(log_file_path, 'r') as f:
                    return sum(1 for line in f)
        except:
            pass
        return 0
    
    def _format_log_details(self, record):
        """Format detailed log information"""
        details = []
        details.append(f"Logger: {record.name}")
        details.append(f"Module: {record.module if hasattr(record, 'module') else 'unknown'}")
        details.append(f"Function: {record.funcName}")
        details.append(f"Line: {record.lineno}")
        details.append(f"Time: {datetime.fromtimestamp(record.created)}")
        
        if record.exc_info:
            details.append("Exception Details:")
            details.append(''.join(traceback.format_exception(*record.exc_info)))
            
        return '\n'.join(details)
    
    def _extract_project_from_record(self, record):
        """Extract project/module name from log record"""
        if hasattr(record, 'module') and record.module:
            return record.module
        
        # Try to extract from logger name
        logger_parts = record.name.split('.')
        if len(logger_parts) > 1:
            return logger_parts[1]  # Usually odoo.addons.module_name
            
        return 'odoo_server'


class LogHandlerManager(models.TransientModel):
    """Model to manage log handler registration"""
    _name = 'qa.log.handler.manager'
    _description = 'Log Handler Manager'
    
    @api.model
    def register_log_handler(self):
        """Register our custom log handler with Odoo's logging system"""
        try:
            # Get the root logger
            root_logger = logging.getLogger()
            
            # Check if our handler is already registered
            handler_exists = any(
                isinstance(h, OdooLogHandler) 
                for h in root_logger.handlers
            )
            
            if not handler_exists:
                # Create and register the handler
                handler = OdooLogHandler(self.env)
                root_logger.addHandler(handler)
                _logger.info("QA Error Reporter log handler registered successfully")
                return True
            else:
                _logger.debug("QA Error Reporter log handler already registered")
                return False
                
        except Exception as e:
            _logger.error(f"Failed to register log handler: {e}")
            return False
    
    @api.model
    def unregister_log_handler(self):
        """Unregister our custom log handler"""
        try:
            root_logger = logging.getLogger()
            handlers_to_remove = [
                h for h in root_logger.handlers 
                if isinstance(h, OdooLogHandler)
            ]
            
            for handler in handlers_to_remove:
                root_logger.removeHandler(handler)
                
            if handlers_to_remove:
                _logger.info("QA Error Reporter log handler unregistered")
                return True
            return False
                
        except Exception as e:
            _logger.error(f"Failed to unregister log handler: {e}")
            return False
    
    @api.model
    def test_log_capture(self):
        """Test method to generate sample log entries"""
        _logger.warning("Test warning message from Error Reporter")
        _logger.error("Test error message from Error Reporter")
        return "Test log entries generated"