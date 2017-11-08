import json
import logging

from structlog import wrap_logger

from frontstage_api import app
from frontstage_api.common.request_handler import request_handler
from frontstage_api.exceptions.exceptions import ApiError, InvalidCaseCategory


logger = wrap_logger(logging.getLogger(__name__))


def get_case_by_party_id(party_id):
    logger.debug('Retrieving case', party_id=party_id)
    url = app.config['RM_CASE_GET_BY_PARTY'].format(party_id)
    response = request_handler('GET', url, auth=app.config['BASIC_AUTH'])

    if response.status_code != 200:
        logger.error('Failed to retrieve case', party_id=party_id)
        raise ApiError(url, response.status_code)

    logger.debug('Successfully retrieved case', party_id=party_id)
    return json.loads(response.text)


def get_case_by_enrolment_code(enrolment_code):
    logger.debug('Retrieving case', enrolment_code=enrolment_code)
    url = app.config['RM_CASE_GET_BY_IAC'].format(enrolment_code)
    response = request_handler('GET', url, auth=app.config['BASIC_AUTH'])

    if response.status_code != 200:
        logger.error('Failed to retrieve case', enrolment_code=enrolment_code)
        raise ApiError(url, response.status_code)

    logger.debug('Successfully retrieved case', enrolment_code=enrolment_code)
    return json.loads(response.text)


def get_case_categories():
    logger.debug('Retrieving case categories')
    url = app.config['RM_CASE_GET_CATEGORIES']
    response = request_handler('GET', url, auth=app.config['BASIC_AUTH'])

    if response.status_code != 200:
        logger.error('Failed to retrieve case categories')
        raise ApiError(url, response.status_code)

    logger.debug('Successfully retrieved case categories')
    return json.loads(response.text)


def validate_case_category(category):
    logger.debug('Validating case category', category=category)
    categories = get_case_categories()
    category_names = [cat['name'] for cat in categories]
    if category not in category_names:
        raise InvalidCaseCategory(category)


def post_case_event(case_id, party_id, category, description):
    logger.debug('Posting case event', case_id=case_id)
    validate_case_category(category)
    url = app.config['RM_CASE_POST_CASE_EVENT'].format(case_id)
    message = {
        'description': description,
        'category': category,
        'partyId': party_id,
        'createdBy': 'RAS_FRONTSTAGE_API'
    }
    response = request_handler('POST', url, auth=app.config['BASIC_AUTH'], json=message)

    if response.status_code != 201:
        logger.error('Failed to post to case service', case_id=case_id)
        raise ApiError(url, response.status_code)
    logger.debug('Successfully posted case event', case_id=case_id)
