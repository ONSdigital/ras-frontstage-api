import logging

from flask import request
from flask_restplus import Resource
from structlog import wrap_logger

from frontstage_api import api, auth
from frontstage_api.controllers import party_controller


logger = wrap_logger(logging.getLogger(__name__))


@api.route('/verify-email')
class VerifyEmail(Resource):

    @staticmethod
    @auth.login_required
    def put():
        token = request.args.get('token')
        logger.info('Attempting to verify email', token=token)

        # Verify email in party service with token
        party_controller.verify_email(token)

        logger.info('Successfully verified email', token=token)
        return "OK", 200
