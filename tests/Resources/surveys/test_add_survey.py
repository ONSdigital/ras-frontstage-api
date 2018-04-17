import base64
import json
import requests_mock
import unittest

from frontstage_api import app
from tests.Resources.surveys.mocked_services import case, case_list, categories, \
    url_get_case_by_enrolment, url_get_case_by_party, url_get_case_categories, \
    url_get_case_by_party_no_events, url_get_iac, url_post_case_event, url_post_add_survey


class TestAddSurvey(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        auth_string = base64.b64encode(
            bytes(f"{app.config['SECURITY_USER_NAME']}:{app.config['SECURITY_USER_PASSWORD']}", 'ascii')
        ).decode("ascii")
        self.headers = {
            'Authorization': f'Basic {auth_string}',
            'Content-Type': 'application/json',
        }
        self.enrolment_json = {
            'enrolment_code': 'test_enrolment',
            'party_id': 'test_party'
        }
        self.iac_response = {
            "iac": "test_enrolment",
            "active": True,
            "lastUsedDateTime": "2017-05-15T10:00:00Z",
            "caseId": "test_case_id",
            "questionSet": "H1"
        }

    @requests_mock.mock()
    def test_add_survey_success(self, mock_request):
        mock_request.get(url_get_iac, json=self.iac_response)
        mock_request.get(url_get_case_by_enrolment, json=case)
        mock_request.get(url_get_case_by_party, json=case)
        mock_request.get(url_get_case_categories, json=categories)
        mock_request.post(url_post_case_event, status_code=201)
        mock_request.post(url_post_add_survey, status_code=200)
        mock_request.get(url_get_case_by_party_no_events, json=case_list)

        response = self.app.post('/surveys/add-survey', headers=self.headers,
                                 data=json.dumps(self.enrolment_json))

        self.assertEqual(response.status_code, 200)
        self.assertTrue('"case_id": "abc670a5-67c6-4d96-9164-13b4017b8704"'.encode() in response.data)

    @requests_mock.mock()
    def test_add_survey_failure(self, mock_request):
        mock_request.get(url_get_iac, json=self.iac_response)
        mock_request.get(url_get_case_by_enrolment, json=case)
        mock_request.get(url_get_case_by_party, json=case)
        mock_request.get(url_get_case_categories, json=categories)
        mock_request.post(url_post_case_event, status_code=201)
        mock_request.post(url_post_add_survey, status_code=500)
        mock_request.get(url_get_case_by_party_no_events, json=case_list)

        response = self.app.post('/surveys/add-survey', headers=self.headers,
                                 data=json.dumps(self.enrolment_json))

        self.assertEqual(response.status_code, 500)
        self.assertTrue('"status_code": 500'.encode() in response.data)

    @requests_mock.mock()
    def test_add_survey_iac_inactive(self, mock_request):
        self.iac_response['active'] = False
        mock_request.get(url_get_iac, json=self.iac_response)
        response = self.app.post('/surveys/add-survey', headers=self.headers,
                                 data=json.dumps(self.enrolment_json))
        self.assertEqual(response.status_code, 401)
        self.assertTrue('"active": false'.encode() in response.data)

    @requests_mock.mock()
    def test_add_survey_iac_fail(self, mock_request):
        mock_request.get(url_get_iac, status_code=500)

        response = self.app.post('/surveys/add-survey', headers=self.headers,
                                 data=json.dumps(self.enrolment_json))

        self.assertEqual(response.status_code, 500)
        self.assertTrue('"status_code": 500'.encode() in response.data)

    @requests_mock.mock()
    def test_add_survey_iac_404(self, mock_request):
        mock_request.get(url_get_iac, status_code=404)

        response = self.app.post('/surveys/add-survey', headers=self.headers,
                                 data=json.dumps(self.enrolment_json))

        self.assertEqual(response.status_code, 404)
        self.assertTrue('"status_code": 404'.encode() in response.data)

    @requests_mock.mock()
    def test_add_survey_case_get_fail(self, mock_request):
        mock_request.get(url_get_iac, json=self.iac_response)
        mock_request.get(url_get_case_by_enrolment, status_code=500)

        response = self.app.post('/surveys/add-survey', headers=self.headers,
                                 data=json.dumps(self.enrolment_json))

        self.assertEqual(response.status_code, 500)
        self.assertTrue('"status_code": 500'.encode() in response.data)

    @requests_mock.mock()
    def test_add_survey_get_categories_fail(self, mock_request):
        mock_request.get(url_get_iac, json=self.iac_response)
        mock_request.get(url_get_case_by_enrolment, json=case)
        mock_request.get(url_get_case_categories, status_code=500)

        response = self.app.post('/surveys/add-survey', headers=self.headers,
                                 data=json.dumps(self.enrolment_json))

        self.assertEqual(response.status_code, 500)
        self.assertTrue('"status_code": 500'.encode() in response.data)

    @requests_mock.mock()
    def test_add_survey_invalid_case_category(self, mock_request):
        mock_request.get(url_get_iac, json=self.iac_response)
        mock_request.get(url_get_case_by_enrolment, json=case)
        mock_request.get(url_get_case_categories, json=[])

        response = self.app.post('/surveys/add-survey', headers=self.headers,
                                 data=json.dumps(self.enrolment_json))

        self.assertEqual(response.status_code, 500)
        self.assertTrue('"message": "Invalid case category"'.encode() in response.data)

    @requests_mock.mock()
    def test_add_survey_post_case_fail(self, mock_request):
        mock_request.get(url_get_iac, json=self.iac_response)
        mock_request.get(url_get_case_by_enrolment, json=case)
        mock_request.get(url_get_case_categories, json=categories)
        mock_request.post(url_post_case_event, status_code=500)

        response = self.app.post('/surveys/add-survey', headers=self.headers,
                                 data=json.dumps(self.enrolment_json))

        self.assertEqual(response.status_code, 500)
        self.assertTrue('"status_code": 500'.encode() in response.data)

    # Test posting to endpoint without basic auth in header
    def test_add_survey_no_basic_auth(self):
        del self.headers['Authorization']
        response = self.app.post('/surveys/add-survey', headers=self.headers,
                                 data=json.dumps(self.enrolment_json))

        self.assertEqual(response.status_code, 401)
