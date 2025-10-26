import logging
import werkzeug

from odoo import http
from odoo.http import request
from odoo.tools.translate import _

_logger = logging.getLogger(__name__)

MAPPED_RATES = {
    1: 1,
    5: 3,
    10: 5,
}


class Rating(http.Controller):

    @http.route('/rate/<string:token>/<int:rate>', type='http', auth="public", website=True)
    def action_open_rating(self, token, rate, **kwargs):
        """Handle rating submission with token and rate"""
        try:
            rating, record_sudo = self._get_rating_and_record(token)
            _logger.info(f'Rating record: {record_sudo.display_name}')
            
            # Apply the rating
            record_sudo.rating_apply(
                rate,
                rating=rating,
                feedback=_('Customer rated %r.', record_sudo.display_name),
                subtype_xmlid=None,
                notify_delay_send=True,
            )

            # Render the response template
            lang = rating.partner_id.lang or request.env.context.get('lang', 'en_US')
            return request.env['ir.ui.view'].with_context(lang=lang)._render_template(
                'freezoner_custom.rating_external_page_submit_custom',
                {
                    'rating': rating,
                    'token': token,
                    'rate_priority': {
                        0: _("Zero"),
                        1: _("Low"),
                        2: _("Normal"),
                        3: _("Medium"),
                        4: _("High"),
                        5: _("Very High"),
                    },
                    'rate': rate,
                }
            )
        except Exception as e:
            _logger.error(f"Error in action_open_rating: {str(e)}")
            raise werkzeug.exceptions.NotFound()

    @http.route(['/rate/<string:token>/submit_feedback'], type="http", auth="public", methods=['post', 'get'], website=True)
    def action_submit_rating(self, token, rate=0, **kwargs):
        """Handle rating feedback submission"""
        try:
            rating, record_sudo = self._get_rating_and_record(token)
            
            if request.httprequest.method == "POST":
                rate = int(rate)
                feedback = kwargs.get('feedback', '')
                
                record_sudo.rating_apply(
                    rate,
                    rating=rating,
                    feedback=feedback,
                    subtype_xmlid=None,  # force default subtype choice
                )

            # Render the response template
            lang = rating.partner_id.lang or request.env.context.get('lang', 'en_US')
            return request.env['ir.ui.view'].with_context(lang=lang)._render_template(
                'rating.rating_external_page_view', 
                {
                    'web_base_url': rating.get_base_url(),
                    'rating': rating,
                }
            )
        except Exception as e:
            _logger.error(f"Error in action_submit_rating: {str(e)}")
            raise werkzeug.exceptions.NotFound()

    def _get_rating_and_record(self, token):
        """Get rating and associated record by token"""
        try:
            rating_sudo = request.env['rating.rating'].sudo().search([('access_token', '=', token)])
            if not rating_sudo:
                _logger.warning(f"No rating found for token: {token}")
                raise werkzeug.exceptions.NotFound()

            record_sudo = request.env[rating_sudo.res_model].sudo().browse(rating_sudo.res_id)
            if not record_sudo.exists():
                _logger.warning(f"Record not found for rating: {rating_sudo.id}")
                raise werkzeug.exceptions.NotFound()
                
            return rating_sudo, record_sudo
        except Exception as e:
            _logger.error(f"Error in _get_rating_and_record: {str(e)}")
            raise werkzeug.exceptions.NotFound()
