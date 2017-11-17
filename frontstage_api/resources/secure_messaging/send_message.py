import logging

from flask import jsonify, make_response, request
from flask_restplus import fields, Resource
from structlog import wrap_logger

from frontstage_api import auth, secure_messaging_api
from frontstage_api.controllers import case_controller, party_controller, secure_messaging_controllers
from frontstage_api.decorators.jwt_decorators import get_jwt


logger = wrap_logger(logging.getLogger(__name__))

message_details = secure_messaging_api.model('MessageDetails', {
        'msg_from': fields.String(required=True),
        'subject': fields.String(required=True),
        'body': fields.String(required=True),
        'thread_id': fields.String(),
})


@secure_messaging_api.route('/send-message')
class SendMessage(Resource):
    method_decorators = [get_jwt(request)]

    @staticmethod
    @auth.login_required
    @secure_messaging_api.expect(message_details, validate=True)
    @secure_messaging_api.header('jwt', 'JWT to pass to secure messaging service', required=True)
    def post(encoded_jwt):
        message_json = request.get_json(force=True)
        party_id = message_json['msg_from']
        is_draft = request.args.get('is_draft')
        logger.info('Attempting to send message', party_id=party_id)

        # Retrieving business party, case and survey id's
        party = party_controller.get_party_by_respondent_id(party_id)
        associations = party.get('associations')
        if associations:
            business_party_id = associations[0].get('partyId')
            survey_id = associations[0].get('enrolments')[0].get('surveyId')
        case = case_controller.get_case_by_party_id(party_id)
        case_id = case[0].get('id')

        # Creating message json block to send to secure messaging
        message_json = {
            **message_json,
            'msg_to': ['BRES'],
            'msg_from': party_id,
            'collection_case': case_id,
            'ru_id': business_party_id,
            'survey': survey_id
        }

        if is_draft == 'False':
            message = secure_messaging_controllers.send_message(encoded_jwt, message_json)
        else:
            message = secure_messaging_controllers.save_draft(encoded_jwt, message_json)

        # If the form was submitted with errors and is part of an existing thread, return the last message from thread
        if message.get('form_errors'):
            if message_json.get('thread_id'):
                thread_message = secure_messaging_controllers.get_thread_message(encoded_jwt, message_json['thread_id'], party_id)
                message = {**message, "thread_message": thread_message}
            message = {
                'error': {
                    'data': message
                }
            }
            return make_response(jsonify(message), 400)

        logger.info('Successfully sent message', party_id=party_id, message_id=message['msg_id'])
        return make_response(jsonify(message), 200)
