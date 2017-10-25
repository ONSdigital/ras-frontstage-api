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
url_get_party_from_id = app.config['PARTY_BY_RESPONDENT_ID'].format('07d672bc-497b-448f-a406-a20a7e6013d7')
with open('tests/test_data/party/party.json') as json_data:
    party = json.load(json_data)
url_get_case_from_party_id = app.config['RM_CASE_GET_BY_PARTY'].format('07d672bc-497b-448f-a406-a20a7e6013d7')
with open('tests/test_data/case/case.json') as json_data:
    case = json.load(json_data)
url_send_message = app.config['SEND_MESSAGE_URL']
url_save_draft = app.config['DRAFT_SAVE_URL']
url_modify_draft = app.config['DRAFT_MODIFY_URL'].format('msg_id')

encoded_jwt = 'testjwt'


class TestSecureMessaging(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.posted_message = {
            'msg_from': '07d672bc-497b-448f-a406-a20a7e6013d7',
            'subject': 'test-subject',
            'body': 'test-body',
            'thread_id': ''
        }
        self.sent_message_response = {
            'msg_id': '36f3133c-9ead-4168-a40e-f07947671b02',
            'status': '201',
            'thread_id': '8caeff79-6067-4f2a-96e0-08617fdeb496'
        }

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

        self.assertEqual(response.status_code, 200)
        self.assertTrue('"code": "FA001"'.encode() in response.data)

    @requests_mock.mock()
    def test_get_messages_list_fail(self, mock_request):
        mock_request.get(url_get_messages_list_INBOX, status_code=500)
        headers = {'authorization': encoded_jwt}

        response = self.app.get("/messages_list?label=INBOX", headers=headers)

        self.assertEqual(response.status_code, 200)
        self.assertTrue('"code": "FA001"'.encode() in response.data)

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
        self.assertTrue('The European languages are members of the same family'.encode() in response.data)
        self.assertTrue('"code": "FA002"'.encode() in response.data)

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
        self.assertTrue('"code": "FA003"'.encode() in response.data)

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
        self.assertTrue('"code": "FA004"'.encode() in response.data)

    @requests_mock.mock()
    def test_get_message_unread(self, mock_request):
        mock_request.get(url_get_message, json=message)
        mock_request.put(url_remove_unread_label)
        headers = {'authorization': encoded_jwt}
        message_url = "/message?message_id=dfcb2b2c-a1d8-4d86-a974-7ffe05a3141b&label=UNREAD&party_id=1f5e1d68-2a4c-4698-8086-e23c0b98923f"

        response = self.app.get(message_url, headers=headers)

        self.assertEqual(response.status_code, 200)
        self.assertTrue('"body": "TEsdfdsfST"'.encode() in response.data)

    @requests_mock.mock()
    def test_get_message_remove_unread_fail(self, mock_request):
        mock_request.get(url_get_message, json=message)
        mock_request.put(url_remove_unread_label, status_code=500)
        headers = {'authorization': encoded_jwt}
        message_url = "/message?message_id=dfcb2b2c-a1d8-4d86-a974-7ffe05a3141b&label=UNREAD&party_id=1f5e1d68-2a4c-4698-8086-e23c0b98923f"

        response = self.app.get(message_url, headers=headers)

        self.assertEqual(response.status_code, 200)
        self.assertTrue('"code": "FA005"'.encode() in response.data)

    @requests_mock.mock()
    def test_post_send_message(self, mock_request):
        mock_request.get(url_get_party_from_id, json=party)
        mock_request.get(url_get_case_from_party_id, json=case)
        mock_request.post(url_send_message, status_code=201, json=self.sent_message_response)

        headers = {'authorization': encoded_jwt}

        response = self.app.post('/send_message?is_draft=False', data=json.dumps(self.posted_message), headers=headers)

        self.assertEqual(response.status_code, 200)
        self.assertTrue('"status": "201"'.encode() in response.data)

    @requests_mock.mock()
    def test_post_send_message_party_fail(self, mock_request):
        mock_request.get(url_get_party_from_id, status_code=500)
        headers = {'authorization': encoded_jwt}

        response = self.app.post('/send_message?is_draft=False', data=json.dumps(self.posted_message), headers=headers)

        self.assertEqual(response.status_code, 200)
        self.assertTrue('"code": "FA101"'.encode() in response.data)

    @requests_mock.mock()
    def test_post_send_message_party_not_found(self, mock_request):
        mock_request.get(url_get_party_from_id, status_code=404)
        headers = {'authorization': encoded_jwt}

        response = self.app.post('/send_message?is_draft=False', data=json.dumps(self.posted_message), headers=headers)

        self.assertEqual(response.status_code, 200)
        self.assertTrue('"code": "FA100"'.encode() in response.data)

    @requests_mock.mock()
    def test_post_send_message_case_fail(self, mock_request):
        mock_request.get(url_get_party_from_id, json=party)
        mock_request.get(url_get_case_from_party_id, status_code=500)
        headers = {'authorization': encoded_jwt}

        response = self.app.post('/send_message?is_draft=False', data=json.dumps(self.posted_message), headers=headers)

        self.assertEqual(response.status_code, 200)
        self.assertTrue('"code": "FA201"'.encode() in response.data)

    @requests_mock.mock()
    def test_post_send_message_case_not_found(self, mock_request):
        mock_request.get(url_get_party_from_id, json=party)
        mock_request.get(url_get_case_from_party_id, status_code=204)
        headers = {'authorization': encoded_jwt}

        response = self.app.post('/send_message?is_draft=False', data=json.dumps(self.posted_message), headers=headers)

        self.assertEqual(response.status_code, 200)
        self.assertTrue('"code": "FA200"'.encode() in response.data)

    @requests_mock.mock()
    def test_post_send_message_fail(self, mock_request):
        mock_request.get(url_get_party_from_id, json=party)
        mock_request.get(url_get_case_from_party_id, json=case)
        mock_request.post(url_send_message, status_code=500)
        headers = {'authorization': encoded_jwt}

        response = self.app.post('/send_message?is_draft=False', data=json.dumps(self.posted_message), headers=headers)

        self.assertEqual(response.status_code, 200)
        self.assertTrue('"code": "FA007"'.encode() in response.data)

    @requests_mock.mock()
    def test_post_send_message_form_errors(self, mock_request):
        mock_request.get(url_get_party_from_id, json=party)
        mock_request.get(url_get_case_from_party_id, json=case)
        form_errors = {'body': ['Body field length must not be greater than 10000']}
        mock_request.post(url_send_message, status_code=400, json=form_errors)
        headers = {'authorization': encoded_jwt}

        response = self.app.post('/send_message?is_draft=False', data=json.dumps(self.posted_message), headers=headers)

        self.assertEqual(response.status_code, 200)
        self.assertTrue('"form_errors"'.encode() in response.data)
        self.assertTrue('"code": "FA006"'.encode() in response.data)

    @requests_mock.mock()
    def test_post_send_message_form_errors_existing_thread(self, mock_request):
        mock_request.get(url_get_party_from_id, json=party)
        mock_request.get(url_get_case_from_party_id, json=case)
        form_errors = {'body': ['Body field length must not be greater than 10000']}
        mock_request.post(url_send_message, status_code=400, json=form_errors)
        headers = {'authorization': encoded_jwt}
        mock_request.get(url_get_thread, json=thread)
        self.posted_message['thread_id'] = 'dfcb2b2c-a1d8-4d86-a974-7ffe05a3141c'

        response = self.app.post('/send_message?is_draft=False', data=json.dumps(self.posted_message), headers=headers)

        self.assertEqual(response.status_code, 200)
        self.assertTrue('"body": "sending"'.encode() in response.data)
        self.assertTrue('"form_errors"'.encode() in response.data)
        self.assertTrue('"code": "FA006"'.encode() in response.data)

    @requests_mock.mock()
    def test_post_save_draft(self, mock_request):
        mock_request.get(url_get_party_from_id, json=party)
        mock_request.get(url_get_case_from_party_id, json=case)
        mock_request.post(url_save_draft, status_code=201, json=self.sent_message_response)

        headers = {'authorization': encoded_jwt}

        response = self.app.post('/send_message?is_draft=True', data=json.dumps(self.posted_message), headers=headers)

        self.assertEqual(response.status_code, 200)
        self.assertTrue('"status": "201"'.encode() in response.data)

    @requests_mock.mock()
    def test_post_save_draft_fail(self, mock_request):
        mock_request.get(url_get_party_from_id, json=party)
        mock_request.get(url_get_case_from_party_id, json=case)
        mock_request.post(url_save_draft, status_code=500)

        headers = {'authorization': encoded_jwt}

        response = self.app.post('/send_message?is_draft=True', data=json.dumps(self.posted_message), headers=headers)

        self.assertEqual(response.status_code, 200)
        self.assertTrue('"code": "FA008"'.encode() in response.data)

    @requests_mock.mock()
    def test_post_save_draft_form_errors(self, mock_request):
        mock_request.get(url_get_party_from_id, json=party)
        mock_request.get(url_get_case_from_party_id, json=case)
        form_errors = {'body': ['Body field length must not be greater than 10000']}
        mock_request.post(url_save_draft, status_code=400, json=form_errors)

        headers = {'authorization': encoded_jwt}

        response = self.app.post('/send_message?is_draft=True', data=json.dumps(self.posted_message), headers=headers)

        self.assertEqual(response.status_code, 200)
        self.assertTrue('"form_errors"'.encode() in response.data)
        self.assertTrue('"code": "FA006"'.encode() in response.data)

    @requests_mock.mock()
    def test_post_modify_draft(self, mock_request):
        mock_request.get(url_get_party_from_id, json=party)
        mock_request.get(url_get_case_from_party_id, json=case)
        mock_request.put(url_modify_draft, status_code=200, json=self.sent_message_response)
        self.posted_message['msg_id'] = 'msg_id'
        headers = {'authorization': encoded_jwt}

        response = self.app.post('/send_message?is_draft=True', data=json.dumps(self.posted_message), headers=headers)

        self.assertEqual(response.status_code, 200)
        self.assertTrue('"status": "201"'.encode() in response.data)
