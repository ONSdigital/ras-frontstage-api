import logging

from flask import jsonify
from structlog import wrap_logger

from frontstage_api import api, app
from frontstage_api.exceptions.exceptions import ApiError, InvalidRequestMethod, NoJWTError


logger = wrap_logger(logging.getLogger(__name__))


@app.errorhandler(ApiError)
@api.errorhandler(ApiError)
def api_error_method(error):
    error_json = {
        "error": {
            "url": error.url,
            "status_code": error.status_code,
            "data": error.data
        }
    }
    logger.error('Error during api call', url=error.url, status_code=error.status_code)
    return jsonify(error_json), 502


@app.errorhandler(InvalidRequestMethod)
@api.errorhandler(InvalidRequestMethod)
def invalid_request_method(error):
    message_json = {
        'message': 'Invalid request method',
        'method': error.method,
        'url': error.url
    }
    logger.error('Invalid request method', method=error.method, url=error.url)
    return message_json, 500


@app.errorhandler(NoJWTError)
@api.errorhandler(NoJWTError)
def no_jwt_in_header(error):  # NOQA # pylint: disable=unused-argument
    return {'message': 'No JWT provided in request header'}, 401
