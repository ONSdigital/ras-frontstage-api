import base64
import unittest

import requests_mock

from frontstage_api import app

url_resend_verification_email = app.config['RAS_PARTY_RESEND_VERIFICATION_EMAIL'].format('test_party_id')


class TestRegister(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Basic {}'.format(base64.b64encode(
                bytes("{}:{}".format(app.config['SECURITY_USER_NAME'], app.config['SECURITY_USER_PASSWORD']), 'ascii')
            ).decode("ascii"))
        }
        self.valid_response = {"message": "A new verification email has been sent"}
        self.invalid_party_response = {"message": "There is no respondent with that party ID "}

    @requests_mock.mock()
    def test_resend_verification_email(self, mock_request):
        mock_request.get(url_resend_verification_email, status_code=200, json=self.valid_response)

        response = self.app.post('/register/resend-verification-email?party_id=test_party_id', headers=self.headers)

        self.assertEqual(response.status_code, 200)

    @requests_mock.mock()
    def test_resend_verification_email_fail_no_party(self, mock_request):
        mock_request.get(url_resend_verification_email, status_code=404, json=self.invalid_party_response)

        response = self.app.post('/register/resend-verification-email?party_id=test_party_id', headers=self.headers)

        self.assertEqual(response.status_code, 404)
        self.assertTrue('"status_code": 404'.encode() in response.data)

    @requests_mock.mock()
    def test_resend_verification_email_fail_notification_error(self, mock_request):
        mock_request.get(url_resend_verification_email, status_code=500)

        response = self.app.post('/register/resend-verification-email?party_id=test_party_id', headers=self.headers)

        self.assertEqual(response.status_code, 500)
        self.assertTrue('"status_code": 500'.encode() in response.data)

    def test_verify_email_no_basic_auth(self):
        del self.headers['Authorization']
        response = self.app.post('/register/resend-verification-email?party_id=test_party_id', headers=self.headers)

        self.assertEqual(response.status_code, 401)
