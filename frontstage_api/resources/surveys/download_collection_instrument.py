import logging

from flask import request, Response
from flask_restplus import Resource, reqparse
from structlog import wrap_logger

from frontstage_api import api, auth
from frontstage_api.controllers import case_controller, collection_instrument_controller


logger = wrap_logger(logging.getLogger(__name__))

parser = reqparse.RequestParser()
parser.add_argument('case_id', location='args', required=True)
parser.add_argument('party_id', location='args', required=True)


@api.route('/download-ci')
class DownloadCollectionInstrument(Resource):

    @staticmethod
    @auth.login_required
    @api.expect(parser)
    def get():
        party_id = request.args['party_id']
        case_id = request.args['case_id']
        logger.info('Downloading collection instrument', case_id=case_id, party_id=party_id)

        # Check if respondent has permission to download for this case
        case = case_controller.get_case_by_case_id(case_id)
        case_controller.check_case_permissions(party_id, case['partyId'], case_id)

        collection_instrument, headers = collection_instrument_controller.download_collection_instrument(case['collectionInstrumentId'], case_id, party_id)

        logger.info('Successfully downloaded collection instrument', case_id=case_id, party_id=party_id)
        return Response(collection_instrument, headers=headers)
