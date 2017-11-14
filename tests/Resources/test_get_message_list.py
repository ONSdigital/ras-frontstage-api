import base64
import json
import unittest

import requests
import requests_mock

from frontstage_api import app
from frontstage_api.exceptions.exceptions import InvalidRequestMethod


url_get_messages_list_INBOX = '{}&label={}'.format(app.config['MESSAGES_LIST_URL'], 'INBOX')
with open('tests/test_data/secure_messaging/messages_list_inbox.json') as json_data:
    messages_list_inbox = json.load(json_data)
url_get_unread_messages_total = app.config['UNREAD_MESSAGES_TOTAL_URL']
url_get_message = '{}/{}'.format(app.config['MESSAGE_URL'], 'dfcb2b2c-a1d8-4d86-a974-7ffe05a3141b')
with open('tests/test_data/secure_messaging/message.json') as json_data:
    message = json.load(json_data)

encoded_jwt = 'testjwt'


class TestGetMessageList(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.headers = {
            'jwt': encoded_jwt,
            'Authorization': 'Basic {}'.format(base64.b64encode(
                bytes("{}:{}".format(app.config['SECURITY_USER_NAME'], app.config['SECURITY_USER_PASSWORD']),
                      'ascii')).decode("ascii"))
        }

    @requests_mock.mock()
    def test_get_messages_list(self, mock_request):
        mock_request.get(url_get_messages_list_INBOX, json=messages_list_inbox)
        mock_request.get(url_get_unread_messages_total, json={"total": "10"})

        response = self.app.get("/messages-list?label=INBOX", headers=self.headers)

        self.assertEqual(response.status_code, 200)
        self.assertTrue('The European languages are members of the same family'.encode() in response.data)
        self.assertTrue('"unread_messages_total": "10"'.encode() in response.data)

    @requests_mock.mock()
    def test_get_messages_list_connection_error(self, mock_request):
        mock_request.get(url_get_messages_list_INBOX, exc=requests.exceptions.ConnectionError)

        response = self.app.get("/messages-list?label=INBOX", headers=self.headers)

        self.assertEqual(response.status_code, 500)
        self.assertTrue('"url": "{}"'.format(url_get_messages_list_INBOX).encode() in response.data)

    @requests_mock.mock()
    def test_get_messages_list_unread_total_connection_error(self, mock_request):
        mock_request.get(url_get_messages_list_INBOX, json=messages_list_inbox)
        mock_request.get(url_get_unread_messages_total, exc=requests.exceptions.ConnectionError)

        response = self.app.get("/messages-list?label=INBOX", headers=self.headers)

        self.assertEqual(response.status_code, 200)
        self.assertTrue('"unread_messages_total": "error"'.encode() in response.data)

    @requests_mock.mock()
    def test_get_messages_list_fail(self, mock_request):
        mock_request.get(url_get_messages_list_INBOX, status_code=500)

        response = self.app.get("/messages-list?label=INBOX", headers=self.headers)

        self.assertEqual(response.status_code, 500)
        self.assertTrue('"status_code": 500'.encode() in response.data)

    @requests_mock.mock()
    def test_get_messages_list_invalid_method(self, mock_request):
        mock_request.get(url_get_messages_list_INBOX, exc=InvalidRequestMethod('GOT', 'http://fakeurl.com'))

        response = self.app.get("/messages-list?label=INBOX", headers=self.headers)

        self.assertEqual(response.status_code, 500)
        self.assertTrue('Invalid request method'.encode() in response.data)

    @requests_mock.mock()
    def test_get_messages_list_no_jwt(self, mock_request):
        mock_request.get(url_get_messages_list_INBOX, json=messages_list_inbox)

        response = self.app.get("/messages-list?label=INBOX")

        self.assertEqual(response.status_code, 401)
        self.assertTrue('No JWT provided in request header'.encode() in response.data)

    @requests_mock.mock()
    def test_get_messages_unread_total_unexpected_code(self, mock_request):
        mock_request.get(url_get_messages_list_INBOX, json=messages_list_inbox)
        mock_request.get(url_get_unread_messages_total, status_code=500)

        response = self.app.get("/messages-list?label=INBOX", headers=self.headers)

        self.assertEqual(response.status_code, 200)
        self.assertTrue('The European languages are members of the same family'.encode() in response.data)
        self.assertTrue('"unread_messages_total": "error"'.encode() in response.data)

    # Test get request to endpoint without basic auth in header
    def test_get_message_no_basic_auth(self):
        response = self.app.get("/messages-list?label=INBOX")

        self.assertEqual(response.status_code, 401)
