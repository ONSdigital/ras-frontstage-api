import logging

from flask import jsonify, make_response, request
from flask_restplus import Resource, fields
from structlog import wrap_logger

from frontstage_api import auth, surveys_api
from frontstage_api.controllers import case_controller, iac_controller, party_controller


logger = wrap_logger(logging.getLogger(__name__))

validate_enrolment_details = surveys_api.model('ValidateAddSurveyDetails', {
    'party_id': fields.String(required=True),
    'enrolment_code': fields.String(required=True)
})


@surveys_api.route('/add-survey')
class AddSurvey(Resource):

    @staticmethod
    @auth.login_required
    @surveys_api.expect(validate_enrolment_details, validate=True)
    def post():
        logger.info('Attempting to add a survey')
        request_json = request.get_json(force=True)
        enrolment_code = request_json.get('enrolment_code')
        party_id = request_json.get('party_id')

        # Verify enrolment code is active
        iac = iac_controller.get_iac_from_enrolment(enrolment_code)
        if not iac['active']:
            return make_response(jsonify(iac), 401)

        case_id = iac['caseId']
        case = case_controller.get_case_by_enrolment_code(enrolment_code)
        case_group = case.get('caseGroup', {}).get('id')
        business_party_id = case['partyId']
        case_controller.post_case_event(case_id,
                                        party_id=business_party_id,
                                        category='ACCESS_CODE_AUTHENTICATION_ATTEMPT',
                                        description='Access code authentication attempted')

        party_controller.add_survey(party_id, enrolment_code)

        case_list = case_controller.get_case_by_party_id(party_id)
        case_id = get_case_id_for_group(case_list, case_group)

        logger.info('Successfully validated enrolment code')
        return {'case_id': case_id}


def get_case_id_for_group(case_list, case_group_id):
    if case_group_id:
        for case in case_list:
            if case_group_id == case.get('caseGroup', {}).get('id'):
                return case['id']
