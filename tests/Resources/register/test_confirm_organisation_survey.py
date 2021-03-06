import base64
import json
import unittest

import requests_mock

from frontstage_api import app


url_get_iac = f"{app.config['RM_IAC_SERVICE']}/iacs/test_enrolment"
url_get_case_by_enrolment = f"{app.config['RM_CASE_SERVICE']}/cases/iac/test_enrolment"
with open('tests/test_data/case/case.json') as json_data:
    case = json.load(json_data)
with open('tests/test_data/case/categories.json') as json_data:
    categories = json.load(json_data)
url_get_business_party = f"{app.config['RAS_PARTY_SERVICE']}/party-api/v1/businesses/id/1216a88f-ee2a-420c-9e6a-ee34893c29cf"
with open('tests/test_data/party/business_party.json') as json_data:
    business_party = json.load(json_data)
url_get_collection_exercise = f"{app.config['RM_COLLECTION_EXERCISE_SERVICE']}/collectionexercises/14fb3e68-4dca-46db-bf49-04b84e07e77c"
with open('tests/test_data/collection_exercise/collection_exercise.json') as json_data:
    collection_exercise = json.load(json_data)
url_get_survey = f"{app.config['RM_SURVEY_SERVICE']}/surveys/test_survey_id"
with open('tests/test_data/survey/survey.json') as json_data:
    survey = json.load(json_data)


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

    @requests_mock.mock()
    def test_confirm_organisation_survey(self, mock_request):
        mock_request.get(url_get_iac, json=self.iac_response)
        mock_request.get(url_get_case_by_enrolment, json=case)
        mock_request.get(url_get_business_party, json=business_party)
        mock_request.get(url_get_collection_exercise, json=collection_exercise)
        mock_request.get(url_get_survey, json=survey)

        response = self.app.post('/register/confirm-organisation-survey', headers=self.headers,
                                 data=json.dumps({'enrolment_code': 'test_enrolment'}))

        self.assertEqual(response.status_code, 200)
        self.assertTrue('"organisation_name": "Bolts and Ratchets Ltd"'.encode() in response.data)
        self.assertTrue('"survey_name": "Business Register and Employment Survey"'.encode() in response.data)

    @requests_mock.mock()
    def test_confirm_organisation_survey_iac_fail(self, mock_request):
        mock_request.get(url_get_iac, status_code=500)

        response = self.app.post('/register/confirm-organisation-survey', headers=self.headers,
                                 data=json.dumps({'enrolment_code': 'test_enrolment'}))

        self.assertEqual(response.status_code, 500)
        self.assertTrue('"status_code": 500'.encode() in response.data)

    @requests_mock.mock()
    def test_confirm_organisation_survey_iac_inactive(self, mock_request):
        self.iac_response['active'] = False
        mock_request.get(url_get_iac, json=self.iac_response)

        response = self.app.post('/register/confirm-organisation-survey', headers=self.headers,
                                 data=json.dumps({'enrolment_code': 'test_enrolment'}))

        self.assertEqual(response.status_code, 401)
        self.assertTrue('"active": false'.encode() in response.data)

    @requests_mock.mock()
    def test_confirm_organisation_survey_business_party_fail(self, mock_request):
        mock_request.get(url_get_iac, json=self.iac_response)
        mock_request.get(url_get_case_by_enrolment, json=case)
        mock_request.get(url_get_business_party, status_code=500)

        response = self.app.post('/register/confirm-organisation-survey', headers=self.headers,
                                 data=json.dumps({'enrolment_code': 'test_enrolment'}))

        self.assertEqual(response.status_code, 500)
        self.assertTrue('"status_code": 500'.encode() in response.data)

    @requests_mock.mock()
    def test_confirm_organisation_survey_collection_exercise_fail(self, mock_request):
        mock_request.get(url_get_iac, json=self.iac_response)
        mock_request.get(url_get_case_by_enrolment, json=case)
        mock_request.get(url_get_business_party, json=business_party)
        mock_request.get(url_get_collection_exercise, status_code=500)

        response = self.app.post('/register/confirm-organisation-survey', headers=self.headers,
                                 data=json.dumps({'enrolment_code': 'test_enrolment'}))

        self.assertEqual(response.status_code, 500)
        self.assertTrue('"status_code": 500'.encode() in response.data)

    @requests_mock.mock()
    def test_confirm_organisation_survey_survey_fail(self, mock_request):
        mock_request.get(url_get_iac, json=self.iac_response)
        mock_request.get(url_get_case_by_enrolment, json=case)
        mock_request.get(url_get_business_party, json=business_party)
        mock_request.get(url_get_collection_exercise, json=collection_exercise)
        mock_request.get(url_get_survey, status_code=500)

        response = self.app.post('/register/confirm-organisation-survey', headers=self.headers,
                                 data=json.dumps({'enrolment_code': 'test_enrolment'}))

        self.assertEqual(response.status_code, 500)
        self.assertTrue('"status_code": 500'.encode() in response.data)

    # Test posting to endpoint without basic auth in header
    def test_confirm_organisation_survey_no_basic_auth(self):
        del self.headers['Authorization']
        response = self.app.post('/register/confirm-organisation-survey', headers=self.headers,
                                 data=json.dumps({'enrolment_code': 'test_enrolment'}))

        self.assertEqual(response.status_code, 401)
