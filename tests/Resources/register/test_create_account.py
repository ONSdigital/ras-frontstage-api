import base64
import json
import unittest

import requests_mock

from frontstage_api import app


url_get_iac = f"{app.config['RM_IAC_SERVICE']}/iacs/test_enrolment"
url_create_account = f"{app.config['RAS_PARTY_SERVICE']}/party-api/v1/respondents"


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
        self.iac_response = {
            "iac": "test_enrolment",
            "active": True,
            "lastUsedDateTime": "2017-05-15T10:00:00Z",
            "caseId": "test_case_id",
            "questionSet": "H1"
        }
        self.registration_form = {
            "enrolmentCode": "test_enrolment",
            "emailAddress": "test_user@ons.gov",
            "password": "password",
            "telephone": "0202020202",
            "firstName": "Andrew",
            "lastName": "Millar"
        }

    @requests_mock.mock()
    def test_create_account_success(self, mock_request):
        mock_request.get(url_get_iac, json=self.iac_response)
        mock_request.post(url_create_account)

        response = self.app.post('/register/create-account', headers=self.headers,
                                 data=json.dumps(self.registration_form))

        self.assertEqual(response.status_code, 201)

    @requests_mock.mock()
    def test_create_account_inactive_iac(self, mock_request):
        self.iac_response['active'] = False
        mock_request.get(url_get_iac, json=self.iac_response)

        response = self.app.post('/register/create-account', headers=self.headers,
                                 data=json.dumps(self.registration_form))

        self.assertEqual(response.status_code, 401)
        self.assertTrue('"active": false'.encode() in response.data)

    @requests_mock.mock()
    def test_create_account_party_fail(self, mock_request):
        mock_request.get(url_get_iac, json=self.iac_response)
        mock_request.post(url_create_account, status_code=500)

        response = self.app.post('/register/create-account', headers=self.headers,
                                 data=json.dumps(self.registration_form))

        self.assertEqual(response.status_code, 500)
        self.assertTrue('"status_code": 500'.encode() in response.data)

    @requests_mock.mock()
    def test_create_account_party_400(self, mock_request):
        mock_request.get(url_get_iac, json=self.iac_response)
        mock_request.post(url_create_account, status_code=400)

        response = self.app.post('/register/create-account', headers=self.headers,
                                 data=json.dumps(self.registration_form))

        self.assertEqual(response.status_code, 400)
        self.assertTrue('"status_code": 400'.encode() in response.data)

    # Test posting to endpoint without basic auth in header
    def test_create_account_no_basic_auth(self):
        del self.headers['Authorization']
        response = self.app.post('/register/create-account', headers=self.headers,
                                 data=json.dumps(self.registration_form))

        self.assertEqual(response.status_code, 401)
