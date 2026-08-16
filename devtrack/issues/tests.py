import json
import tempfile
from pathlib import Path
from unittest.mock import patch

from django.test import TestCase


class ApiTests(TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.reporters_file = Path(self.temp_dir.name) / 'reporters.json'
        self.issues_file = Path(self.temp_dir.name) / 'issues.json'
        self.reporters_file.write_text(json.dumps([
            {
                'id': 1,
                'name': 'Alice Engineer',
                'email': 'alice@example.com',
                'team': 'backend',
            },
        ]), encoding='utf-8')
        self.issues_file.write_text(json.dumps([]), encoding='utf-8')
        self.file_patches = [
            patch('issues.views.REPORTERS_FILE', self.reporters_file),
            patch('issues.views.ISSUES_FILE', self.issues_file),
        ]
        for file_patch in self.file_patches:
            file_patch.start()

    def tearDown(self):
        for file_patch in reversed(self.file_patches):
            file_patch.stop()
        self.temp_dir.cleanup()

    def test_api_root_lists_endpoints(self):
        response = self.client.get('/api/')

        self.assertEqual(response.status_code, 200)
        self.assertIn('/api/issues/', response.json()['endpoints'])

    def test_reporter_can_be_created_and_retrieved(self):
        response = self.client.post('/api/reporters/', {
            'id': 2,
            'name': 'Bob Builder',
            'email': 'bob@example.com',
            'team': 'frontend',
        }, content_type='application/json')

        self.assertEqual(response.status_code, 201)
        self.assertEqual(self.client.get('/api/reporters/?id=2').json()['name'], 'Bob Builder')

    def test_issue_creation_uses_priority_description_and_status_filter(self):
        response = self.client.post('/api/issues/', {
            'id': 10,
            'title': 'Broken login',
            'description': 'Login fails on mobile',
            'status': 'open',
            'priority': 'critical',
            'reporter_id': 1,
        }, content_type='application/json')

        self.assertEqual(response.status_code, 201)
        self.assertTrue(response.json()['message'].startswith('[URGENT]'))
        filtered = self.client.get('/api/issues/?status=open')
        self.assertEqual(filtered.status_code, 200)
        self.assertEqual([issue['id'] for issue in filtered.json()], [10])

    def test_unknown_records_and_reporters_return_404_or_400(self):
        self.assertEqual(self.client.get('/api/reporters/?id=999').status_code, 404)
        self.assertEqual(self.client.get('/api/issues/?id=999').status_code, 404)
        response = self.client.post('/api/issues/', {
            'id': 11,
            'title': 'Unassigned issue',
            'description': 'No reporter exists',
            'status': 'open',
            'priority': 'medium',
            'reporter_id': 999,
        }, content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_invalid_json_shapes_and_values_return_400(self):
        for endpoint in ('/api/reporters/', '/api/issues/'):
            response = self.client.post(endpoint, '[]', content_type='application/json')
            self.assertEqual(response.status_code, 400)
            self.assertEqual(response.json()['error'], 'JSON object required')

        response = self.client.post('/api/reporters/', {
            'id': 3,
            'name': 'No Email',
        }, content_type='application/json')
        self.assertEqual(response.status_code, 400)

        self.assertEqual(self.client.get('/api/reporters/?id=abc').status_code, 400)
        self.assertEqual(self.client.get('/api/issues/?id=abc').status_code, 400)

    def test_duplicate_reporter_returns_400(self):
        response = self.client.post('/api/reporters/', {
            'id': 1,
            'name': 'Another Alice',
            'email': 'another@example.com',
            'team': 'backend',
        }, content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertIn('already exists', response.json()['error'])

    def test_invalid_issue_status_and_priority_return_400(self):
        for field, value in (('status', 'pending'), ('priority', 'urgent')):
            payload = {
                'id': 20,
                'title': 'Invalid issue',
                'description': 'Invalid value',
                'status': 'open',
                'priority': 'medium',
                'reporter_id': 1,
            }
            payload[field] = value
            response = self.client.post('/api/issues/', payload, content_type='application/json')
            self.assertEqual(response.status_code, 400)

    def test_low_priority_issue_uses_low_priority_message(self):
        response = self.client.post('/api/issues/', {
            'id': 21,
            'title': 'Minor UI issue',
            'description': 'Small spacing problem',
            'status': 'open',
            'priority': 'low',
            'reporter_id': 1,
        }, content_type='application/json')

        self.assertEqual(response.status_code, 201)
        self.assertIn('low priority', response.json()['message'])

    def test_unsupported_methods_return_405(self):
        self.assertEqual(self.client.put('/api/reporters/').status_code, 405)
        self.assertEqual(self.client.put('/api/issues/').status_code, 405)
