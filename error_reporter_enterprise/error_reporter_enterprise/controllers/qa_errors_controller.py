from odoo import http, fields, _
from odoo.http import request
from odoo.exceptions import ValidationError
import hashlib
import datetime
import json
import logging

_logger = logging.getLogger(__name__)

class QaErrorsController(http.Controller):

    @http.route('/qa/errors/ingest', type='json', auth='none', methods=['POST'], csrf=False)
    def ingest_errors(self, **kwargs):
        """Ingest error reports from various sources"""
        try:
            # Validate authentication token
            token = request.httprequest.headers.get('X-QA-TOKEN')
            expected_token = request.env['ir.config_parameter'].sudo().get_param('qa.error.api_token')

            if not expected_token:
                _logger.warning('QA error API token not configured')
                return request.make_response('Service not configured', status=503)

            if token != expected_token:
                _logger.warning('Invalid QA error API token received')
                return request.make_response('Unauthorized', status=401)

            # Validate payload
            required_fields = ['source', 'message', 'severity']
            for field in required_fields:
                if field not in kwargs:
                    return request.make_response(f'Missing field: {field}', status=400)

            # Validate field values
            valid_sources = ['odoo_ui', 'odoo_server', 'playwright']
            valid_severities = ['info', 'warning', 'error', 'critical']
            
            if kwargs.get('source') not in valid_sources:
                return request.make_response(f'Invalid source. Must be one of: {valid_sources}', status=400)
            
            if kwargs.get('severity') not in valid_severities:
                return request.make_response(f'Invalid severity. Must be one of: {valid_severities}', status=400)

            # Validate message length
            message = kwargs.get('message', '')
            if len(message) > 5000:
                return request.make_response('Message too long (max 5000 characters)', status=400)

            # Compute fingerprint server-side if not provided
            provided_fp = kwargs.get('fingerprint')
            src = kwargs.get('source') or ''
            scn = kwargs.get('scenario') or ''
            url = kwargs.get('url') or ''
            msg = message
            first_line = msg.splitlines()[0] if msg else ''
            key = provided_fp or (src + scn + url + first_line)
            fp = None
            if key:
                fp = hashlib.sha1(key.encode('utf-8')).hexdigest()

            # Dedup / rate-limit: if same fingerprint exists within last 5 minutes, increment occurrences
            if fp:
                qa_model = request.env['qa.error.event'].sudo()
                recent = qa_model.search([('fingerprint', '=', fp)], order='create_date desc', limit=1)
                if recent:
                    try:
                        recent_dt = fields.Datetime.from_string(recent.create_date)
                        threshold = fields.Datetime.from_string(fields.Datetime.now()) - datetime.timedelta(minutes=5)
                    except Exception as e:
                        _logger.warning('Error parsing dates for deduplication: %s', e)
                        recent_dt = None
                        threshold = None

                    if recent_dt and threshold and recent_dt >= threshold:
                        # bump occurrences and return existing id
                        try:
                            recent.sudo().write({'occurrences': (recent.occurrences or 1) + 1})
                        except Exception as e:
                            # ignore write errors but still return existing id
                            _logger.warning('Failed to update occurrences: %s', e)
                        return {'ok': True, 'id': recent.id, 'deduped': True}

            # Create the error event
            try:
                error_event = request.env['qa.error.event'].sudo().create({
                    'source': kwargs.get('source'),
                    'severity': kwargs.get('severity'),
                    'project': kwargs.get('project'),
                    'scenario': kwargs.get('scenario'),
                    'user_login': kwargs.get('user_login'),
                    'url': kwargs.get('url'),
                    'browser': kwargs.get('browser'),
                    'trace_url': kwargs.get('trace_url'),
                    'message': message,
                    'details': kwargs.get('details'),
                    'fingerprint': fp,
                    'tags': kwargs.get('tags'),
                })
                return {'ok': True, 'id': error_event.id}
            except ValidationError as e:
                return request.make_response(f'Validation error: {e}', status=400)
            except Exception as e:
                _logger.error('Failed to create error event: %s', e)
                return request.make_response('Internal server error', status=500)

        except Exception as e:
            _logger.error('Unexpected error in error ingest: %s', e)
            return request.make_response('Internal server error', status=500)

    @http.route('/qa/errors/token', type='json', auth='user', methods=['GET'])
    def get_token(self, **kwargs):
        """Return the configured QA token for authenticated users so frontend can read it from a controlled endpoint."""
        try:
            token = request.env['ir.config_parameter'].sudo().get_param('qa.error.api_token')
            if not token:
                _logger.warning('QA error API token not configured')
                return {'error': 'Token not configured'}
            return {'token': token}
        except Exception as e:
            _logger.error('Error retrieving QA token: %s', e)
            return {'error': 'Internal server error'}