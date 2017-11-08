import logging

from flask import Response
from flask import request
from flask_restplus import Resource
from structlog import wrap_logger

from frontstage_api import api, auth
from frontstage_api.controllers import party_controller


logger = wrap_logger(logging.getLogger(__name__))


@api.route('/change_password')
class ChangePassword(Resource):

    @staticmethod
    @auth.login_required
    def put():
        logger.info('Attempting to change user password')
        message_json = request.get_json()
        password = message_json.get('new_password')
        token = message_json.get('token')

        party_controller.change_password(password, token)
        logger.info('Successfully changed user password')

        return Response(status=200)
