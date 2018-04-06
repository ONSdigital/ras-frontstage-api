import requests_mock
import unittest

from frontstage_api import app
from tests.Resources.surveys.mocked_services import case, categories, url_download_ci, \
     url_get_case, url_get_case_categories, url_post_case_event_uuid
from tests.Resources.surveys.basic_auth_header import basic_auth_header

case_id = 'abc670a5-67c6-4d96-9164-13b4017b8704'
party_id = '07d672bc-497b-448f-a406-a20a7e6013d7'
test_download_ci = f'/surveys/download-ci?case_id={case_id}&party_id={party_id}'


class TestDownloadCollectionInstrument(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.headers = basic_auth_header()

    @requests_mock.mock()
    def test_download_collection_instrument(self, mock_request):
        mock_request.get(url_get_case, json=case)
        mock_request.get(url_download_ci)
        mock_request.get(url_get_case_categories, json=categories)
        mock_request.post(url_post_case_event_uuid, status_code=201)

        response = self.app.get(test_download_ci, headers=self.headers)

        self.assertEqual(response.status_code, 200)

    def test_download_collection_instrument_missing_args(self):
        response = self.app.get('/surveys/download-ci', headers=self.headers)

        self.assertEqual(response.status_code, 400)

    @requests_mock.mock()
    def test_download_collection_instrument_fail(self, mock_request):
        mock_request.get(url_get_case, json=case)
        mock_request.get(url_download_ci, status_code=500)
        mock_request.get(url_get_case_categories, json=categories)
        mock_request.post(url_post_case_event_uuid, status_code=201)

        response = self.app.get(test_download_ci, headers=self.headers)

        self.assertEqual(response.status_code, 500)
        self.assertTrue('"status_code": 500'.encode() in response.data)

    # Test get request to endpoint without basic auth in header
    def test_get_message_no_basic_auth(self):
        del self.headers['Authorization']

        response = self.app.get(test_download_ci, headers=self.headers)

        self.assertEqual(response.status_code, 401)
