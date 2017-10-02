import logging

import requests
from requests.exceptions import ConnectionError, ConnectTimeout
from structlog import wrap_logger

from frontstage_api.exceptions.exceptions import FailedRequest, InvalidRequestMethod


logger = wrap_logger(logging.getLogger(__name__))


def request_handler(method, url, headers=None, json=None):
    try:
        if method == 'GET':
            response = requests.get(url, headers=headers)
        elif method == 'POST':
            response = requests.post(url, headers=headers, json=json)
        elif method == 'PUT':
            response = requests.put(url, headers=headers, json=json)
        else:
            logger.error('Invalid request method', method=str(method), url=url)
            raise InvalidRequestMethod(method, url)
    except ConnectTimeout as e:
        logger.error('Connection to remote server timed out', method=method, url=url, exception=str(e))
        raise FailedRequest(method, url, e)
    except ConnectionError as e:
        logger.error('Failed to connect to external service', method=method, url=url, exception=str(e))
        raise FailedRequest(method, url, e)

    return response
