import logging

from flask import Response
from flask import request
from flask_restplus import Resource
from structlog import wrap_logger

from frontstage_api import api, auth
from frontstage_api.controllers import django_controller, party_controller


logger = wrap_logger(logging.getLogger(__name__))


@api.route('/request-password-change')
class RequestPasswordChange(Resource):

    @staticmethod
    @auth.login_required
    def post():
        logger.info('Attempting to retrieved user details for password change request')
        message_json = request.get_json()
        username = message_json.get('username')

        django_controller.check_account_valid(username)
        party_controller.reset_password_request(username)
        logger.info('Successfully sent password change request')

        return Response(status=200)
