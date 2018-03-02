import requests_mock
import unittest

from frontstage_api import app
from tests.Resources.surveys.basic_auth_header import basic_auth_header
from tests.Resources.surveys.mocked_services import business_party, case, collection_exercise, \
     collection_instrument_seft, go_live_event, survey, url_get_business_party, \
     url_get_case, url_get_collection_exercise, url_get_collection_exercise_go_live, url_get_collection_instrument, \
     url_get_survey


case_id = 'abc670a5-67c6-4d96-9164-13b4017b8704'
party_id = '07d672bc-497b-448f-a406-a20a7e6013d7'
test_access_case_url = '/surveys/access-case?case_id={}&party_id={}'.format(case_id, party_id)


class TestAccessCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.headers = basic_auth_header()

    @requests_mock.mock()
    def test_access_case(self, mock_request):
        mock_request.get(url_get_case, json=case)
        mock_request.get(url_get_collection_exercise, json=collection_exercise)
        mock_request.get(url_get_collection_exercise_go_live, json=go_live_event)
        mock_request.get(url_get_business_party, json=business_party)
        mock_request.get(url_get_survey, json=survey)
        mock_request.get(url_get_collection_instrument, json=collection_instrument_seft)

        response = self.app.get(test_access_case_url, headers=self.headers)

        self.assertEqual(response.status_code, 200)
        self.assertTrue('case'.encode() in response.data)
        self.assertTrue('"collection_instrument_size": 5'.encode() in response.data)

    def test_access_case_missing_args(self):
        response = self.app.get('/surveys/access-case', headers=self.headers)

        self.assertEqual(response.status_code, 400)

    @requests_mock.mock()
    def test_access_case_no_permission(self, mock_request):
        mock_request.get(url_get_case, json=case)

        test_url = '/surveys/access-case?case_id=abc670a5-67c6-4d96-9164-13b4017b8704&party_id=wrong'
        response = self.app.get(test_url, headers=self.headers)

        self.assertEqual(response.status_code, 403)
        self.assertTrue('"message": "Party does not have permission to access case"'.encode() in response.data)

    @requests_mock.mock()
    def test_access_case_fail(self, mock_request):
        mock_request.get(url_get_case, status_code=500)

        response = self.app.get(test_access_case_url, headers=self.headers)

        self.assertEqual(response.status_code, 500)
        self.assertTrue('"status_code": 500'.encode() in response.data)

    # Test get request to endpoint without basic auth in header
    def test_access_case_no_basic_auth(self):
        del self.headers['Authorization']

        response = self.app.get(test_access_case_url, headers=self.headers)

        self.assertEqual(response.status_code, 401)
