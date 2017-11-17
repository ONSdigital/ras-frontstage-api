import logging

from flask import Response
from flask import request
from flask_restplus import Resource, reqparse
from structlog import wrap_logger

from frontstage_api import auth, passwords_api
from frontstage_api.controllers import party_controller


logger = wrap_logger(logging.getLogger(__name__))

parser = reqparse.RequestParser()
parser.add_argument('token', location='args', required=True)


@passwords_api.route('/verify-password-token')
class VerifyPasswordToken(Resource):

    @staticmethod
    @auth.login_required
    @passwords_api.expect(parser)
    def get():
        logger.info('Attempting verify password token')
        token = request.args.get('token')

        party_controller.verify_token(token)
        logger.info('Successfully verified password token')

        return Response(status=200)
