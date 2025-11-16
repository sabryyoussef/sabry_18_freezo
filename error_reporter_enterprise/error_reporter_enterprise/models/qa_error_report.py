# -*- coding: utf-8 -*-
from odoo import api, models


class QAErrorReportXlsx(models.AbstractModel):
    _name = 'report.error_reporter_enterprise.report_all_errors_template'
    _description = 'QA Error Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        """Get all error records for the report"""
        # Always fetch all error records regardless of docids
        QAErrorEvent = self.env['qa.error.event']
        docs = QAErrorEvent.search([])
        
        return {
            'doc_ids': [d.id for d in docs],
            'doc_model': 'qa.error.event',
            'docs': docs,
            'data': data,
        }