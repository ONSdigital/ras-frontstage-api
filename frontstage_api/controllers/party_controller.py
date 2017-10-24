import json
import logging

from structlog import wrap_logger

from frontstage_api import app
from frontstage_api.common.request_handler import request_handler
from frontstage_api.decorators.api_error_handler import api_error_handler
from frontstage_api.exceptions.exceptions import ApiError


logger = wrap_logger(logging.getLogger(__name__))


@api_error_handler
def get_party_by_respondent_id(party_id):
    logger.debug('Retrieving party', party_id=party_id)
    url = app.config['PARTY_BY_RESPONDENT_ID'].format(party_id)
    response = request_handler('GET', url, auth=app.config['BASIC_AUTH'])

    if response.status_code == 404:
        logger.warning('No respondent found for party id', party_id=party_id)
        raise ApiError('FA100')
    elif response.status_code != 200:
        logger.error('Failed to retrieve party')
        raise ApiError('FA101')

    return json.loads(response.text)
