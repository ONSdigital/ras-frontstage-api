import json
import logging

from structlog import wrap_logger

from frontstage_api import app
from frontstage_api.common.request_handler import request_handler
from frontstage_api.exceptions.exceptions import ApiError


logger = wrap_logger(logging.getLogger(__name__))


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
