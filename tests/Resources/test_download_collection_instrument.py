import base64
import json
import unittest

import requests_mock

from frontstage_api import app


url_download_collection_instrument = app.config['RAS_CI_DOWNLOAD'].format('68ad4018-2ddd-4894-89e7-33f0135887a2')
url_get_case = app.config['RM_CASE_GET_BY_ID'].format('abc670a5-67c6-4d96-9164-13b4017b8704')
with open('tests/test_data/case/case.json') as json_data:
    case = json.load(json_data)
url_post_case_event = app.config['RM_CASE_POST_CASE_EVENT'].format('abc670a5-67c6-4d96-9164-13b4017b8704')
url_get_case_categories = app.config['RM_CASE_GET_CATEGORIES']
with open('tests/test_data/case/categories.json') as json_data:
    categories = json.load(json_data)


class TestDownloadCollectionInstrument(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.headers = {
            'Authorization': 'Basic {}'.format(base64.b64encode(
                bytes("{}:{}".format(app.config['SECURITY_USER_NAME'], app.config['SECURITY_USER_PASSWORD']),
                      'ascii')).decode("ascii"))
        }
        self.test_url = '/surveys/download-ci?case_id=abc670a5-67c6-4d96-9164-13b4017b8704&party_id=07d672bc-497b-448f-a406-a20a7e6013d7'

    @requests_mock.mock()
    def test_download_collection_instrument(self, mock_request):
        mock_request.get(url_get_case, json=case)
        mock_request.get(url_download_collection_instrument)
        mock_request.get(url_get_case_categories, json=categories)
        mock_request.post(url_post_case_event, status_code=201)

        response = self.app.get(self.test_url, headers=self.headers)

        self.assertEqual(response.status_code, 200)

    def test_download_collection_instrument_missing_args(self):
        response = self.app.get('/surveys/download-ci', headers=self.headers)

        self.assertEqual(response.status_code, 400)

    @requests_mock.mock()
    def test_download_collection_instrument_fail(self, mock_request):
        mock_request.get(url_get_case, json=case)
        mock_request.get(url_download_collection_instrument, status_code=500)
        mock_request.get(url_get_case_categories, json=categories)
        mock_request.post(url_post_case_event, status_code=201)

        response = self.app.get(self.test_url, headers=self.headers)

        self.assertEqual(response.status_code, 500)
        self.assertTrue('"status_code": 500'.encode() in response.data)

    # Test get request to endpoint without basic auth in header
    def test_get_message_no_basic_auth(self):
        del self.headers['Authorization']

        response = self.app.get(self.test_url, headers=self.headers)

        self.assertEqual(response.status_code, 401)