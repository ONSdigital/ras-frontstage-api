import logging

from structlog import wrap_logger

from frontstage_api import app
from frontstage_api.common.request_handler import request_handler
from frontstage_api.controllers import case_controller
from frontstage_api.exceptions.exceptions import ApiError


logger = wrap_logger(logging.getLogger(__name__))


def get_collection_instrument(collection_instrument_id):
    logger.debug('Retrieving collection instrument',
                 collection_instrument_id=collection_instrument_id)
    url = app.config['RAS_CI_DETAILS'].format(collection_instrument_id)
    response = request_handler('GET', url, auth=app.config['BASIC_AUTH'])

    if response.status_code != 200:
        raise ApiError(url=url, status_code=response.status_code,
                       description='Failed to retrieve collection instrument',
                       collection_instrument_id=collection_instrument_id)
    return response.json()


def download_collection_instrument(collection_instrument_id, case_id, party_id):
    logger.debug('Downloading collection instrument', collection_instrument_id=collection_instrument_id)
    url = app.config['RAS_CI_DOWNLOAD'].format(collection_instrument_id)
    response = request_handler('GET', url, auth=app.config['BASIC_AUTH'])

    # Post relevant download case event
    category = 'COLLECTION_INSTRUMENT_DOWNLOADED' if response.status_code == 200 else 'COLLECTION_INSTRUMENT_ERROR'
    case_controller.post_case_event(case_id,
                                    party_id=party_id,
                                    category=category,
                                    description=f'Instrument {collection_instrument_id} downloaded by {party_id} for case {case_id}')

    if response.status_code != 200:
        raise ApiError(url=url, status_code=response.status_code,
                       description='Failed to download collection instrument',
                       collection_instrument_id=collection_instrument_id)

    logger.debug('Successfully downloaded collection instrument', collection_instrument_id=collection_instrument_id)
    return response.content, response.headers.items()


def upload_collection_instrument(upload_file, case_id, party_id):
    logger.info('Attempting to upload collection instrument', case_id=case_id)
    url = app.config['RAS_CI_UPLOAD'].format(case_id)
    response = request_handler('POST', url, auth=app.config['BASIC_AUTH'], files=upload_file)

    # Post relevant upload case event
    category = 'SUCCESSFUL_RESPONSE_UPLOAD' if response.status_code == 200 else 'UNSUCCESSFUL_RESPONSE_UPLOAD'
    case_controller.post_case_event(case_id,
                                    party_id=party_id,
                                    category=category,
                                    description=f'Survey response for case {case_id} uploaded by {party_id}')

    if response.status_code == 400:
        data = {
            'message': response.text
        }
        raise ApiError(url=url, status_code=response.status_code, data=data, description='Invalid file uploaded',
                       case_id=case_id)

    if response.status_code != 200:
        raise ApiError(url=url, status_code=response.status_code, description='Failed to upload collection instrument',
                       case_id=case_id)

    logger.debug('Successfully uploaded collection instrument', case_id=case_id)
