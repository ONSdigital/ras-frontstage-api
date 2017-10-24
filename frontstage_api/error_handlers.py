import logging

from structlog import wrap_logger

from frontstage_api import api
from frontstage_api.exceptions.exceptions import InvalidRequestMethod, NoJWTError


logger = wrap_logger(logging.getLogger(__name__))


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
