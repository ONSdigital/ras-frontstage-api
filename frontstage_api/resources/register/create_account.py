import logging

from flask import jsonify, make_response, request
from flask_restplus import Resource, fields
from structlog import wrap_logger

from frontstage_api import auth, register_api
from frontstage_api.controllers import iac_controller, party_controller


logger = wrap_logger(logging.getLogger(__name__))

registration_details = register_api.model('RegistrationDetails', {
    'enrolmentCode': fields.String(required=True),
    'status': fields.String(required=True)
})


@register_api.route('/create-account')
class CreateAccount(Resource):

    @staticmethod
    @auth.login_required
    @register_api.expect(registration_details, validate=True)
    def post():
        logger.info('Attempting to create account')
        registration_data = request.get_json()

        # Verify enrolment code is active
        iac = iac_controller.get_iac_from_enrolment(registration_data['enrolmentCode'])
        if not iac['active']:
            return make_response(jsonify(iac), 401)

        # Create account in party service
        party_controller.create_account(registration_data)

        logger.info('Successfully created account')
        return "OK", 201
