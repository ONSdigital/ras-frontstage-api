import logging

from flask import jsonify, make_response, request
from flask_restplus import Resource, fields
from structlog import wrap_logger

from frontstage_api import api, auth
from frontstage_api.controllers import case_controller, iac_controller


logger = wrap_logger(logging.getLogger(__name__))

validate_enrolment_details = api.model('ValidateEnrolmentDetails', {
    'enrolment_code': fields.String(required=True),
    'initial': fields.Boolean(required=False)
})


@api.route('/validate-enrolment')
class ValidateEnrolment(Resource):

    @staticmethod
    @auth.login_required
    @api.expect(validate_enrolment_details, validate=True)
    def post():
        logger.info('Attempting to validate enrolment code')
        request_json = request.get_json(force=True)
        enrolment_code = request_json.get('enrolment_code')
        initial_submission = request_json.get('initial')

        # Verify enrolment code is active
        iac = iac_controller.get_iac_from_enrolment(enrolment_code)
        if not iac['active']:
            return make_response(jsonify(iac), 401)

        # If this is the initial submission of enrolment code post a case event for authentication attempt
        if initial_submission:
            case_id = iac['caseId']
            case = case_controller.get_case_by_enrolment_code(enrolment_code)
            business_party_id = case['partyId']
            case_controller.post_case_event(case_id,
                                            party_id=business_party_id,
                                            category='ACCESS_CODE_AUTHENTICATION_ATTEMPT',
                                            description='Access code authentication attempted')

        logger.info('Successfully validated enrolment code')
        return "OK", 200
