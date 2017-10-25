import logging

from flask import jsonify, make_response, request
from flask_restplus import Resource
from structlog import wrap_logger

from frontstage_api import api
from frontstage_api.controllers import secure_messaging_controllers
from frontstage_api.decorators.jwt_decorators import get_jwt


logger = wrap_logger(logging.getLogger(__name__))


@api.route('/message')
class GetMessageView(Resource):
    method_decorators = [get_jwt(request)]

    @staticmethod
    def get(encoded_jwt):
        message_id = request.args.get('message_id')
        label = request.args.get('label')
        party_id = request.args.get('party_id')

        message = secure_messaging_controllers.get_message(encoded_jwt, message_id, label)
        # If the message was returned with errors return the error message
        if message.get('error'):
            return make_response(jsonify(message), 200)

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
        # If the message was returned with errors return the error message
        if message.get('error'):
            make_response(jsonify(message), 200)

        remove_unread_label = secure_messaging_controllers.remove_unread_label(encoded_jwt, message_id) if label == 'UNREAD' else {}
        # Create json response
        response_json = {
            "message": message,
            "draft": draft
        }
        # If we failed to remove the unread label append error but don't fail request
        if remove_unread_label.get('error'):
            response_json = {**response_json, **remove_unread_label}

        return make_response(jsonify(response_json), 200)