import json
import logging

from structlog import wrap_logger

from frontstage_api import app
from frontstage_api.common.request_handler import request_handler
from frontstage_api.exceptions.exceptions import ApiError


logger = wrap_logger(logging.getLogger(__name__))


def get_messages_list(encoded_jwt, label):
    logger.debug('Attempting to retrieve the messages list', label=label)
    url = '{}&label={}'.format(app.config['MESSAGES_LIST_URL'], label)
    headers = {"Authorization": encoded_jwt}
    response = request_handler('GET', url, headers=headers, error_code='FA001')

    if response.status_code != 200:
        logger.error('Error retrieving the messages list', label=label, status_code=response.status_code)
        raise ApiError('FA001')

    logger.debug('Successfully retrieved the messages list', label=label)
    messages_json = {"messages": json.loads(response.text)}
    return messages_json


def get_unread_message_total(encoded_jwt):
    logger.debug('Attempting to retrieve the unread message total')
    url = app.config['UNREAD_MESSAGES_TOTAL_URL']
    headers = {"Authorization": encoded_jwt}
    response = request_handler('GET', url, headers=headers, error_code='FA002')

    if response.status_code != 200:
        error_json = {
            "error": {
                "code": "FA002"
            }
        }
        return error_json

    logger.debug('Successfully retrieved the unread message total')
    return {"unread_messages_total": json.loads(response.text).get('total')}


def get_message(encoded_jwt, message_id, label):
    logger.debug('Attempting to retrieve message', message_id=message_id, label=label)
    url = app.config['DRAFT_URL'] if label == 'DRAFT' else app.config['MESSAGE_URL']
    url = '{}/{}'.format(url, message_id)
    headers = {"Authorization": encoded_jwt}
    response = request_handler('GET', url, headers=headers, error_code='FA003')

    if response.status_code != 200:
        logger.error('Error retrieving the messages', status_code=response.status_code, message_id=message_id, label=label)
        raise ApiError('FA003')

    logger.debug('Successfully retrieved the messages list', message_id=message_id, label=label)
    return json.loads(response.text)


def get_thread_message(encoded_jwt, thread_id, party_id):
    logger.debug('Attempting to retrieve thread message', thread_id=thread_id, party_id=party_id)
    method = 'GET'
    url = '{}/{}'.format(app.config['THREAD_URL'], thread_id)
    headers = {"Authorization": encoded_jwt}
    response = request_handler(method, url, headers=headers, error_code='FA004')

    if response.status_code != 200:
        logger.error('Error retrieving the thread message', status_code=response.status_code, thread_id=thread_id, party_id=party_id)
        raise ApiError('FA004')

    # Look for the last message in the thread not from the given party id
    thread = json.loads(response.text)
    for thread_message in thread['messages']:
        if thread_message['@msg_from']['id'] != party_id:
            message = thread_message
            break
    else:
        logger.debug('No message found in thread not belonging to the user', thread_id=thread_id, party_id=party_id)
        message = {}

    logger.debug('Retrieved message from thread successfully', thread_id=thread_id, party_id=party_id)
    return message


def remove_unread_label(encoded_jwt, message_id):
    logger.debug('Attempting to remove unread label', message_id=message_id)
    url = app.config['REMOVE_UNREAD_LABEL_URL'].format(message_id)
    headers = {"Authorization": encoded_jwt}
    data = {"label": 'UNREAD', "action": 'remove'}
    response = request_handler('PUT', url, headers=headers, json=data, error_code='FA005')

    if response.status_code != 200:
        logger.error('Error removing unread message label', status_code=response.status_code, message_id=message_id)
        error_json = {
            "error": {
                "code": "FA005"
            }
        }
        return error_json

    logger.debug('Successfully removed unread label')
    return {"unread_message_removed": True}


def send_message(encoded_jwt, message_json):
    logger.debug('Attempting to send message')
    headers = {"Authorization": encoded_jwt}
    url = app.config['SEND_MESSAGE_URL']
    response = request_handler('POST', url, headers=headers, json=message_json, error_code='FA007')

    if response.status_code == 400:
        logger.debug('Form submitted with errors')
        error_json = {
            "error": {
                "code": "FA006",
                "data": {
                    "form_errors": json.loads(response.text)
                }
            }
        }
        return error_json
    elif response.status_code != 201:
        logger.error('Failed to create message')
        raise ApiError('FA007')

    message = json.loads(response.text)
    logger.info('Secure Message sent successfully', message_id=message['msg_id'])
    return message


def save_draft(encoded_jwt, message_json):
    logger.debug('Attempting to send message')
    headers = {"Authorization": encoded_jwt}

    # If message already exists modify, otherwise save a new draft
    if message_json.get('msg_id'):
        url = app.config['DRAFT_MODIFY_URL'].format(message_json['msg_id'])
        response = request_handler('PUT', url, headers=headers, json=message_json, error_code='FA007')
    else:
        url = app.config['DRAFT_SAVE_URL']
        response = request_handler('POST', url, headers=headers, json=message_json, error_code='FA007')

    if response.status_code == 400:
        logger.debug('Form submitted with errors')
        error_json = {
            "error": {
                "code": "FA006",
                "data": {
                    "form_errors": json.loads(response.text)
                }
            }
        }
        return error_json
    elif response.status_code != 201 and response.status_code != 200:
        logger.error('Failed to save draft')
        raise ApiError('FA008')

    message = json.loads(response.text)
    logger.info('Secure Message sent successfully', message_id=message['msg_id'])
    return message
