import unittest

from requests.exceptions import ConnectionError, ConnectTimeout
import requests_mock

from frontstage_api.common.utilities import request_handler
from frontstage_api.exceptions.exceptions import FailedRequest


url = 'http://testurl'


class TestSecureMessaging(unittest.TestCase):

    @requests_mock.mock()
    def test_get_response(self, mock_request):
        mock_request.get(url)

        response = request_handler('GET', url)

        self.assertEqual(response.status_code, 200)

    @requests_mock.mock()
    def test_post_response(self, mock_request):
        mock_request.post(url)

        response = request_handler('POST', url)

        self.assertEqual(response.status_code, 200)

    @requests_mock.mock()
    def test_put_response(self, mock_request):
        mock_request.put(url)

        response = request_handler('PUT', url)

        self.assertEqual(response.status_code, 200)

    @requests_mock.mock()
    def test_get_response_connection_error(self, mock_request):
        mock_request.get(url, exc=ConnectionError)

        with self.assertRaises(FailedRequest):
            request_handler('GET', url)

    @requests_mock.mock()
    def test_get_response_connection_timeout(self, mock_request):
        mock_request.get(url, exc=ConnectTimeout)

        with self.assertRaises(FailedRequest):
            request_handler('GET', url)
