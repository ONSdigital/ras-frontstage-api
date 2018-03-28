import json
import logging

from structlog import wrap_logger

from frontstage_api import app
from frontstage_api.common.request_handler import request_handler
from frontstage_api.exceptions.exceptions import ApiError


logger = wrap_logger(logging.getLogger(__name__))


def get_party_by_respondent_id(party_id):
    logger.debug('Retrieving party', party_id=party_id)
    url = app.config['RAS_PARTY_GET_BY_RESPONDENT_ID'].format(party_id)
    response = request_handler('GET', url, auth=app.config['BASIC_AUTH'])

    if response.status_code != 200:
        logger.error('Failed to retrieve party', party_id=party_id)
        raise ApiError(url=url, status_code=response.status_code)

    logger.debug('Successfully retrieved party', party_id=party_id)
    return json.loads(response.text)


def get_party_by_business_id(party_id, collection_exercise_id=None):
    logger.debug('Retrieving party', party_id=party_id)
    url = app.config['RAS_PARTY_GET_BY_BUSINESS_ID'].format(party_id)
    if collection_exercise_id:
        url += f"?collection_exercise_id={collection_exercise_id}&verbose=True"
    response = request_handler('GET', url, auth=app.config['BASIC_AUTH'])

    if response.status_code != 200:
        logger.error('Failed to retrieve party', party_id=party_id)
        raise ApiError(url=url, status_code=response.status_code)

    logger.debug('Successfully retrieved party', party_id=party_id)
    return json.loads(response.text)


def get_party_by_email(email):
    logger.debug('Retrieving party')
    url = app.config['RAS_PARTY_GET_BY_EMAIL_URL']
    response = request_handler('GET', url, json={"email": email}, auth=app.config['BASIC_AUTH'])

    if response.status_code != 200:
        logger.error('Failed to retrieve party')
        raise ApiError(url=url, status_code=response.status_code)

    logger.debug('Successfully retrieved party')
    return json.loads(response.text)


def verify_token(token):
    logger.debug('Verifying token party')
    url = app.config['RAS_PARTY_VERIFY_PASSWORD_TOKEN'].format(token)
    response = request_handler('GET', url, auth=app.config['BASIC_AUTH'])

    if response.status_code != 200:
        logger.error('Failed to verify token')
        raise ApiError(url=url, status_code=response.status_code)

    logger.debug('Successfully verified token')
    return json.loads(response.text)


def reset_password_request(username):
    logger.debug('Sending reset password request party')
    post_data = {"email_address": username}
    url = app.config['RAS_PARTY_RESET_PASSWORD_REQUEST'].format(username)
    response = request_handler('POST', url, auth=app.config['BASIC_AUTH'], json=post_data)

    if response.status_code != 200:
        logger.error('Failed to send reset password request party')
        raise ApiError(url=url, status_code=response.status_code)

    logger.debug('Successfully sent reset password request party')


def change_password(password, token):
    logger.debug('Changing password party')
    post_data = {"new_password": password}
    url = app.config['RAS_PARTY_CHANGE_PASSWORD'].format(token)
    response = request_handler('PUT', url, auth=app.config['BASIC_AUTH'], json=post_data)

    if response.status_code != 200:
        raise ApiError(url=url, status_code=response.status_code, description='Failed to change password party')

    logger.debug('Successfully changed password party')


def create_account(registration_data):
    logger.debug('Creating account')
    url = app.config['RAS_PARTY_POST_RESPONDENTS']
    registration_data['status'] = 'CREATED'
    response = request_handler('POST', url, auth=app.config['BASIC_AUTH'], json=registration_data)

    if response.status_code == 400:
        logger.debug('Email has already been used')
        raise ApiError(url=url, status_code=response.status_code)
    elif response.status_code != 200:
        logger.error('Failed to create account')
        raise ApiError(url=url, status_code=response.status_code)


def verify_email(token):
    logger.debug('Verifying email address', token=token)
    url = app.config['RAS_PARTY_VERIFY_EMAIL'].format(token)
    response = request_handler('PUT', url, auth=app.config['BASIC_AUTH'])

    if response.status_code != 200:
        logger.error('Failed to verify email address', token=token)
        raise ApiError(url=url, status_code=response.status_code)

    logger.debug('Successfully verified email address', token=token)


def add_survey(party_id, enrolment_code):
    logger.debug('Adding a survey')
    url = app.config['RAS_PARTY_ADD_SURVEY']
    request_json = {"party_id": party_id, "enrolment_code": enrolment_code}
    response = request_handler('POST', url, auth=app.config['BASIC_AUTH'], json=request_json)

    if response.status_code != 200:
        raise ApiError(url=url, status_code=response.status_code, description='Failed to add a survey')

    logger.debug('Successfully added a survey')
