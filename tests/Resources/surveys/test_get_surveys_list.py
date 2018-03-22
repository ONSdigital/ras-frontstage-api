import requests_mock
import unittest

from frontstage_api import app
from tests.Resources.surveys.basic_auth_header import basic_auth_header

from tests.Resources.surveys.mocked_services import business_party, case, completed_case, \
    collection_exercise, collection_exercise_before_go_live, collection_instrument_seft, \
    survey, go_live_event, go_live_event_before, url_get_business_party, url_get_case_by_party, \
    url_get_collection_exercise, url_get_collection_exercise_go_live, url_get_survey, url_get_collection_instrument, \
    completed_by_phone_case

party_id = '07d672bc-497b-448f-a406-a20a7e6013d7'
test_surveys_list_todo = f'/surveys/surveys-list?list=todo&party_id={party_id}'


class TestGetSurveysList(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.headers = basic_auth_header()

    @requests_mock.mock()
    def test_get_surveys_list_todo(self, mock_request):
        mock_request.get(url_get_case_by_party, json=[case])
        mock_request.get(url_get_collection_exercise, json=collection_exercise)
        mock_request.get(url_get_collection_exercise_go_live, json=go_live_event)
        mock_request.get(url_get_business_party, json=business_party)
        mock_request.get(url_get_survey, json=survey)
        mock_request.get(url_get_collection_instrument, json=collection_instrument_seft)

        response = self.app.get(test_surveys_list_todo, headers=self.headers)

        self.assertEqual(response.status_code, 200)
        self.assertTrue('case'.encode() in response.data)
        self.assertTrue('collection_exercise'.encode() in response.data)
        self.assertTrue('business_party'.encode() in response.data)

    @requests_mock.mock()
    def test_get_surveys_list_todo_before_go_live(self, mock_request):
        mock_request.get(url_get_case_by_party, json=[case])
        mock_request.get(url_get_collection_exercise, json=collection_exercise_before_go_live)
        mock_request.get(url_get_collection_exercise_go_live, json=go_live_event_before)
        mock_request.get(url_get_business_party, json=business_party)
        mock_request.get(url_get_survey, json=survey)
        mock_request.get(url_get_collection_instrument, json=collection_instrument_seft)

        response = self.app.get(test_surveys_list_todo, headers=self.headers)

        self.assertEqual(response.status_code, 200)
        self.assertFalse('case'.encode() in response.data)
        self.assertFalse('collection_exercise'.encode() in response.data)
        self.assertFalse('business_party'.encode() in response.data)

    @requests_mock.mock()
    def test_get_surveys_list_history(self, mock_request):
        mock_request.get(url_get_case_by_party, json=[completed_case])
        mock_request.get(url_get_collection_exercise, json=collection_exercise)
        mock_request.get(url_get_collection_exercise_go_live, json=go_live_event)
        mock_request.get(url_get_business_party, json=business_party)
        mock_request.get(url_get_survey, json=survey)
        mock_request.get(url_get_collection_instrument, json=collection_instrument_seft)

        response = self.app.get('/surveys/surveys-list?list=history&party_id=07d672bc-497b-448f-a406-a20a7e6013d7',
                                headers=self.headers)

        self.assertEqual(response.status_code, 200)
        self.assertTrue('case'.encode() in response.data)
        self.assertTrue('collection_exercise'.encode() in response.data)
        self.assertTrue('business_party'.encode() in response.data)

    @requests_mock.mock()
    def test_get_surveys_list_history_includes_completed_by_phone(self, mock_request):
        mock_request.get(url_get_case_by_party, json=completed_by_phone_case)
        mock_request.get(url_get_collection_exercise, json=collection_exercise)
        mock_request.get(url_get_collection_exercise_go_live, json=go_live_event)
        mock_request.get(url_get_business_party, json=business_party)
        mock_request.get(url_get_survey, json=survey)
        mock_request.get(url_get_collection_instrument, json=collection_instrument_seft)

        response = self.app.get('/surveys/surveys-list?list=history&party_id=07d672bc-497b-448f-a406-a20a7e6013d7',
                                headers=self.headers)

        self.assertEqual(response.status_code, 200)
        self.assertIn('Completed by phone'.encode(), response.data)

    def test_get_surveys_list_todo_missing_args(self):
        response = self.app.get('/surveys/surveys-list?list=todo', headers=self.headers)

        self.assertEqual(response.status_code, 400)

    @requests_mock.mock()
    def test_get_surveys_list_invalid_surveys_list(self, mock_request):
        mock_request.get(url_get_case_by_party, json=case)

        response = self.app.get('/surveys/surveys-list?list=wronglist&party_id=07d672bc-497b-448f-a406-a20a7e6013d7', headers=self.headers)

        self.assertEqual(response.status_code, 400)
        self.assertTrue('"message": "Invalid survey list name"'.encode() in response.data)

    @requests_mock.mock()
    def test_get_surveys_list_todo_case_fail(self, mock_request):
        mock_request.get(url_get_case_by_party, status_code=500)

        response = self.app.get(test_surveys_list_todo, headers=self.headers)

        self.assertEqual(response.status_code, 500)
        self.assertTrue('"status_code": 500'.encode() in response.data)

    @requests_mock.mock()
    def test_get_surveys_list_todo_collection_exercise_fail(self, mock_request):
        mock_request.get(url_get_case_by_party, json=[case])
        mock_request.get(url_get_collection_exercise, status_code=500)

        response = self.app.get(test_surveys_list_todo, headers=self.headers)

        self.assertEqual(response.status_code, 500)
        self.assertTrue('"status_code": 500'.encode() in response.data)

    @requests_mock.mock()
    def test_get_surveys_list_todo_collection_exercise_event_fail(self, mock_request):
        mock_request.get(url_get_case_by_party, json=[case])
        mock_request.get(url_get_collection_exercise, json=collection_exercise)
        mock_request.get(url_get_collection_exercise_go_live, status_code=500)

        response = self.app.get(test_surveys_list_todo, headers=self.headers)

        self.assertEqual(response.status_code, 500)
        self.assertTrue('"status_code": 500'.encode() in response.data)

    @requests_mock.mock()
    def test_get_surveys_list_todo_party_fail(self, mock_request):
        mock_request.get(url_get_case_by_party, json=[case])
        mock_request.get(url_get_collection_exercise, json=collection_exercise)
        mock_request.get(url_get_collection_exercise_go_live, json=go_live_event)
        mock_request.get(url_get_business_party, status_code=500)

        response = self.app.get(test_surveys_list_todo, headers=self.headers)

        self.assertEqual(response.status_code, 500)
        self.assertTrue('"status_code": 500'.encode() in response.data)

    @requests_mock.mock()
    def test_get_surveys_list_todo_survey_fail(self, mock_request):
        mock_request.get(url_get_case_by_party, json=[case])
        mock_request.get(url_get_collection_exercise, json=collection_exercise)
        mock_request.get(url_get_collection_exercise_go_live, json=go_live_event)
        mock_request.get(url_get_business_party, json=business_party)
        mock_request.get(url_get_survey, status_code=500)

        response = self.app.get(test_surveys_list_todo, headers=self.headers)

        self.assertEqual(response.status_code, 500)
        self.assertTrue('"status_code": 500'.encode() in response.data)

    @requests_mock.mock()
    def test_get_surveys_list_todo_collection_instrument_fail(self, mock_request):
        mock_request.get(url_get_case_by_party, json=[case])
        mock_request.get(url_get_collection_exercise, json=collection_exercise)
        mock_request.get(url_get_collection_exercise_go_live, json=go_live_event)
        mock_request.get(url_get_business_party, json=business_party)
        mock_request.get(url_get_survey, json=survey)
        mock_request.get(url_get_collection_instrument, status_code=500)

        response = self.app.get(test_surveys_list_todo, headers=self.headers)

        self.assertEqual(response.status_code, 500)
        self.assertTrue('"status_code": 500'.encode() in response.data)

    # Test get request to endpoint without basic auth in header
    def test_get_message_no_basic_auth(self):
        del self.headers['Authorization']

        response = self.app.get(test_surveys_list_todo, headers=self.headers)

        self.assertEqual(response.status_code, 401)
