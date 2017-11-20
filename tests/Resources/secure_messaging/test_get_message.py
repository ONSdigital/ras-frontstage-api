import base64
import json
import unittest

import requests_mock

from frontstage_api import app


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
url_remove_unread_label = app.config['REMOVE_UNREAD_LABEL_URL'].format('dfcb2b2c-a1d8-4d86-a974-7ffe05a3141b')
encoded_jwt = 'testjwt'


class TestGetMessage(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

        self.headers = {
            'jwt': encoded_jwt,
            'Content-Type': 'application/json',
            'Authorization': 'Basic {}'.format(base64.b64encode(
                bytes("{}:{}".format(app.config['SECURITY_USER_NAME'], app.config['SECURITY_USER_PASSWORD']),
                      'ascii')).decode("ascii"))
        }

    @requests_mock.mock()
    def test_get_message(self, mock_request):
        mock_request.get(url_get_message, json=message)
        message_url = "/secure-messaging/message?message_id=dfcb2b2c-a1d8-4d86-a974-7ffe05a3141b&label=INBOX&party_id=1f5e1d68-2a4c-4698-8086-e23c0b98923f"

        response = self.app.get(message_url, headers=self.headers)

        self.assertEqual(response.status_code, 200)
        self.assertTrue('"body": "TEsdfdsfST"'.encode() in response.data)

    @requests_mock.mock()
    def test_get_message_fail(self, mock_request):
        mock_request.get(url_get_message, status_code=500)
        message_url = "/secure-messaging/message?message_id=dfcb2b2c-a1d8-4d86-a974-7ffe05a3141b&label=INBOX&party_id=1f5e1d68-2a4c-4698-8086-e23c0b98923f"

        response = self.app.get(message_url, headers=self.headers)

        self.assertEqual(response.status_code, 500)
        self.assertTrue('"status_code": 500'.encode() in response.data)

    @requests_mock.mock()
    def test_get_message_draft_no_thread(self, mock_request):
        mock_request.get(url_get_draft, json=draft)
        message_url = "/secure-messaging/message?message_id=dfcb2b2c-a1d8-4d86-a974-7ffe05a3141b&label=DRAFT&party_id=1f5e1d68-2a4c-4698-8086-e23c0b98923f"

        response = self.app.get(message_url, headers=self.headers)

        self.assertEqual(response.status_code, 200)
        self.assertTrue('"body": "TEsdfdsfST"'.encode() in response.data)

    @requests_mock.mock()
    def test_get_message_draft_with_thread(self, mock_request):
        mock_request.get(url_get_draft, json=draft_with_thread)
        mock_request.get(url_get_thread, json=thread)
        message_url = "/secure-messaging/message?message_id=dfcb2b2c-a1d8-4d86-a974-7ffe05a3141b&label=DRAFT&party_id=1f5e1d68-2a4c-4698-8086-e23c0b98923f"

        response = self.app.get(message_url, headers=self.headers)

        self.assertEqual(response.status_code, 200)
        self.assertTrue('"body": "TEsdfdsfST"'.encode() in response.data)
        self.assertTrue('"body": "Replying "'.encode() in response.data)

    @requests_mock.mock()
    def test_get_message_draft_thread_no_party(self, mock_request):
        mock_request.get(url_get_draft, json=draft_with_thread)
        mock_request.get(url_get_thread, json=thread_no_party)
        message_url = "/secure-messaging/message?message_id=dfcb2b2c-a1d8-4d86-a974-7ffe05a3141b&label=DRAFT&party_id=1f5e1d68-2a4c-4698-8086-e23c0b98923f"

        response = self.app.get(message_url, headers=self.headers)

        self.assertEqual(response.status_code, 200)
        self.assertTrue('"body": "TEsdfdsfST"'.encode() in response.data)

    @requests_mock.mock()
    def test_get_message_draft_thread_fail(self, mock_request):
        mock_request.get(url_get_draft, json=draft_with_thread)
        mock_request.get(url_get_thread, status_code=500)
        message_url = "/secure-messaging/message?message_id=dfcb2b2c-a1d8-4d86-a974-7ffe05a3141b&label=DRAFT&party_id=1f5e1d68-2a4c-4698-8086-e23c0b98923f"

        response = self.app.get(message_url, headers=self.headers)

        self.assertEqual(response.status_code, 500)
        self.assertTrue('"status_code": 500'.encode() in response.data)

    @requests_mock.mock()
    def test_get_message_unread(self, mock_request):
        mock_request.get(url_get_message, json=message)
        mock_request.put(url_remove_unread_label)
        message_url = "/secure-messaging/message?message_id=dfcb2b2c-a1d8-4d86-a974-7ffe05a3141b&label=UNREAD&party_id=1f5e1d68-2a4c-4698-8086-e23c0b98923f"

        response = self.app.get(message_url, headers=self.headers)

        self.assertEqual(response.status_code, 200)
        self.assertTrue('"body": "TEsdfdsfST"'.encode() in response.data)

    @requests_mock.mock()
    def test_get_message_remove_unread_fail(self, mock_request):
        mock_request.get(url_get_message, json=message)
        mock_request.put(url_remove_unread_label, status_code=500)
        message_url = "/secure-messaging/message?message_id=dfcb2b2c-a1d8-4d86-a974-7ffe05a3141b&label=UNREAD&party_id=1f5e1d68-2a4c-4698-8086-e23c0b98923f"

        response = self.app.get(message_url, headers=self.headers)

        self.assertEqual(response.status_code, 200)
        self.assertTrue('"unread_label_removed": false'.encode() in response.data)

    # Test get request to endpoint without basic auth in header
    def test_get_message_no_basic_auth(self):
        del self.headers['Authorization']
        message_url = "/secure-messaging/message?message_id=dfcb2b2c-a1d8-4d86-a974-7ffe05a3141b&label=UNREAD&party_id=1f5e1d68-2a4c-4698-8086-e23c0b98923f"

        response = self.app.get(message_url, headers=self.headers)

        self.assertEqual(response.status_code, 401)
