import logging

from flask import jsonify, make_response, request
from flask_restplus import Resource
from structlog import wrap_logger

from frontstage_api import api
from frontstage_api.controllers import secure_messaging_controllers
from frontstage_api.decorators.jwt_decorators import get_jwt


logger = wrap_logger(logging.getLogger(__name__))


class GetMessagesList(Resource):
    method_decorators = [get_jwt(request)]

    @staticmethod
    def get(encoded_jwt):
        messages = secure_messaging_controllers.get_messages_list(encoded_jwt)
        total = secure_messaging_controllers.get_unread_message_total(encoded_jwt)
        messages_list = {**messages, **total}
        return make_response(jsonify(messages_list), 200)


api.add_resource(GetMessagesList, '/messages_list')
