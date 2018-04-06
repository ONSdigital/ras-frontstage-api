import json
import logging

from structlog import wrap_logger

from frontstage_api import app
from frontstage_api.common.request_handler import request_handler
from frontstage_api.exceptions.exceptions import ApiError


logger = wrap_logger(logging.getLogger(__name__))


def get_messages_list(encoded_jwt, label):
    logger.debug('Attempting to retrieve the messages list', label=label)
    url = f"{app.config['RAS_SECURE_MESSAGE_SERVICE']}/messages?limit={app.config['MESSAGE_LIMIT']}&label={label}"
    headers = {"Authorization": encoded_jwt}
    response = request_handler('GET', url, headers=headers)

    if response.status_code != 200:
        raise ApiError(url=url, status_code=response.status_code, description='Error retrieving the messages list', label=label)

    logger.debug('Successfully retrieved the messages list', label=label)
    messages_json = {"messages": json.loads(response.text)}
    return messages_json


def get_unread_message_total(encoded_jwt):
    logger.debug('Attempting to retrieve the unread message total')
    url = f"{app.config['RAS_SECURE_MESSAGE_SERVICE']}/labels?name=unread"
    headers = {"Authorization": encoded_jwt}
    response = request_handler('GET', url, headers=headers, fail=False)

    # If request failed or if status code is not 200 return empty unread message total
    if not response or response.status_code != 200:
        logger.debug('Failed to retrieve the unread message total')
        unread_message_total = 'error'
    else:
        logger.debug('Successfully retrieved the unread message total')
        unread_message_total = json.loads(response.text).get('total')

    return {"unread_messages_total": unread_message_total}


def get_message(encoded_jwt, message_id, label):
    logger.debug('Attempting to retrieve message', message_id=message_id, label=label)
    url = f"{app.config['RAS_SECURE_MESSAGE_SERVICE']}/draft" if label == 'DRAFT' else f"{app.config['RAS_SECURE_MESSAGE_SERVICE']}/message"
    url = f'{url}/{message_id}'
    headers = {"Authorization": encoded_jwt}
    response = request_handler('GET', url, headers=headers)

    if response.status_code != 200:
        raise ApiError(url=url, status_code=response.status_code, description='Error retrieving the messages',
                       message_id=message_id, label=label)

    logger.debug('Successfully retrieved message', message_id=message_id, label=label)
    return json.loads(response.text)


def get_thread_message(encoded_jwt, thread_id, party_id):
    logger.debug('Attempting to retrieve thread message', thread_id=thread_id, party_id=party_id)
    method = 'GET'
    url = f"{app.config['RAS_SECURE_MESSAGE_SERVICE']}/thread/{thread_id}"
    headers = {"Authorization": encoded_jwt}
    response = request_handler(method, url, headers=headers)

    if response.status_code != 200:
        raise ApiError(url=url, status_code=response.status_code, description='Error retrieving the thread message',
                       thread_id=thread_id, party_id=party_id)

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
    url = f"{app.config['RAS_SECURE_MESSAGE_SERVICE']}/message/{message_id}/modify"
    headers = {"Authorization": encoded_jwt}
    data = {"label": 'UNREAD', "action": 'remove'}
    response = request_handler('PUT', url, headers=headers, json=data, fail=False)

    if not response or response.status_code != 200:
        logger.error('Error removing unread message label', status_code=response.status_code, message_id=message_id)
        unread_label_removed = False
    else:
        logger.debug('Successfully removed unread label')
        unread_label_removed = True

    return {"unread_label_removed": unread_label_removed}


def send_message(encoded_jwt, message_json):
    logger.debug('Attempting to send message')
    headers = {"Authorization": encoded_jwt}
    url = f"{app.config['RAS_SECURE_MESSAGE_SERVICE']}/v2/messages"
    response = request_handler('POST', url, headers=headers, json=message_json)

    if response.status_code == 400:
        logger.debug('Form submitted with errors')
        form_errors = json.loads(response.text)
        return {"form_errors": form_errors}
    elif response.status_code != 201:
        raise ApiError(url=url, status_code=response.status_code, description='Failed to send message')

    message = json.loads(response.text)
    logger.info('Secure Message sent successfully', message_id=message['msg_id'])
    return message


def save_draft(encoded_jwt, message_json):
    logger.debug('Attempting to send message')
    headers = {"Authorization": encoded_jwt}

    # If message already exists modify, otherwise save a new draft
    if message_json.get('msg_id'):
        url = f"{app.config['RAS_SECURE_MESSAGE_SERVICE']}/draft/{message_json['msg_id']}/modify"
        response = request_handler('PUT', url, headers=headers, json=message_json)
    else:
        url = f"{app.config['RAS_SECURE_MESSAGE_SERVICE']}/draft/save"
        response = request_handler('POST', url, headers=headers, json=message_json)

    if response.status_code == 400:
        logger.debug('Form submitted with errors')
        form_errors = json.loads(response.text)
        return {"form_errors": form_errors}
    elif response.status_code != 201 and response.status_code != 200:
        raise ApiError(url=url, status_code=response.status_code, description='Failed to save draft')

    message = json.loads(response.text)
    logger.info('Secure Message sent successfully', message_id=message['msg_id'])
    return message
