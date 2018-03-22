import base64
import json
import unittest

import requests_mock

from frontstage_api import app


url_verify_token = app.config['RAS_PARTY_VERIFY_PASSWORD_TOKEN']


class TestVerifyPasswordToken(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        auth_string = base64.b64encode(
            bytes(f"{app.config['SECURITY_USER_NAME']}:{app.config['SECURITY_USER_PASSWORD']}", 'ascii')
        ).decode("ascii")
        self.headers = {
            'Authorization': f'Basic {auth_string}',
            'Content-Type': 'application/json',
        }
        self.posted_form = {
            'username': 'test'
        }
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
        self.params = dict(token='nekoT')

    @requests_mock.mock()
    def test_verify_password_token_successful(self, mock_request):
        mock_request.get(url_verify_token.format('nekoT'), status_code=200, json={"status": "OKs"})

        response = self.app.get('/passwords/verify-password-token', headers=self.headers, query_string=self.params)

        self.assertEqual(response.status_code, 200)

    @requests_mock.mock()
    def test_verify_password_token_party_fail(self, mock_request):
        mock_request.get(url_verify_token.format('nekoT'), status_code=500)

        response = self.app.get('/passwords/verify-password-token', headers=self.headers, query_string=self.params)

        self.assertEqual(response.status_code, 500)
        self.assertTrue('"status_code": 500'.encode() in response.data)

    @requests_mock.mock()
    def test_verify_password_token_token_expired(self, mock_request):
        mock_request.get(url_verify_token.format('nekoT'), status_code=409)

        response = self.app.get('/passwords/verify-password-token', headers=self.headers, query_string=self.params)

        self.assertEqual(response.status_code, 409)
        self.assertTrue('"status_code": 409'.encode() in response.data)

    @requests_mock.mock()
    def test_verify_password_token_token_invalid(self, mock_request):
        mock_request.get(url_verify_token.format('nekoT'), status_code=404)

        response = self.app.get('/passwords/verify-password-token', headers=self.headers, query_string=self.params)

        self.assertEqual(response.status_code, 404)
        self.assertTrue('"status_code": 404'.encode() in response.data)

    # Test posting to endpoint without basic auth in header
    def test_verify_password_token_no_basic_auth(self):
        del self.headers['Authorization']
        response = self.app.get('/passwords/verify-password-token', headers=self.headers, data=json.dumps(self.posted_form))

        self.assertEqual(response.status_code, 401)
