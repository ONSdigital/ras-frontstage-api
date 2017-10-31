import base64
import json
import unittest

import requests_mock

from frontstage_api import app


url_get_token = app.config['OAUTH_TOKEN_URL']
url_get_party_by_email = app.config['RAS_PARTY_GET_BY_EMAIL_URL'].format('test')
with open('tests/test_data/party/party.json') as json_data:
    party = json.load(json_data)


class TestSignIn(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.headers = {
            'Authorization': 'Basic {}'.format(base64.b64encode(bytes("{}:{}".format(app.config['SECURITY_USER_NAME'], app.config['SECURITY_USER_PASSWORD']), 'ascii')).decode("ascii"))
        }
        self.posted_form = {
            'username': 'test',
            'password': 'test'
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
    def test_sign_in_success(self, mock_request):
        mock_request.post(url_get_token, status_code=201, json=self.oauth2_response)
        mock_request.get(url_get_party_by_email, status_code=200, json=party)

        response = self.app.post('/sign-in', headers=self.headers, data=json.dumps(self.posted_form))

        self.assertEqual(response.status_code, 200)
        self.assertTrue('"party_id": "07d672bc-497b-448f-a406-a20a7e6013d7"'.encode() in response.data)
        self.assertTrue('"access_token": "99a81f9c-e827-448b-8fa7-d563b76137ca"'.encode() in response.data)

    @requests_mock.mock()
    def test_sign_in_oauth_fail(self, mock_request):
        mock_request.post(url_get_token, status_code=500)

        response = self.app.post('/sign-in', headers=self.headers, data=json.dumps(self.posted_form))

        self.assertEqual(response.status_code, 500)
        self.assertTrue('"status_code": 500'.encode() in response.data)

    @requests_mock.mock()
    def test_sign_in_oauth_401_error(self, mock_request):
        mock_request.post(url_get_token, status_code=401, json=self.oauth2_error)

        response = self.app.post('/sign-in', headers=self.headers, data=json.dumps(self.posted_form))

        self.assertEqual(response.status_code, 401)
        self.assertTrue('"detail": "test error"'.encode() in response.data)

    @requests_mock.mock()
    def test_sign_in_party_fail(self, mock_request):
        mock_request.post(url_get_token, status_code=201, json=self.oauth2_response)
        mock_request.get(url_get_party_by_email, status_code=500)

        response = self.app.post('/sign-in', headers=self.headers, data=json.dumps(self.posted_form))

        self.assertEqual(response.status_code, 500)
        self.assertTrue('"status_code": 500'.encode() in response.data)
