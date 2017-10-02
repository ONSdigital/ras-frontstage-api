import logging

from flask import jsonify, make_response
from structlog import wrap_logger

from frontstage_api import app
from frontstage_api.exceptions.exceptions import FailedRequest, InvalidRequestMethod, NoJWTError, UnexpectedStatusCode


logger = wrap_logger(logging.getLogger(__name__))


@app.errorhandler(FailedRequest)
def failed_request(error):
    message_json = {
        'message': 'External request failed',
        'url': error.url,
        'method': error.method,
        'exception': error.exception
    }
    return make_response(jsonify(message_json), 500)


@app.errorhandler(InvalidRequestMethod)
def failed_request(error):
    message_json = {
        'message': 'Invalid request method',
        'method': error.method,
        'url': error.url
    }
    logger.error('Invalid request method', method=error.method, url=error.url)
    return make_response(jsonify(message_json), 500)


@app.errorhandler(NoJWTError)
def no_jwt_in_header(error):  # pylint: disable=unused-argument
    return make_response(jsonify({'message': 'No JWT provided in request header'}), 401)


@app.errorhandler(UnexpectedStatusCode)
def unexpected_status_code(error):
    message_json = {
        'message': 'Unexpected status code received from service',
        'method': error.method,
        'url': error.url,
        'status_code': error.status_code,
        'content': error.content
    }
    logger.error('Unexpected status code returned from service', method=error.method, url=error.url, status_code=error.status_code)
    return make_response(jsonify(message_json), error.status_code)
