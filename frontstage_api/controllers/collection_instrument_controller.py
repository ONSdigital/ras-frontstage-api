import logging

from structlog import wrap_logger

from frontstage_api import app
from frontstage_api.common.request_handler import request_handler
from frontstage_api.controllers import case_controller
from frontstage_api.exceptions.exceptions import ApiError


logger = wrap_logger(logging.getLogger(__name__))


def get_collection_instrument_size(collection_instrument_id):
    logger.debug('Retrieving collection instrument size', collection_instrument_id=collection_instrument_id)
    url = app.config['RAS_CI_SIZE'].format(collection_instrument_id)
    response = request_handler('GET', url, auth=app.config['BASIC_AUTH'], fail=False)

    if response.status_code != 200:
        logger.error('Failed to retrieve collection instrument size', collection_instrument_id=collection_instrument_id)
        return 0
    collection_instrument_size = response.json().get('size')

    logger.debug('Successfully retrieved collection instrument size', collection_instrument_id=collection_instrument_id)
    return collection_instrument_size


def download_collection_instrument(collection_instrument_id, case_id, party_id):
    logger.debug('Downloading collection instrument', collection_instrument_id=collection_instrument_id)
    url = app.config['RAS_CI_DOWNLOAD'].format(collection_instrument_id)
    response = request_handler('GET', url, auth=app.config['BASIC_AUTH'], fail=False)

    # Post relevant download case event
    category = 'COLLECTION_INSTRUMENT_DOWNLOADED' if response.status_code == 200 else 'COLLECTION_INSTRUMENT_ERROR'
    case_controller.post_case_event(case_id,
                                    party_id=party_id,
                                    category=category,
                                    description='Instrument {} downloaded by {} for case {}'.format(collection_instrument_id, party_id, case_id))

    if response.status_code != 200:
        logger.error('Failed to download collection instrument', collection_instrument_id=collection_instrument_id)
        raise ApiError(url, response.status_code)

    logger.debug('Successfully downloaded collection instrument', collection_instrument_id=collection_instrument_id)
    return response.content, response.headers.items()


def upload_collection_instrument(upload_file, case_id, party_id):
    logger.info('Attempting to upload collection instrument', case_id=case_id)
    url = app.config['RAS_CI_UPLOAD'].format(case_id)
    response = request_handler('POST', url, auth=app.config['BASIC_AUTH'], files=upload_file, fail=False)

    # Post relevant upload case event
    category = 'SUCCESSFUL_RESPONSE_UPLOAD' if response.status_code == 200 else 'UNSUCCESSFUL_RESPONSE_UPLOAD'
    case_controller.post_case_event(case_id,
                                    party_id=party_id,
                                    category=category,
                                    description='Survey response for case {} uploaded by {}'.format(case_id, party_id))

    if response.status_code == 400:
        logger.debug('Invalid file uploaded', case_id=case_id)
        data = {
            'message': response.text
        }
        raise ApiError(url, response.status_code, data)

    if response.status_code != 200:
        logger.error('Failed to upload collection instrument', case_id=case_id)
        raise ApiError(url, response.status_code)

    logger.debug('Successfully uploaded collection instrument', case_id=case_id)