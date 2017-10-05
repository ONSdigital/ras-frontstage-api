import json
import unittest

import requests
import requests_mock

from frontstage_api import app
from frontstage_api.exceptions.exceptions import FailedRequest, InvalidRequestMethod


url_get_messages_list_INBOX = '{}&label={}'.format(app.config['MESSAGES_LIST_URL'], 'INBOX')
with open('tests/test_data/secure_messaging/messages_list_inbox.json') as json_data:
    messages_list_inbox = json.load(json_data)
url_get_unread_messages_total = app.config['UNREAD_MESSAGES_TOTAL_URL']

encoded_jwt = 'testjwt'


class TestSecureMessaging(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    @requests_mock.mock()
    def test_get_messages_list(self, mock_request):
        mock_request.get(url_get_messages_list_INBOX, json=messages_list_inbox)
        mock_request.get(url_get_unread_messages_total, json={"total": "10"})
        headers = {'authorization': encoded_jwt}

        response = self.app.get("/messages_list?label=INBOX", headers=headers)

        self.assertEqual(response.status_code, 200)
        self.assertTrue('The European languages are members of the same family'.encode() in response.data)
        self.assertTrue('"total": "10"'.encode() in response.data)

    @requests_mock.mock()
    def test_get_messages_list_connection_error(self, mock_request):
        mock_request.get(url_get_messages_list_INBOX, exc=requests.exceptions.ConnectionError)
        headers = {'authorization': encoded_jwt}

        response = self.app.get("/messages_list?label=INBOX", headers=headers)

        self.assertEqual(response.status_code, 500)
        self.assertTrue('External request failed'.encode() in response.data)

    @requests_mock.mock()
    def test_get_messages_list_connection_timeout(self, mock_request):
        mock_request.get(url_get_messages_list_INBOX, exc=requests.exceptions.ConnectTimeout)
        headers = {'authorization': encoded_jwt}

        response = self.app.get("/messages_list?label=INBOX", headers=headers)

        self.assertEqual(response.status_code, 500)
        self.assertTrue('External request failed'.encode() in response.data)

    @requests_mock.mock()
    def test_get_messages_list_unexpected_code(self, mock_request):
        mock_request.get(url_get_messages_list_INBOX, status_code=500)
        headers = {'authorization': encoded_jwt}

        response = self.app.get("/messages_list?label=INBOX", headers=headers)

        self.assertEqual(response.status_code, 500)
        self.assertTrue('Unexpected status code received from service'.encode() in response.data)

    @requests_mock.mock()
    def test_get_messages_list_invalid_method(self, mock_request):
        mock_request.get(url_get_messages_list_INBOX, exc=InvalidRequestMethod('GOT', 'http://fakeurl.com'))
        headers = {'authorization': encoded_jwt}

        response = self.app.get("/messages_list?label=INBOX", headers=headers)

        self.assertEqual(response.status_code, 500)
        self.assertTrue('Invalid request method'.encode() in response.data)

    @requests_mock.mock()
    def test_get_messages_list_no_jwt(self, mock_request):
        mock_request.get(url_get_messages_list_INBOX, json=messages_list_inbox)

        response = self.app.get("/messages_list?label=INBOX")

        self.assertEqual(response.status_code, 401)
        self.assertTrue('No JWT provided in request header'.encode() in response.data)

    @requests_mock.mock()
    def test_get_messages_unread_total_unexpected_code(self, mock_request):
        mock_request.get(url_get_messages_list_INBOX, json=messages_list_inbox)
        mock_request.get(url_get_unread_messages_total, status_code=500)
        headers = {'authorization': encoded_jwt}

        response = self.app.get("/messages_list?label=INBOX", headers=headers)

        self.assertEqual(response.status_code, 500)
        self.assertTrue("Unexpected status code received from service".encode() in response.data)
