import base64
import json
import unittest

import requests_mock

from frontstage_api import app


url_get_token = app.config['OAUTH_TOKEN_URL']
url_reset_password_request = app.config['RAS_PARTY_RESET_PASSWORD_REQUEST']


class TestRequestPasswordChange(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.headers = {
            'Authorization': 'Basic {}'.format(base64.b64encode(
                bytes("{}:{}".format(app.config['SECURITY_USER_NAME'], app.config['SECURITY_USER_PASSWORD']), 'ascii')
            ).decode("ascii")),
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

    @requests_mock.mock()
    def test_request_password_change_success(self, mock_request):
        mock_request.post(url_get_token, status_code=201, json=self.oauth2_response)
        mock_request.post(url_reset_password_request, status_code=200)

        response = self.app.post('/request-password-change', headers=self.headers, data=json.dumps(self.posted_form))

        self.assertEqual(response.status_code, 200)

    @requests_mock.mock()
    def test_request_password_change_oauth_fail(self, mock_request):
        mock_request.post(url_get_token, status_code=500)

        response = self.app.post('/request-password-change', headers=self.headers, data=json.dumps(self.posted_form))

        self.assertEqual(response.status_code, 500)
        self.assertTrue('"status_code": 500'.encode() in response.data)

    @requests_mock.mock()
    def test_request_password_change_oauth_oauth_401_error(self, mock_request):
        mock_request.post(url_get_token, status_code=401, json=self.oauth2_error)

        response = self.app.post('/request-password-change', headers=self.headers, data=json.dumps(self.posted_form))

        self.assertEqual(response.status_code, 401)
        self.assertTrue('"detail": "test error"'.encode() in response.data)

    @requests_mock.mock()
    def test_request_password_change_party_fail(self, mock_request):
        mock_request.post(url_get_token, status_code=201, json=self.oauth2_response)
        mock_request.post(url_reset_password_request, status_code=500)

        response = self.app.post('/request-password-change', headers=self.headers, data=json.dumps(self.posted_form))

        self.assertEqual(response.status_code, 500)
        self.assertTrue('"status_code": 500'.encode() in response.data)

    @requests_mock.mock()
    def test_request_password_change_party_username_not_found(self, mock_request):
        mock_request.post(url_get_token, status_code=201, json=self.oauth2_response)
        mock_request.post(url_reset_password_request, status_code=404)

        response = self.app.post('/request-password-change', headers=self.headers, data=json.dumps(self.posted_form))

        self.assertEqual(response.status_code, 404)
        self.assertTrue('"status_code": 404'.encode() in response.data)

    # Test posting to endpoint without basic auth in header
    def test_request_password_change_no_basic_auth(self):
        del self.headers['Authorization']
        response = self.app.post('/request-password-change', headers=self.headers, data=json.dumps(self.posted_form))

        self.assertEqual(response.status_code, 401)
