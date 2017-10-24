import json
import logging

from structlog import wrap_logger

from frontstage_api import app
from frontstage_api.common.request_handler import request_handler
from frontstage_api.decorators.api_error_handler import api_error_handler
from frontstage_api.exceptions.exceptions import ApiError


logger = wrap_logger(logging.getLogger(__name__))


@api_error_handler
def get_case_by_party_id(party_id):
    logger.debug('Retrieving case', party_id=party_id)
    url = app.config['RM_CASE_GET_BY_PARTY'].format(party_id)
    response = request_handler('GET', url, auth=app.config['BASIC_AUTH'])

    if response.status_code == 204:
        logger.warning('No case found for party id', party_id=party_id)
        raise ApiError('FA200')
    elif response.status_code != 200:
        logger.error('Failed to retrieve case')
        raise ApiError('FA201')

    return json.loads(response.text)
