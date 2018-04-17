import json
import logging

from structlog import wrap_logger

from frontstage_api import app
from frontstage_api.common.request_handler import request_handler
from frontstage_api.exceptions.exceptions import ApiError


logger = wrap_logger(logging.getLogger(__name__))


def get_iac_from_enrolment(enrolment_code):
    logger.debug('Retrieving IAC', enrolment_code=enrolment_code)
    url = f"{app.config['RM_IAC_SERVICE']}/iacs/{enrolment_code}"
    response = request_handler('GET', url, auth=app.config['BASIC_AUTH'])

    if response.status_code == 404:
        raise ApiError(url=url, status_code=response.status_code, description='IAC not found', enrolment_code=enrolment_code)
    if response.status_code != 200:
        raise ApiError(url=url, status_code=response.status_code, description='Failed to retrieve IAC', enrolment_code=enrolment_code)

    logger.debug('Successfully retrieved IAC', enrolment_code=enrolment_code)
    return json.loads(response.text)
