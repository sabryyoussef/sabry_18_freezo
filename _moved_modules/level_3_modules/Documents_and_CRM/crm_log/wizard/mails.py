from odoo import api, fields, models

class MailComposeMessages(models.TransientModel):
    _inherit = 'mail.compose.message'

    def action_send_mail(self):
        res = super(MailComposeMessages, self).action_send_mail()
        if self.model == 'crm.lead' and self.res_ids:
            try:
                record_id = self.res_ids[0] if isinstance(self.res_ids, list) else int(self.res_ids)
                record = self.env['crm.lead'].sudo().search([('id', '=', record_id)], limit=1)
                if record:
                    record.mail_sent = True
            except (ValueError, TypeError, IndexError):
                pass
        return res
