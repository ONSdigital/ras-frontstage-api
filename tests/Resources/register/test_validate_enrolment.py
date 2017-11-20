import base64
import json
import unittest

import requests_mock

from frontstage_api import app


url_get_iac = app.config['RM_IAC_GET'].format('test_enrolment')
url_get_case_by_enrolment = app.config['RM_CASE_GET_BY_IAC'].format('test_enrolment')
with open('tests/test_data/case/case.json') as json_data:
    case = json.load(json_data)
url_get_case_categories = app.config['RM_CASE_GET_CATEGORIES']
with open('tests/test_data/case/categories.json') as json_data:
    categories = json.load(json_data)
url_post_case_event = app.config['RM_CASE_POST_CASE_EVENT'].format('test_case_id')


class TestRegister(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Basic {}'.format(base64.b64encode(
                bytes("{}:{}".format(app.config['SECURITY_USER_NAME'], app.config['SECURITY_USER_PASSWORD']), 'ascii')
            ).decode("ascii"))
        }
        self.enrolment_json = {
            'enrolment_code': 'test_enrolment',
            'initial': True
        }
        self.iac_response = {
            "iac": "test_enrolment",
            "active": True,
            "lastUsedDateTime": "2017-05-15T10:00:00Z",
            "caseId": "test_case_id",
            "questionSet": "H1"
        }

    @requests_mock.mock()
    def test_validate_enrolment_success(self, mock_request):
        mock_request.get(url_get_iac, json=self.iac_response)
        mock_request.get(url_get_case_by_enrolment, json=case)
        mock_request.get(url_get_case_categories, json=categories)
        mock_request.post(url_post_case_event, status_code=201)

        response = self.app.post('/register/validate-enrolment', headers=self.headers,
                                 data=json.dumps(self.enrolment_json))

        self.assertEqual(response.status_code, 200)

    @requests_mock.mock()
    def test_validate_enrolment_iac_inactive(self, mock_request):
        self.iac_response['active'] = False
        mock_request.get(url_get_iac, json=self.iac_response)

        response = self.app.post('/register/validate-enrolment', headers=self.headers,
                                 data=json.dumps(self.enrolment_json))

        self.assertEqual(response.status_code, 401)
        self.assertTrue('"active": false'.encode() in response.data)

    @requests_mock.mock()
    def test_validate_enrolment_iac_fail(self, mock_request):
        mock_request.get(url_get_iac, status_code=500)

        response = self.app.post('/register/validate-enrolment', headers=self.headers,
                                 data=json.dumps(self.enrolment_json))

        self.assertEqual(response.status_code, 500)
        self.assertTrue('"status_code": 500'.encode() in response.data)

    @requests_mock.mock()
    def test_validate_enrolment_iac_404(self, mock_request):
        mock_request.get(url_get_iac, status_code=404)

        response = self.app.post('/register/validate-enrolment', headers=self.headers,
                                 data=json.dumps(self.enrolment_json))

        self.assertEqual(response.status_code, 404)
        self.assertTrue('"status_code": 404'.encode() in response.data)

    @requests_mock.mock()
    def test_validate_enrolment_case_get_fail(self, mock_request):
        mock_request.get(url_get_iac, json=self.iac_response)
        mock_request.get(url_get_case_by_enrolment, status_code=500)

        response = self.app.post('/register/validate-enrolment', headers=self.headers,
                                 data=json.dumps(self.enrolment_json))

        self.assertEqual(response.status_code, 500)
        self.assertTrue('"status_code": 500'.encode() in response.data)

    @requests_mock.mock()
    def test_validate_enrolment_get_categories_fail(self, mock_request):
        mock_request.get(url_get_iac, json=self.iac_response)
        mock_request.get(url_get_case_by_enrolment, json=case)
        mock_request.get(url_get_case_categories, status_code=500)

        response = self.app.post('/register/validate-enrolment', headers=self.headers,
                                 data=json.dumps(self.enrolment_json))

        self.assertEqual(response.status_code, 500)
        self.assertTrue('"status_code": 500'.encode() in response.data)

    @requests_mock.mock()
    def test_validate_enrolment_invalid_case_category(self, mock_request):
        mock_request.get(url_get_iac, json=self.iac_response)
        mock_request.get(url_get_case_by_enrolment, json=case)
        mock_request.get(url_get_case_categories, json=[])

        response = self.app.post('/register/validate-enrolment', headers=self.headers,
                                 data=json.dumps(self.enrolment_json))

        self.assertEqual(response.status_code, 500)
        self.assertTrue('"message": "Invalid case category"'.encode() in response.data)

    @requests_mock.mock()
    def test_validate_enrolment_post_case_fail(self, mock_request):
        mock_request.get(url_get_iac, json=self.iac_response)
        mock_request.get(url_get_case_by_enrolment, json=case)
        mock_request.get(url_get_case_categories, json=categories)
        mock_request.post(url_post_case_event, status_code=500)

        response = self.app.post('/register/validate-enrolment', headers=self.headers,
                                 data=json.dumps(self.enrolment_json))

        self.assertEqual(response.status_code, 500)
        self.assertTrue('"status_code": 500'.encode() in response.data)

    # Test posting to endpoint without basic auth in header
    def test_validate_enrolment_no_basic_auth(self):
        del self.headers['Authorization']
        response = self.app.post('/register/validate-enrolment', headers=self.headers,
                                 data=json.dumps(self.enrolment_json))

        self.assertEqual(response.status_code, 401)
