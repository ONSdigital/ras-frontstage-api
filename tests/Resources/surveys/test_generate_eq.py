import json
import requests_mock
import unittest

from frontstage_api import app
from frontstage_api.controllers import collection_exercise_controller
from frontstage_api.controllers.eq_payload import EqPayload
from frontstage_api.exceptions.exceptions import ApiError, InvalidEqPayLoad

from tests.Resources.surveys.mocked_services import case, collection_exercise, collection_exercise_events, \
     business_party, survey, collection_instrument_eq,url_get_case, url_get_collection_exercise, \
     url_get_collection_exercise_events, url_get_business_party, url_get_survey, url_get_collection_instrument, \
     collection_instrument_seft
from tests.Resources.surveys.basic_auth_header import basic_auth_header


party_id = '07d672bc-497b-448f-a406-a20a7e6013d7'
case_id = 'abc670a5-67c6-4d96-9164-13b4017b8704'
test_generate_eq_url = '/surveys/generate-eq-url?party_id={}&case_id={}'.format(party_id,case_id)


class TestGenerateEqURL(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.headers = basic_auth_header()

    @requests_mock.mock()
    def test_generate_eq_url(self, mock_request):

        # Given all external services are mocked and we have an EQ collection instrument
        mock_request.get(url_get_case, json=case)
        mock_request.get(url_get_collection_exercise, json=collection_exercise)
        mock_request.get(url_get_collection_exercise_events, json=collection_exercise_events)
        mock_request.get(url_get_business_party, json=business_party)
        mock_request.get(url_get_survey, json=survey)
        mock_request.get(url_get_collection_instrument, json=collection_instrument_eq)

        # When the generate-eq-url is called
        response = self.app.get(test_generate_eq_url, headers=self.headers)

        # A dict with the eq_url is returned
        self.assertEqual(response.status_code, 200)
        self.assertIn("eq_url", json.loads(response.data))

    @requests_mock.mock()
    def test_generate_eq_url_seft(self, mock_request):

        # Given all external services are mocked and we have seft collection instrument
        mock_request.get(url_get_collection_exercise, json=collection_exercise)
        mock_request.get(url_get_collection_exercise_events, json=collection_exercise_events)
        mock_request.get(url_get_business_party, json=business_party)
        mock_request.get(url_get_survey, json=survey)
        mock_request.get(url_get_collection_instrument, json=collection_instrument_seft)


        # When create_payload is called
        # Then an InvalidEqPayLoad is raised
        with self.assertRaises(InvalidEqPayLoad) as e:
            EqPayload().create_payload(case)
        self.assertEqual(e.exception.error, 'Collection instrument 68ad4018-2ddd-4894-89e7-33f0135887a2 type is not EQ')

    @requests_mock.mock()
    def test_generate_eq_url_no_eq_id(self, mock_request):

        # Given all external services are mocked and we have an EQ collection instrument without an EQ ID
        with open('tests/test_data/collection_instrument/collection_instrument_eq_no_eq_id.json') as json_data:
            collection_instrument_eq_no_eq_id = json.load(json_data)

        mock_request.get(url_get_collection_instrument, json=collection_instrument_eq_no_eq_id)

        # When create_payload is called
        # Then an InvalidEqPayLoad is raised
        with self.assertRaises(InvalidEqPayLoad) as e:
            EqPayload().create_payload(case)
        self.assertEqual(e.exception.error, 'Collection instrument 68ad4018-2ddd-4894-89e7-33f0135887a2 '
                                            'classifiers are incorrect or missing')

    @requests_mock.mock()
    def test_generate_eq_url_no_form_type(self, mock_request):

        # Given all external services are mocked and we have an EQ collection instrument without a Form_type
        with open('tests/test_data/collection_instrument/collection_instrument_eq_no_form_type.json') as json_data:
            collection_instrument_eq_no_form_type = json.load(json_data)

        mock_request.get(url_get_collection_instrument, json=collection_instrument_eq_no_form_type)

        # When create_payload is called
        # Then an InvalidEqPayLoad is raised
        with self.assertRaises(InvalidEqPayLoad) as e:
            EqPayload().create_payload(case)
        self.assertEqual(e.exception.error, 'Collection instrument 68ad4018-2ddd-4894-89e7-33f0135887a2 '
                                            'classifiers are incorrect or missing')

    @requests_mock.mock()
    def test_access_collection_exercise_events_fail(self, mock_request):

        # Given a failing collection exercise events service
        mock_request.get(url_get_collection_exercise_events, status_code=500)
        collection_exercise_id = '14fb3e68-4dca-46db-bf49-04b84e07e77c'

        # When get collection exercise events is called
        # Then an ApiError is raised
        with self.assertRaises(ApiError):
            collection_exercise_controller.get_collection_exercise_events(collection_exercise_id)

    def test_generate_eq_url_incorrect_date_format(self):

        # Given an invalid date
        date = 'invalid'

        # When format_string_long_date_time_to_short_date is called
        # Then an InvalidEqPayLoad is raised
        with self.assertRaises(InvalidEqPayLoad) as e:
            EqPayload()._format_string_long_date_time_to_short_date(date)
        self.assertEqual(e.exception.error, 'Unable to format invalid, expected format %Y-%m-%dT%H:%M:%S.%fZ')

    def test_generate_eq_url_missing_event_date(self):

        # Given no event dates
        collex_events_dates = []
        # When find_event_date_by_tag is called with a search param
        # Then an InvalidEqPayLoad is raised

        with self.assertRaises(InvalidEqPayLoad) as e:
            EqPayload()._find_event_date_by_tag('return by', collex_events_dates, '123')
        self.assertEqual(e.exception.error, 'Event not found for collection 123 for search param return by')
