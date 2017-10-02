import json
import logging

from flask import request
from structlog import wrap_logger

from frontstage_api import app
from frontstage_api.exceptions.exceptions import UnexpectedStatusCode
from frontstage_api.common.utilities import request_handler


logger = wrap_logger(logging.getLogger(__name__))


def get_messages_list(encoded_jwt):
    logger.debug('Attempting to retrieve the messages list')
    method = 'GET'
    url = app.config['MESSAGES_LIST_URL']
    headers = {"Authorization": encoded_jwt}
    label = request.args.get('label')
    if label is not None:
        url = url + "&label=" + label
    response = request_handler(method, url, headers)

    if response.status_code != 200:
        logger.error('Error retrieving the messages list', status_code=response.status_code)
        raise UnexpectedStatusCode(method, url, response.status_code, response.content)

    logger.debug('Successfully retrieved the messages list')
    return json.loads(response.text)


def get_unread_message_total(encoded_jwt):
    logger.debug('Attempting to retrieve the unread message total')
    method = 'GET'
    url = app.config['UNREAD_MESSAGES_TOTAL_URL']
    headers = {"Authorization": encoded_jwt}
    response = request_handler(method, url, headers)

    if response.status_code != 200:
        logger.error('Error retrieving the unread messages total', status_code=response.status_code)
        raise UnexpectedStatusCode(method, url, response.status_code, response.content)

    logger.debug('Successfully retrieved the unread message total')
    return json.loads(response.text)
