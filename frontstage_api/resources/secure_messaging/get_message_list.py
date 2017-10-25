import logging

from flask import jsonify, make_response, request
from flask_restplus import Resource
from structlog import wrap_logger

from frontstage_api import api
from frontstage_api.controllers import secure_messaging_controllers
from frontstage_api.decorators.jwt_decorators import get_jwt


logger = wrap_logger(logging.getLogger(__name__))


@api.route('/messages_list')
class GetMessagesList(Resource):
    method_decorators = [get_jwt(request)]

    @staticmethod
    def get(encoded_jwt):
        label = request.args.get('label')

        messages = secure_messaging_controllers.get_messages_list(encoded_jwt, label)
        # If the messages were returned with errors return the error message
        if messages.get('error'):
            return make_response(jsonify(messages), 200)

        unread_message_total = secure_messaging_controllers.get_unread_message_total(encoded_jwt)
        messages = {**messages, **unread_message_total}

        return make_response(jsonify(messages), 200)
