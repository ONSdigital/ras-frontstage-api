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
        unread_messages_total = secure_messaging_controllers.get_unread_message_total(encoded_jwt)
        messages_list = {**messages, **unread_messages_total}
        return make_response(jsonify(messages_list), 200)


class GetMessageView(Resource):
    method_decorators = [get_jwt(request)]

    @staticmethod
    def get(encoded_jwt):
        message_id = request.args.get('message_id')
        label = request.args.get('label')
        party_id = request.args.get('party_id')

        message = secure_messaging_controllers.get_message(encoded_jwt, message_id, label)

        # If message is a draft also return the last message from the thread if it exists
        if label == 'DRAFT':
            draft = message
            thread_id = draft.get('thread_id')
            if thread_id != draft['msg_id']:
                message = secure_messaging_controllers.get_thread_message(encoded_jwt, thread_id, party_id)
            else:
                message = {}
        else:
            draft = {}

        response_json = {
            "message": message,
            "draft": draft
        }
        return make_response(jsonify(response_json), 200)


api.add_resource(GetMessagesList, '/messages_list')
api.add_resource(GetMessageView, '/message')
