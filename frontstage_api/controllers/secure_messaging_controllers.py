import json
import logging

from flask import request
from requests import Response
from structlog import wrap_logger

from frontstage_api import app
from frontstage_api.common.request_handler import request_handler
from frontstage_api.exceptions.exceptions import UnexpectedStatusCode


logger = wrap_logger(logging.getLogger(__name__))


def get_messages_list(encoded_jwt):
    logger.debug('Attempting to retrieve the messages list')
    method = 'GET'
    label = request.args.get('label')
    url = '{}&label={}'.format(app.config['MESSAGES_LIST_URL'], label)
    headers = {"Authorization": encoded_jwt}
    response = request_handler(method, url, headers)

    # If the response status code is not 200 call exception to stop request
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
    response = request_handler(method, url, headers, fail=False)

    # If request handler has failed to generate a response return the error message
    if isinstance(response, Response):
        return response

    # If the response status code is not 200 return json error message
    if response.status_code != 200:
        logger.error('Error retrieving the unread messages total', status_code=response.status_code)
        return {
            "error": "Unexpected status code returned",
            "url": url
        }

    logger.debug('Successfully retrieved the unread message total')
    return json.loads(response.text)
