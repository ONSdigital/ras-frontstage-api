import logging

from flask import Response
from flask import request
from flask_restplus import Resource
from structlog import wrap_logger

from frontstage_api import api, auth
from frontstage_api.controllers import party_controller


logger = wrap_logger(logging.getLogger(__name__))


@api.route('/verify-password-token')
class VerifyPasswordToken(Resource):

    @staticmethod
    @auth.login_required
    def get():
        logger.info('Attempting verify password token')
        token = request.args.get('token')

        party_controller.verify_token(token)
        logger.info('Successfully verified password token')

        return Response(status=200)
