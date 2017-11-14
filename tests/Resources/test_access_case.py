import base64
import json
import unittest

import requests_mock

from frontstage_api import app


url_get_case = app.config['RM_CASE_GET_BY_ID'].format('abc670a5-67c6-4d96-9164-13b4017b8704')
with open('tests/test_data/case/case.json') as json_data:
    case = json.load(json_data)
with open('tests/test_data/case/completed_case.json') as json_data:
    completed_case = [json.load(json_data)]
url_get_collection_exercise = app.config['RM_COLLECTION_EXERCISE_GET'].format('14fb3e68-4dca-46db-bf49-04b84e07e77c')
with open('tests/test_data/collection_exercise/collection_exercise.json') as json_data:
    collection_exercise = json.load(json_data)
url_get_business_party = app.config['RAS_PARTY_GET_BY_BUSINESS_ID'].format('1216a88f-ee2a-420c-9e6a-ee34893c29cf')
with open('tests/test_data/party/business_party.json') as json_data:
    business_party = json.load(json_data)
url_get_survey = app.config['RM_SURVEY_GET'].format('test_survey_id')
with open('tests/test_data/survey/survey.json') as json_data:
    survey = json.load(json_data)
url_get_collection_instrument_size = app.config['RAS_CI_SIZE'].format('68ad4018-2ddd-4894-89e7-33f0135887a2')


class TestAccessCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.headers = {
            'Authorization': 'Basic {}'.format(base64.b64encode(
                bytes("{}:{}".format(app.config['SECURITY_USER_NAME'], app.config['SECURITY_USER_PASSWORD']),
                      'ascii')).decode("ascii"))
        }
        self.test_url = '/access-case?case_id=abc670a5-67c6-4d96-9164-13b4017b8704&party_id=07d672bc-497b-448f-a406-a20a7e6013d7'

    @requests_mock.mock()
    def test_access_case(self, mock_request):
        mock_request.get(url_get_case, json=case)
        mock_request.get(url_get_collection_exercise, json=collection_exercise)
        mock_request.get(url_get_business_party, json=business_party)
        mock_request.get(url_get_survey, json=survey)
        mock_request.get(url_get_collection_instrument_size, json={'size': 5})

        response = self.app.get(self.test_url, headers=self.headers)

        self.assertEqual(response.status_code, 200)
        self.assertTrue('case'.encode() in response.data)
        self.assertTrue('"collection_instrument_size": 5'.encode() in response.data)

    @requests_mock.mock()
    def test_access_case_no_permission(self, mock_request):
        mock_request.get(url_get_case, json=case)

        test_url = '/access-case?case_id=abc670a5-67c6-4d96-9164-13b4017b8704&party_id=wrong'
        response = self.app.get(test_url, headers=self.headers)

        self.assertEqual(response.status_code, 403)
        self.assertTrue('"message": "Party does not have permission to access case"'.encode() in response.data)

    @requests_mock.mock()
    def test_access_case_fail(self, mock_request):
        mock_request.get(url_get_case, status_code=500)

        response = self.app.get(self.test_url, headers=self.headers)

        self.assertEqual(response.status_code, 500)
        self.assertTrue('"status_code": 500'.encode() in response.data)
