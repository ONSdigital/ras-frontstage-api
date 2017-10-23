import json
import unittest

import requests
import requests_mock

from frontstage_api import app
from frontstage_api.exceptions.exceptions import InvalidRequestMethod, UnexpectedStatusCode


url_get_messages_list_INBOX = '{}&label={}'.format(app.config['MESSAGES_LIST_URL'], 'INBOX')
with open('tests/test_data/secure_messaging/messages_list_inbox.json') as json_data:
    messages_list_inbox = json.load(json_data)
url_get_unread_messages_total = app.config['UNREAD_MESSAGES_TOTAL_URL']
url_get_message = '{}/{}'.format(app.config['MESSAGE_URL'], 'dfcb2b2c-a1d8-4d86-a974-7ffe05a3141b')
with open('tests/test_data/secure_messaging/message.json') as json_data:
    message = json.load(json_data)
url_get_draft = '{}/{}'.format(app.config['DRAFT_URL'], 'dfcb2b2c-a1d8-4d86-a974-7ffe05a3141b')
with open('tests/test_data/secure_messaging/draft.json') as json_data:
    draft = json.load(json_data)
with open('tests/test_data/secure_messaging/draft_with_thread.json') as json_data:
    draft_with_thread = json.load(json_data)
url_get_thread = '{}/{}'.format(app.config['THREAD_URL'], 'dfcb2b2c-a1d8-4d86-a974-7ffe05a3141c')
with open('tests/test_data/secure_messaging/thread.json') as json_data:
    thread = json.load(json_data)
with open('tests/test_data/secure_messaging/thread_no_party.json') as json_data:
    thread_no_party = json.load(json_data)

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

        self.assertEqual(response.status_code, 200)
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

        self.assertEqual(response.status_code, 200)
        self.assertTrue('"error": "Unexpected status code returned"'.encode() in response.data)

    @requests_mock.mock()
    def test_get_messages_unread_total_connection_error(self, mock_request):
        mock_request.get(url_get_messages_list_INBOX, json=messages_list_inbox)
        mock_request.get(url_get_unread_messages_total, exc=requests.exceptions.ConnectionError)
        headers = {'authorization': encoded_jwt}

        response = self.app.get("/messages_list?label=INBOX", headers=headers)

        self.assertEqual(response.status_code, 200)
        self.assertTrue('"error": "Connection error"'.encode() in response.data)

    @requests_mock.mock()
    def test_get_messages_unread_total_connection_timeout(self, mock_request):
        mock_request.get(url_get_messages_list_INBOX, json=messages_list_inbox)
        mock_request.get(url_get_unread_messages_total, exc=requests.exceptions.ConnectTimeout)
        headers = {'authorization': encoded_jwt}

        response = self.app.get("/messages_list?label=INBOX", headers=headers)

        self.assertEqual(response.status_code, 200)
        self.assertTrue('"error": "Connection timeout"'.encode() in response.data)

    @requests_mock.mock()
    def test_get_message(self, mock_request):
        mock_request.get(url_get_message, json=message)
        headers = {'authorization': encoded_jwt}
        message_url = "/message?message_id=dfcb2b2c-a1d8-4d86-a974-7ffe05a3141b&label=INBOX&party_id=1f5e1d68-2a4c-4698-8086-e23c0b98923f"

        response = self.app.get(message_url, headers=headers)

        self.assertEqual(response.status_code, 200)
        self.assertTrue('"body": "TEsdfdsfST"'.encode() in response.data)

    @requests_mock.mock()
    def test_get_message_fail(self, mock_request):
        mock_request.get(url_get_message, status_code=500)
        headers = {'authorization': encoded_jwt}
        message_url = "/message?message_id=dfcb2b2c-a1d8-4d86-a974-7ffe05a3141b&label=INBOX&party_id=1f5e1d68-2a4c-4698-8086-e23c0b98923f"

        response = self.app.get(message_url, headers=headers)

        self.assertEqual(response.status_code, 200)
        self.assertTrue('"status_code": 500'.encode() in response.data)

    @requests_mock.mock()
    def test_get_message_draft_no_thread(self, mock_request):
        mock_request.get(url_get_draft, json=draft)
        headers = {'authorization': encoded_jwt}
        message_url = "/message?message_id=dfcb2b2c-a1d8-4d86-a974-7ffe05a3141b&label=DRAFT&party_id=1f5e1d68-2a4c-4698-8086-e23c0b98923f"

        response = self.app.get(message_url, headers=headers)

        self.assertEqual(response.status_code, 200)
        self.assertTrue('"body": "TEsdfdsfST"'.encode() in response.data)

    @requests_mock.mock()
    def test_get_message_draft_with_thread(self, mock_request):
        mock_request.get(url_get_draft, json=draft_with_thread)
        mock_request.get(url_get_thread, json=thread)
        headers = {'authorization': encoded_jwt}
        message_url = "/message?message_id=dfcb2b2c-a1d8-4d86-a974-7ffe05a3141b&label=DRAFT&party_id=1f5e1d68-2a4c-4698-8086-e23c0b98923f"

        response = self.app.get(message_url, headers=headers)

        self.assertEqual(response.status_code, 200)
        self.assertTrue('"body": "TEsdfdsfST"'.encode() in response.data)
        self.assertTrue('"body": "Replying "'.encode() in response.data)

    @requests_mock.mock()
    def test_get_message_draft_thread_no_party(self, mock_request):
        mock_request.get(url_get_draft, json=draft_with_thread)
        mock_request.get(url_get_thread, json=thread_no_party)
        headers = {'authorization': encoded_jwt}
        message_url = "/message?message_id=dfcb2b2c-a1d8-4d86-a974-7ffe05a3141b&label=DRAFT&party_id=1f5e1d68-2a4c-4698-8086-e23c0b98923f"

        response = self.app.get(message_url, headers=headers)

        self.assertEqual(response.status_code, 200)
        self.assertTrue('"body": "TEsdfdsfST"'.encode() in response.data)

    @requests_mock.mock()
    def test_get_message_draft_thread_fail(self, mock_request):
        mock_request.get(url_get_draft, json=draft_with_thread)
        mock_request.get(url_get_thread, status_code=500)
        headers = {'authorization': encoded_jwt}
        message_url = "/message?message_id=dfcb2b2c-a1d8-4d86-a974-7ffe05a3141b&label=DRAFT&party_id=1f5e1d68-2a4c-4698-8086-e23c0b98923f"

        response = self.app.get(message_url, headers=headers)

        self.assertEqual(response.status_code, 200)
        self.assertTrue('"status_code": 500'.encode() in response.data)
