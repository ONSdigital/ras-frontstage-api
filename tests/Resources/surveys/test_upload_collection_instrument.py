import io
import unittest

import requests_mock

from frontstage_api import app

from tests.Resources.surveys.mocked_services import case, categories, url_get_case, url_get_case_categories, \
    url_upload_collection_instrument, url_post_case_event_uuid
from tests.Resources.surveys.basic_auth_header import basic_auth_header

case_id = 'abc670a5-67c6-4d96-9164-13b4017b8704'
party_id = '07d672bc-497b-448f-a406-a20a7e6013d7'
test_upload_ci_url = f'/surveys/upload-ci?case_id={case_id}&party_id={party_id}'


class TestUploadCollectionInstrument(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.headers = basic_auth_header()
        self.ci_data = dict(file=(io.BytesIO(b'my file contents'), "testfile.xlsx"))

    @requests_mock.mock()
    def test_upload_collection_instrument(self, mock_request):
        mock_request.get(url_get_case, json=case)
        mock_request.post(url_upload_collection_instrument)
        mock_request.get(url_get_case_categories, json=categories)
        mock_request.post(url_post_case_event_uuid, status_code=201)

        response = self.app.post(test_upload_ci_url, headers=self.headers, data=self.ci_data)

        self.assertEqual(response.status_code, 200)

    def test_upload_collection_instrument_missing_args(self):
        response = self.app.post(f'/surveys/upload-ci?case_id={case_id}',
                                 headers=self.headers, data=self.ci_data)

        self.assertEqual(response.status_code, 400)

    @requests_mock.mock()
    def test_upload_collection_instrument_missing_file(self, mock_request):
        mock_request.get(url_get_case, json=case)

        response = self.app.post(test_upload_ci_url, headers=self.headers)

        self.assertEqual(response.status_code, 400)

    def test_upload_collection_instrument_file_too_large(self):
        file_data = 'a' * 21 * 1024 * 1024
        over_size_file = dict(file=(io.BytesIO(file_data.encode()), "testfile.xlsx"))

        response = self.app.post(test_upload_ci_url, headers=self.headers, data=over_size_file)

        self.assertEqual(response.status_code, 400)
        self.assertTrue('"message": "File too large"'.encode() in response.data)

    @requests_mock.mock()
    def test_upload_collection_instrument_400(self, mock_request):
        mock_request.get(url_get_case, json=case)
        mock_request.post(url_upload_collection_instrument, status_code=400, text="FAILED")
        mock_request.get(url_get_case_categories, json=categories)
        mock_request.post(url_post_case_event_uuid, status_code=201)

        response = self.app.post(test_upload_ci_url, headers=self.headers, data=self.ci_data)

        self.assertEqual(response.status_code, 400)
        self.assertIn('"message": "FAILED"'.encode(), response.data)

    @requests_mock.mock()
    def test_upload_collection_instrument_fail(self, mock_request):
        mock_request.get(url_get_case, json=case)
        mock_request.post(url_upload_collection_instrument, status_code=500)
        mock_request.get(url_get_case_categories, json=categories)
        mock_request.post(url_post_case_event_uuid, status_code=201)

        response = self.app.post(test_upload_ci_url, headers=self.headers, data=self.ci_data)

        self.assertEqual(response.status_code, 500)
        self.assertTrue('"status_code": 500'.encode() in response.data)

    # Test get request to endpoint without basic auth in header
    def test_get_message_no_basic_auth(self):
        del self.headers['Authorization']

        response = self.app.post(test_upload_ci_url, headers=self.headers, data=self.ci_data)

        self.assertEqual(response.status_code, 401)
