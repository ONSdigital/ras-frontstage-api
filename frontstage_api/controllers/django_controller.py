import json
import logging

from structlog import wrap_logger

from frontstage_api import app
from frontstage_api.common.request_handler import request_handler
from frontstage_api.exceptions.exceptions import ApiError


logger = wrap_logger(logging.getLogger(__name__))


def sign_in(username, password):
    logger.debug('Attempting to retrieve OAuth2 token for sign-in')
    url = app.config['OAUTH_TOKEN_URL']
    data = {
        'grant_type': 'password',
        'client_id': app.config['DJANGO_CLIENT_ID'],
        'client_secret': app.config['DJANGO_CLIENT_SECRET'],
        'username': username,
        'password': password,
    }
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
    }
    response = request_handler('POST', url, headers=headers, auth=app.config['DJANGO_BASIC_AUTH'], data=data)

    if response.status_code == 401:
        oauth2_error = json.loads(response.text)
        raise ApiError(url=url, status_code=response.status_code, data=oauth2_error, description='Authentication error in oauth2 service')
    elif response.status_code != 201:
        raise ApiError(url=url, status_code=response.status_code, description='Failed to retrieve OAuth2 token')

    oauth2_token = json.loads(response.text)
    logger.debug('Successfully retrieved OAuth2 token')
    return oauth2_token


def check_account_valid(username):
    logger.debug('Attempting to check if account is valid in OAuth2')
    url = app.config['OAUTH_TOKEN_URL']
    data = {
        'grant_type': 'reset_password',
        'client_id': app.config['DJANGO_CLIENT_ID'],
        'client_secret': app.config['DJANGO_CLIENT_SECRET'],
        'username': username,
    }
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
    }

    response = request_handler('POST', url, headers=headers, auth=app.config['DJANGO_BASIC_AUTH'], data=data)

    if response.status_code == 401:
        oauth2_error = json.loads(response.text)
        raise ApiError(url=url, status_code=response.status_code, data=oauth2_error, description='Authentication error in oauth2 service')
    elif response.status_code != 201:
        raise ApiError(url=url, status_code=response.status_code, description='Failed to retrieve OAuth2 token')

    logger.debug('Successfully checked account state, account is valid')
