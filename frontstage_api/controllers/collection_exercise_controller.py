import json
import logging

from structlog import wrap_logger

from frontstage_api import app
from frontstage_api.common.request_handler import request_handler
from frontstage_api.exceptions.exceptions import ApiError


logger = wrap_logger(logging.getLogger(__name__))


def get_collection_exercise(collection_exercise_id):
    logger.debug('Retrieving collection exercise', collection_exercise_id=collection_exercise_id)
    url = app.config['RM_COLLECTION_EXERCISE_GET'].format(collection_exercise_id)
    response = request_handler('GET', url, auth=app.config['BASIC_AUTH'])

    if response.status_code != 200:
        raise ApiError(url=url, status_code=response.status_code,
                       description='Failed to retrieve collection exercise',
                       collection_exercise_id=collection_exercise_id)

    logger.debug('Successfully retrieved collection exercise', collection_exercise_id=collection_exercise_id)
    return json.loads(response.text)


def get_collection_exercise_events(collection_exercise_id):
    logger.debug('Retrieving collection exercise events', collection_exercise_id=collection_exercise_id)
    url = app.config['RM_COLLECTION_EXERCISE_EVENTS'].format(collection_exercise_id)
    response = request_handler('GET', url, auth=app.config['BASIC_AUTH'])

    if response.status_code != 200:
        raise ApiError(url=url, status_code=response.status_code,
                       description='Failed to retrieve collection exercise events',
                       collection_exercise_id=collection_exercise_id)

    logger.debug('Successfully retrieved collection exercise events', collection_exercise_id=collection_exercise_id)
    return json.loads(response.text)
