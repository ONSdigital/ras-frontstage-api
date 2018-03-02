import logging

from flask import jsonify
from structlog import wrap_logger

from frontstage_api import app, api
from frontstage_api.exceptions.exceptions import (ApiError, InvalidCaseCategory, InvalidSurveyList,
                                                  InvalidRequestMethod, NoJWTError, NoSurveyPermission, FileTooLarge,
                                                  InvalidEqPayLoad)


logger = wrap_logger(logging.getLogger(__name__))


@app.errorhandler(ApiError)
@api.errorhandler(ApiError)
def api_error_method(error):
    error_json = {
        "error": {
            "url": error.url,
            "status_code": error.status_code,
            "data": error.data,
            "description": error.description
        }
    }
    status_code = error.status_code if error.status_code else 500
    if status_code == 500:
        logger.error(error.description, url=error.url, status=error.status_code, **error.kwargs)
    else:
        logger.info(error.description, url=error.url, status=error.status_code, **error.kwargs)
    return jsonify(error_json), status_code


@app.errorhandler(InvalidCaseCategory)
@api.errorhandler(InvalidCaseCategory)
def invalid_case_category(error):
    message_json = {
        'message': 'Invalid case category',
        'category': error.category
    }
    logger.error('Invalid case category', category=error.category)
    return message_json, 500


@app.errorhandler(InvalidSurveyList)
@api.errorhandler(InvalidSurveyList)
def invalid_survey_list(error):
    message_json = {
        'message': 'Invalid survey list name',
        'survey_list': error.survey_list
    }
    logger.info('Invalid survey list name', survey_list=error.survey_list)
    return message_json, 400


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


@app.errorhandler(NoSurveyPermission)
@api.errorhandler(NoSurveyPermission)
def no_survey_permission(error):
    message_json = {
        'message': 'Party does not have permission to access case',
        'party_id': error.party_id,
        'case_id': error.case_id,
        'case_party_id': error.case_party_id
    }
    logger.warning('Party does not have permission to access case', party_id=error.party_id, case_id=error.case_id)
    return message_json, 403


@app.errorhandler(InvalidEqPayLoad)
@api.errorhandler(InvalidEqPayLoad)
def invalid_eq_payload(error):
    logger.warning(error.error)
    return 'Unable to create eQ payload', 500


@app.errorhandler(NoJWTError)
@api.errorhandler(NoJWTError)
def no_jwt_in_header(error):  # NOQA # pylint: disable=unused-argument
    return {'message': 'No JWT provided in request header'}, 401


@app.errorhandler(FileTooLarge)
@api.errorhandler(FileTooLarge)
def file_too_large(error):
    logger.info('File submitted too large', case_id=error.case_id, party_id=error.party_id, file_size=error.file_size)
    error_json = {
        "error": {
            "data": {
                "message": "File too large"
            }
        }
    }
    return error_json, 400
