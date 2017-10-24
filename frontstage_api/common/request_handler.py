import logging

import requests
from requests.exceptions import ConnectionError
from structlog import wrap_logger

from frontstage_api.exceptions.exceptions import ApiError, InvalidRequestMethod


logger = wrap_logger(logging.getLogger(__name__))


def request_handler(method, url, auth=None, headers=None, json=None, error_code=None):
    try:
        if method == 'GET':
            response = requests.get(url, auth=auth, headers=headers)
        elif method == 'POST':
            response = requests.post(url, auth=auth, headers=headers, json=json)
        elif method == 'PUT':
            response = requests.put(url, auth=auth, headers=headers, json=json)
        else:
            logger.error('Invalid request method', method=str(method), url=url)
            raise InvalidRequestMethod(method, url)
    except ConnectionError as e:
        logger.error('Failed to connect to external service', method=method, url=url, exception=str(e))
        raise ApiError(error_code)

    return response
