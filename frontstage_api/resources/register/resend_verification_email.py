import logging

from flask import request
from flask_restplus import Resource, reqparse
from structlog import wrap_logger

from frontstage_api import auth, register_api
from frontstage_api.controllers import party_controller


logger = wrap_logger(logging.getLogger(__name__))

parser = reqparse.RequestParser()
parser.add_argument('party_id', location='args', required=True)


@register_api.route('/resend-verification-email')
class ResendVerificationEmail(Resource):

    @staticmethod
    @auth.login_required
    @register_api.expect(parser)
    def post():
        party_id = request.args.get('party_id')
        logger.info('Attempting to resend verification email', party_id=party_id)

        # Verify email in party service with token
        party_controller.resend_verification_email(party_id)

        logger.info('Successfully resent verification email', party_id=party_id)
        return "OK", 200
