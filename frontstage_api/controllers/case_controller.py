import json
import logging

import arrow
from structlog import wrap_logger

from frontstage_api import app
from frontstage_api.common.request_handler import request_handler
from frontstage_api.controllers import collection_exercise_controller, collection_instrument_controller, party_controller, survey_controller
from frontstage_api.exceptions.exceptions import ApiError, InvalidCaseCategory, NoSurveyPermission


logger = wrap_logger(logging.getLogger(__name__))


def get_case_by_case_id(case_id):
    logger.debug('Retrieving case', case_id=case_id)
    url = app.config['RM_CASE_GET_BY_ID'].format(case_id)
    response = request_handler('GET', url, auth=app.config['BASIC_AUTH'])

    if response.status_code != 200:
        logger.error('Failed to retrieve case', case_id=case_id)
        raise ApiError(url, response.status_code)

    logger.debug('Successfully retrieved case', case_id=case_id)
    return json.loads(response.text)


def get_case_by_party_id(party_id, case_events=False):
    logger.debug('Retrieving case', party_id=party_id)
    url = app.config['RM_CASE_GET_BY_PARTY'].format(party_id)
    if case_events:
        url = '{}?caseevents=true'.format(url)
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


def check_case_permissions(party_id, case_party_id, case_id=None):
    logger.debug('Party requesting access to case', party_id=party_id, case_id=case_id, case_party_id=case_party_id)
    if party_id != case_party_id:
        raise NoSurveyPermission(party_id, case_id, case_party_id)

    logger.debug('Party has permission to access case', party_id=party_id, case_id=case_id, case_party_id=case_party_id)


def build_full_case_data(case):
    logger.debug('Attempting to build case data', case_id=case['id'])
    collection_exercise_id = case["caseGroup"]["collectionExerciseId"]
    collection_exercise = collection_exercise_controller.get_collection_exercise(collection_exercise_id)
    collection_exercise_formatted = format_collection_exercise_dates(collection_exercise)

    business_party_id = case['caseGroup']['partyId']
    business_party = party_controller.get_party_by_business_id(business_party_id)
    survey_id = collection_exercise['surveyId']
    survey = survey_controller.get_survey(survey_id)
    collection_instrument_size = collection_instrument_controller.get_collection_instrument_size(case['collectionInstrumentId'])
    status = calculate_case_status(case)
    survey_data = {
        "case": case,
        "collection_exercise": collection_exercise_formatted,
        "business_party": business_party,
        "survey": survey,
        "collection_instrument_size": collection_instrument_size,
        'status': status
    }
    logger.debug('Successfully built case data', case_id=case['id'])
    return survey_data


def calculate_case_status(case):
    logger.debug('Getting the status of case')
    case_events = case.get('caseEvents')
    status = None
    if case_events:
        for event in case_events:
            if event['category'] == 'SUCCESSFUL_RESPONSE_UPLOAD':
                status = 'Complete'
                break
            elif event['category'] == 'COLLECTION_INSTRUMENT_DOWNLOADED':
                status = 'Downloaded'
    logger.debug('Retrieved the status of case', status=status)
    return status if status else 'Not Started'


def format_collection_exercise_dates(collection_exercise):
    logger.debug('Formatting collection exercise dates')
    input_date_format = 'YYYY-MM-DDThh:mm:ss'
    output_date_format = 'D MMM YYYY'
    for key in ['periodStartDateTime', 'periodEndDateTime', 'scheduledReturnDateTime']:
        collection_exercise[key] = collection_exercise[key].replace('Z', '')
        collection_exercise[key + 'Formatted'] = arrow.get(collection_exercise[key], input_date_format).format(output_date_format)
    logger.debug('Successfully formatted collection exercise dates')
    return collection_exercise