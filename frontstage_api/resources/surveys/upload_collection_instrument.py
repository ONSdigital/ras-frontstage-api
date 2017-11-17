import logging

from flask import request, Response
from flask_restplus import Resource, reqparse
from structlog import wrap_logger

from frontstage_api import app, auth, surveys_api
from frontstage_api.controllers import case_controller, collection_instrument_controller
from frontstage_api.exceptions.exceptions import FileTooLarge

logger = wrap_logger(logging.getLogger(__name__))

parser = reqparse.RequestParser()
parser.add_argument('case_id', location='args', required=True)
parser.add_argument('party_id', location='args', required=True)
parser.add_argument('file', location='files', required=True)


@surveys_api.route('/upload-ci')
class UploadCollectionInstrument(Resource):

    @staticmethod
    @auth.login_required
    @surveys_api.expect(parser)
    def post():
        case_id = request.args['case_id']
        party_id = request.args['party_id']
        logger.info('Attempting to upload collection instrument', case_id=case_id, party_id=party_id)

        if request.content_length > app.config['MAX_UPLOAD_LENGTH']:
            raise FileTooLarge(case_id, party_id)

        # Check if respondent has permission to upload for this case
        case = case_controller.get_case_by_case_id(case_id)
        case_controller.check_case_permissions(party_id, case['partyId'], case_id)

        upload_file = request.files['file']
        upload_filename = upload_file.filename
        upload_file = {'file': (upload_filename, upload_file.stream, upload_file.mimetype, {'Expires': 0})}

        collection_instrument_controller.upload_collection_instrument(upload_file, case_id, party_id)

        logger.info('Successfully uploaded collection instrument', case_id=case_id, party_id=party_id)
        return Response(status=200)
