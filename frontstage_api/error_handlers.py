import logging

from structlog import wrap_logger

from frontstage_api import api
from frontstage_api.exceptions.exceptions import FailedRequest, InvalidRequestMethod, NoJWTError, UnexpectedStatusCode


logger = wrap_logger(logging.getLogger(__name__))


@api.errorhandler(FailedRequest)
def failed_request(error):
    message_json = {
        'message': 'External request failed',
        'url': error.url,
        'method': error.method,
        'exception': error.exception
    }
    return message_json, 500


@api.errorhandler(InvalidRequestMethod)
def invalid_request_method(error):
    message_json = {
        'message': 'Invalid request method',
        'method': error.method,
        'url': error.url
    }
    logger.error('Invalid request method', method=error.method, url=error.url)
    return message_json, 500


@api.errorhandler(NoJWTError)
def no_jwt_in_header(error):  # NOQA # pylint: disable=unused-argument
    return {'message': 'No JWT provided in request header'}, 401


@api.errorhandler(UnexpectedStatusCode)
def unexpected_status_code(error):
    message_json = {
        'message': 'Unexpected status code received from service',
        'method': error.method,
        'url': error.url,
        'status_code': error.status_code,
        'content': error.content
    }
    logger.error('Unexpected status code returned from service', method=error.method, url=error.url, status_code=error.status_code)
    return message_json, error.status_code
