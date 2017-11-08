import json
import logging

from structlog import wrap_logger

from frontstage_api import app
from frontstage_api.common.request_handler import request_handler
from frontstage_api.exceptions.exceptions import ApiError


logger = wrap_logger(logging.getLogger(__name__))


def get_survey(survey_id):
    logger.debug('Retrieving survey', survey_id=survey_id)
    url = app.config['RM_SURVEY_GET'].format(survey_id)
    response = request_handler('GET', url, auth=app.config['BASIC_AUTH'])

    if response.status_code != 200:
        logger.error('Failed to retrieve survey', survey_id=survey_id)
        raise ApiError(url, response.status_code)

    logger.debug('Successfully retrieved survey', survey_id=survey_id)
    return json.loads(response.text)
