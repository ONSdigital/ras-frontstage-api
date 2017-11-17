import logging

from flask import request
from flask_restplus import Resource, reqparse
from structlog import wrap_logger

from frontstage_api import auth, register_api
from frontstage_api.controllers import party_controller


logger = wrap_logger(logging.getLogger(__name__))

parser = reqparse.RequestParser()
parser.add_argument('token', location='args', required=True)


@register_api.route('/verify-email')
class VerifyEmail(Resource):

    @staticmethod
    @auth.login_required
    @register_api.expect(parser)
    def put():
        token = request.args.get('token')
        logger.info('Attempting to verify email', token=token)

        # Verify email in party service with token
        party_controller.verify_email(token)

        logger.info('Successfully verified email', token=token)
        return "OK", 200
