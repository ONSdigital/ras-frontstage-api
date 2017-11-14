import logging

from flask import request
from flask_restplus import Resource, reqparse
from structlog import wrap_logger

from frontstage_api import api, auth
from frontstage_api.controllers import case_controller


logger = wrap_logger(logging.getLogger(__name__))

parser = reqparse.RequestParser()
parser.add_argument('case_id', location='args', required=True)
parser.add_argument('party_id', location='args', required=True)


@api.route('/access-case')
class GetAccessCase(Resource):

    @staticmethod
    @auth.login_required
    @api.expect(parser)
    def get():
        case_id = request.args['case_id']
        party_id = request.args['party_id']
        logger.info('Attempting to retrieve detailed case data', case_id=case_id, party_id=party_id)

        # Check if respondent has permission to see case data
        case = case_controller.get_case_by_case_id(case_id)
        case_controller.check_case_permissions(party_id, case['partyId'], case_id=case_id)

        full_case_data = case_controller.build_full_case_data(case)

        logger.info('Successfully retrieved all data relating to case', case_id=case_id, party_id=party_id)
        return full_case_data
