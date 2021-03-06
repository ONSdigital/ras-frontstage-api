import base64
import json
import unittest

import requests_mock

from frontstage_api import app

url_change_password = f"{app.config['RAS_PARTY_SERVICE']}/party-api/v1/respondents/change_password/nekoT"


class TestChangePassword(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        auth_string = base64.b64encode(
            bytes(f"{app.config['SECURITY_USER_NAME']}:{app.config['SECURITY_USER_PASSWORD']}", 'ascii')
        ).decode("ascii")
        self.headers = {
            'Authorization': f'Basic {auth_string}',
            'Content-Type': 'application/json',
        }
        self.posted_form = dict(token='nekoT', new_password='new_password')

        self.oauth2_response = {
            'id': 1,
            'access_token': '99a81f9c-e827-448b-8fa7-d563b76137ca',
            'expires_in': 3600,
            'token_type': 'Bearer',
            'scope': '',
            'refresh_token': 'a74fd471-6981-4503-9f59-00d45d339a15'
        }
        self.oauth2_error = {
            'detail': 'test error'
        }

    @requests_mock.mock()
    def test_change_password_successful(self, mock_request):
        mock_request.put(url_change_password, status_code=200)

        response = self.app.put('/passwords/change-password', headers=self.headers, data=json.dumps(self.posted_form))

        self.assertEqual(response.status_code, 200)

    @requests_mock.mock()
    def test_change_password_party_fail(self, mock_request):
        mock_request.put(url_change_password, status_code=500)

        response = self.app.put('/passwords/change-password', headers=self.headers, data=json.dumps(self.posted_form))

        self.assertEqual(response.status_code, 500)
        self.assertIn('"status_code": 500'.encode(), response.data)

    @requests_mock.mock()
    def test_change_password_token_expired(self, mock_request):
        mock_request.put(url_change_password, status_code=409)

        response = self.app.put('/passwords/change-password', headers=self.headers, data=json.dumps(self.posted_form))

        self.assertEqual(response.status_code, 409)
        self.assertIn('"status_code": 409'.encode(), response.data)

    @requests_mock.mock()
    def test_change_password_invalid(self, mock_request):
        mock_request.put(url_change_password, status_code=404)

        response = self.app.put('/passwords/change-password', headers=self.headers, data=json.dumps(self.posted_form))

        self.assertEqual(response.status_code, 404)
        self.assertIn('"status_code": 404'.encode(), response.data)

    # Test posting to endpoint without basic auth in header
    def test_password_change_no_basic_auth(self):
        del self.headers['Authorization']
        response = self.app.put('/passwords/change-password', headers=self.headers, data=json.dumps(self.posted_form))

        self.assertEqual(response.status_code, 401)
