import pytest
from odoo.tests.common import TransactionCase

class TestQAErrorEvent(TransactionCase):

    def setUp(self):
        super(TestQAErrorEvent, self).setUp()
        self.EventModel = self.env['qa.error.event']

    def test_create_event(self):
        event = self.EventModel.create({
            'source': 'odoo_ui',
            'severity': 'error',
            'message': 'Test error message',
            'project': 'Test Project',
            'scenario': 'Test Scenario',
            'user_login': 'test_user',
            'url': 'http://example.com',
            'browser': 'Chrome',
            'trace_url': 'http://trace.example.com',
            'details': 'Detailed error information',
            'fingerprint': 'test_fingerprint',
            'tags': 'test, error'
        })
        self.assertTrue(event.id)
        self.assertEqual(event.source, 'odoo_ui')
        self.assertEqual(event.severity, 'error')

    def test_fingerprint_computation(self):
        event = self.EventModel.create({
            'source': 'playwright',
            'message': 'Another test error message',
            'scenario': 'Another Test Scenario',
            'url': 'http://example.com/test',
        })
        expected_fingerprint = 'playwrightAnother Test Scenariohttp://example.com/testAnother test error message'.encode('utf-8')
        self.assertEqual(event.fingerprint, self.EventModel._compute_fingerprint(expected_fingerprint))

    def test_access_rights(self):
        user = self.env['res.users'].create({
            'name': 'Test User',
            'login': 'test_user',
            'groups_id': [(6, 0, [self.env.ref('base.group_user').id])]
        })
        self.assertTrue(self.EventModel.check_access_rights('read'))
        self.assertTrue(self.EventModel.check_access_rights('create'))
        self.assertFalse(self.EventModel.check_access_rights('unlink'))