import base64
import json
import unittest

import requests_mock

from frontstage_api import app


url_get_thread = f"{app.config['THREAD_URL']}/dfcb2b2c-a1d8-4d86-a974-7ffe05a3141c"
with open('tests/test_data/secure_messaging/thread.json') as json_data:
    thread = json.load(json_data)
with open('tests/test_data/secure_messaging/thread_no_party.json') as json_data:
    thread_no_party = json.load(json_data)
url_get_party_from_id = app.config['RAS_PARTY_GET_BY_RESPONDENT_ID'].format('07d672bc-497b-448f-a406-a20a7e6013d7')
with open('tests/test_data/party/party.json') as json_data:
    party = json.load(json_data)
url_get_case_from_party_id = app.config['RM_CASE_GET_BY_PARTY'].format('07d672bc-497b-448f-a406-a20a7e6013d7')
with open('tests/test_data/case/case.json') as json_data:
    case = [json.load(json_data)]
url_send_message = app.config['SEND_MESSAGE_URL']
url_save_draft = app.config['DRAFT_SAVE_URL']
url_modify_draft = app.config['DRAFT_MODIFY_URL'].format('msg_id')

encoded_jwt = 'testjwt'


class TestSendMessage(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.posted_message = {
            'msg_from': '07d672bc-497b-448f-a406-a20a7e6013d7',
            'msg_to': ['GROUP'],
            'subject': 'test-subject',
            'body': 'test-body',
            'thread_id': '',
            'ru_id': 'testru',
            'survey': 'testsurvey',
            'collection_case': 'testcase'
        }
        self.sent_message_response = {
            'msg_id': '36f3133c-9ead-4168-a40e-f07947671b02',
            'status': '201',
            'thread_id': '8caeff79-6067-4f2a-96e0-08617fdeb496'
        }
        auth_string = base64.b64encode(
            bytes(f"{app.config['SECURITY_USER_NAME']}:{app.config['SECURITY_USER_PASSWORD']}", 'ascii')
        ).decode("ascii")
        self.headers = {
            'Authorization': f'Basic {auth_string}',
            'Content-Type': 'application/json',
            'jwt': encoded_jwt,
        }

    @requests_mock.mock()
    def test_post_send_message(self, mock_request):
        mock_request.get(url_get_party_from_id, json=party)
        mock_request.get(url_get_case_from_party_id, json=case)
        mock_request.post(url_send_message, status_code=201, json=self.sent_message_response)

        response = self.app.post('/secure-messaging/send-message?is_draft=False', data=json.dumps(self.posted_message), headers=self.headers)

        self.assertEqual(response.status_code, 200)
        self.assertTrue('"status": "201"'.encode() in response.data)

    @requests_mock.mock()
    def test_post_send_message_party_fail(self, mock_request):
        mock_request.get(url_get_party_from_id, status_code=500)

        response = self.app.post('/secure-messaging/send-message?is_draft=False', data=json.dumps(self.posted_message), headers=self.headers)

        self.assertEqual(response.status_code, 500)
        self.assertTrue('Internal Server Error'.encode() in response.data)

    @requests_mock.mock()
    def test_post_send_message_case_fail(self, mock_request):
        mock_request.get(url_get_party_from_id, json=party)
        mock_request.get(url_get_case_from_party_id, status_code=500)

        response = self.app.post('/secure-messaging/send-message?is_draft=False', data=json.dumps(self.posted_message), headers=self.headers)

        self.assertEqual(response.status_code, 500)
        self.assertTrue('Internal Server Error'.encode() in response.data)

    @requests_mock.mock()
    def test_post_send_message_fail(self, mock_request):
        mock_request.get(url_get_party_from_id, json=party)
        mock_request.get(url_get_case_from_party_id, json=case)
        mock_request.post(url_send_message, status_code=500)

        response = self.app.post('/secure-messaging/send-message?is_draft=False', data=json.dumps(self.posted_message), headers=self.headers)

        self.assertEqual(response.status_code, 500)
        self.assertTrue('"status_code": 500'.encode() in response.data)

    @requests_mock.mock()
    def test_post_send_message_form_errors(self, mock_request):
        mock_request.get(url_get_party_from_id, json=party)
        mock_request.get(url_get_case_from_party_id, json=case)
        form_errors = {'body': ['Body field length must not be greater than 10000']}
        mock_request.post(url_send_message, status_code=400, json=form_errors)

        response = self.app.post('/secure-messaging/send-message?is_draft=False', data=json.dumps(self.posted_message), headers=self.headers)

        self.assertEqual(response.status_code, 400)
        self.assertTrue('"form_errors"'.encode() in response.data)

    @requests_mock.mock()
    def test_post_send_message_form_errors_existing_thread(self, mock_request):
        mock_request.get(url_get_party_from_id, json=party)
        mock_request.get(url_get_case_from_party_id, json=case)
        form_errors = {'body': ['Body field length must not be greater than 10000']}
        mock_request.post(url_send_message, status_code=400, json=form_errors)
        mock_request.get(url_get_thread, json=thread)
        self.posted_message['thread_id'] = 'dfcb2b2c-a1d8-4d86-a974-7ffe05a3141c'

        response = self.app.post('/secure-messaging/send-message?is_draft=False', data=json.dumps(self.posted_message), headers=self.headers)

        self.assertEqual(response.status_code, 400)
        self.assertTrue('"body": "sending"'.encode() in response.data)
        self.assertTrue('"form_errors"'.encode() in response.data)

    @requests_mock.mock()
    def test_post_save_draft(self, mock_request):
        mock_request.get(url_get_party_from_id, json=party)
        mock_request.get(url_get_case_from_party_id, json=case)
        mock_request.post(url_save_draft, status_code=201, json=self.sent_message_response)

        response = self.app.post('/secure-messaging/send-message?is_draft=True', data=json.dumps(self.posted_message), headers=self.headers)

        self.assertEqual(response.status_code, 200)
        self.assertTrue('"status": "201"'.encode() in response.data)

    @requests_mock.mock()
    def test_post_save_draft_fail(self, mock_request):
        mock_request.get(url_get_party_from_id, json=party)
        mock_request.get(url_get_case_from_party_id, json=case)
        mock_request.post(url_save_draft, status_code=500)

        response = self.app.post('/secure-messaging/send-message?is_draft=True', data=json.dumps(self.posted_message), headers=self.headers)

        self.assertEqual(response.status_code, 500)
        self.assertTrue('"status_code": 500'.encode() in response.data)

    @requests_mock.mock()
    def test_post_save_draft_form_errors(self, mock_request):
        mock_request.get(url_get_party_from_id, json=party)
        mock_request.get(url_get_case_from_party_id, json=case)
        form_errors = {'body': ['Body field length must not be greater than 10000']}
        mock_request.post(url_save_draft, status_code=400, json=form_errors)

        response = self.app.post('/secure-messaging/send-message?is_draft=True', data=json.dumps(self.posted_message), headers=self.headers)

        self.assertEqual(response.status_code, 400)
        self.assertTrue('"form_errors"'.encode() in response.data)

    @requests_mock.mock()
    def test_post_modify_draft(self, mock_request):
        mock_request.get(url_get_party_from_id, json=party)
        mock_request.get(url_get_case_from_party_id, json=case)
        mock_request.put(url_modify_draft, status_code=200, json=self.sent_message_response)
        self.posted_message['msg_id'] = 'msg_id'

        response = self.app.post('/secure-messaging/send-message?is_draft=True', data=json.dumps(self.posted_message), headers=self.headers)

        self.assertEqual(response.status_code, 200)
        self.assertTrue('"status": "201"'.encode() in response.data)

    # Test posting to endpoint without basic auth in header
    def test_request_password_change_no_basic_auth(self):
        del self.headers['Authorization']
        response = self.app.post('/secure-messaging/send-message?is_draft=True',
                                 headers=self.headers,
                                 data=json.dumps(self.posted_message))

        self.assertEqual(response.status_code, 401)
