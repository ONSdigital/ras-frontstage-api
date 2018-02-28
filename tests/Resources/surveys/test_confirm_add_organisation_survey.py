import base64
import json
import requests_mock
import unittest

from frontstage_api import app
from tests.Resources.surveys.mocked_services import business_party, case, collection_exercise, \
     survey, url_get_business_party, url_get_case_by_enrolment, url_get_collection_exercise, \
     url_get_iac, url_get_survey


class TestAddSurvey(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Basic {}'.format(base64.b64encode(
                bytes("{}:{}".format(app.config['SECURITY_USER_NAME'], app.config['SECURITY_USER_PASSWORD']), 'ascii')
            ).decode("ascii"))
        }
        self.iac_response = {
            "iac": "test_enrolment",
            "active": True,
            "used": False,
            "lastUsedDateTime": "2017-05-15T10:00:00Z",
            "caseId": "test_case_id",
            "questionSet": "H1"
        }

    @requests_mock.mock()
    def test_confirm_add_organisation_survey(self, mock_request):
        mock_request.get(url_get_iac, json=self.iac_response)
        mock_request.get(url_get_case_by_enrolment, json=case)
        mock_request.get(url_get_business_party, json=business_party)
        mock_request.get(url_get_collection_exercise, json=collection_exercise)
        mock_request.get(url_get_survey, json=survey)

        response = self.app.post('/surveys/add-survey/confirm-add-organisation-survey', headers=self.headers,
                                 data=json.dumps({'enrolment_code': 'test_enrolment'}))

        self.assertEqual(response.status_code, 200)
        self.assertTrue('"organisation_name": "Bolts and Ratchets Ltd"'.encode() in response.data)
        self.assertTrue('"survey_name": "Business Register and Employment Survey"'.encode() in response.data)

    @requests_mock.mock()
    def test_confirm_add_organisation_survey_iac_fail(self, mock_request):
        mock_request.get(url_get_iac, status_code=500)

        response = self.app.post('/surveys/add-survey/confirm-add-organisation-survey', headers=self.headers,
                                 data=json.dumps({'enrolment_code': 'test_enrolment'}))

        self.assertEqual(response.status_code, 500)
        self.assertTrue('"status_code": 500'.encode() in response.data)

    @requests_mock.mock()
    def test_confirm_add_organisation_survey_iac_inactive(self, mock_request):
        self.iac_response['active'] = False
        mock_request.get(url_get_iac, json=self.iac_response)

        response = self.app.post('/surveys/add-survey/confirm-add-organisation-survey', headers=self.headers,
                                 data=json.dumps({'enrolment_code': 'test_enrolment'}))

        self.assertEqual(response.status_code, 401)
        self.assertTrue('"active": false'.encode() in response.data)

    @requests_mock.mock()
    def test_confirm_add_organisation_survey_business_party_fail(self, mock_request):
        mock_request.get(url_get_iac, json=self.iac_response)
        mock_request.get(url_get_case_by_enrolment, json=case)
        mock_request.get(url_get_business_party, status_code=500)

        response = self.app.post('/surveys/add-survey/confirm-add-organisation-survey', headers=self.headers,
                                 data=json.dumps({'enrolment_code': 'test_enrolment'}))

        self.assertEqual(response.status_code, 500)
        self.assertTrue('"status_code": 500'.encode() in response.data)

    @requests_mock.mock()
    def test_confirm_add_organisation_survey_collection_exercise_fail(self, mock_request):
        mock_request.get(url_get_iac, json=self.iac_response)
        mock_request.get(url_get_case_by_enrolment, json=case)
        mock_request.get(url_get_business_party, json=business_party)
        mock_request.get(url_get_collection_exercise, status_code=500)

        response = self.app.post('/surveys/add-survey/confirm-add-organisation-survey', headers=self.headers,
                                 data=json.dumps({'enrolment_code': 'test_enrolment'}))

        self.assertEqual(response.status_code, 500)
        self.assertTrue('"status_code": 500'.encode() in response.data)

    @requests_mock.mock()
    def test_confirm_add_organisation_survey_survey_fail(self, mock_request):
        mock_request.get(url_get_iac, json=self.iac_response)
        mock_request.get(url_get_case_by_enrolment, json=case)
        mock_request.get(url_get_business_party, json=business_party)
        mock_request.get(url_get_collection_exercise, json=collection_exercise)
        mock_request.get(url_get_survey, status_code=500)

        response = self.app.post('/surveys/add-survey/confirm-add-organisation-survey', headers=self.headers,
                                 data=json.dumps({'enrolment_code': 'test_enrolment'}))

        self.assertEqual(response.status_code, 500)
        self.assertTrue('"status_code": 500'.encode() in response.data)

    # Test posting to endpoint without basic auth in header
    def test_confirm_add_organisation_survey_no_basic_auth(self):
        del self.headers['Authorization']
        response = self.app.post('surveys/add-survey/confirm-add-organisation-survey', headers=self.headers,
                                 data=json.dumps({'enrolment_code': 'test_enrolment'}))

        self.assertEqual(response.status_code, 401)
