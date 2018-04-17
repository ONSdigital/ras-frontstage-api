import base64
import unittest

import requests_mock

from frontstage_api import app

url_verify_email = f"{app.config['RAS_PARTY_SERVICE']}/party-api/v1/emailverification/test_token"


class TestRegister(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        auth_string = base64.b64encode(
            bytes(f"{app.config['SECURITY_USER_NAME']}:{app.config['SECURITY_USER_PASSWORD']}", 'ascii')
        ).decode("ascii")
        self.headers = {
            'Authorization': f'Basic {auth_string}',
            'Content-Type': 'application/json',
        }

    @requests_mock.mock()
    def test_verify_email(self, mock_request):
        mock_request.put(url_verify_email, status_code=200)

        response = self.app.put('/register/verify-email?token=test_token', headers=self.headers)

        self.assertEqual(response.status_code, 200)

    @requests_mock.mock()
    def test_verify_email_fail(self, mock_request):
        mock_request.put(url_verify_email, status_code=500)

        response = self.app.put('/register/verify-email?token=test_token', headers=self.headers)

        self.assertEqual(response.status_code, 500)
        self.assertTrue('"status_code": 500'.encode() in response.data)

    # Test posting to endpoint without basic auth in header
    def test_verify_email_no_basic_auth(self):
        del self.headers['Authorization']
        response = self.app.put('/register/verify-email?token=test_token', headers=self.headers)

        self.assertEqual(response.status_code, 401)
