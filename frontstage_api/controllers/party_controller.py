import json
import logging

from structlog import wrap_logger

from frontstage_api import app
from frontstage_api.common.request_handler import request_handler
from frontstage_api.exceptions.exceptions import ApiError


logger = wrap_logger(logging.getLogger(__name__))


def get_party_by_respondent_id(party_id):
    logger.debug('Retrieving party', party_id=party_id)
    url = app.config['PARTY_BY_RESPONDENT_ID'].format(party_id)
    response = request_handler('GET', url, auth=app.config['BASIC_AUTH'])

    if response.status_code != 200:
        logger.error('Failed to retrieve party', party_id=party_id)
        raise ApiError(url, response.status_code)

    logger.debug('Successfully retrieved party', party_id=party_id)
    return json.loads(response.text)


def get_party_by_email(email):
    logger.debug('Retrieving party')
    url = app.config['RAS_PARTY_GET_BY_EMAIL_URL'].format(email)
    response = request_handler('GET', url, auth=app.config['BASIC_AUTH'])

    if response.status_code != 200:
        logger.error('Failed to retrieve party')
        raise ApiError(url, response.status_code)

    logger.debug('Successfully retrieved party')
    return json.loads(response.text)
