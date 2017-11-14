import logging

from flask import jsonify, make_response, request
from flask_restplus import reqparse, Resource
from structlog import wrap_logger

from frontstage_api import api, auth
from frontstage_api.controllers import secure_messaging_controllers
from frontstage_api.decorators.jwt_decorators import get_jwt


logger = wrap_logger(logging.getLogger(__name__))

parser = reqparse.RequestParser()
parser.add_argument('label', location='args', required=True)


@api.route('/messages-list')
class GetMessagesList(Resource):
    method_decorators = [get_jwt(request)]

    @staticmethod
    @auth.login_required
    @api.expect(parser)
    @api.header('jwt', 'JWT to pass to secure messaging service', required=True)
    def get(encoded_jwt):
        label = request.args.get('label')
        logger.info('Attempting to retrieve message list', label=label)

        messages = secure_messaging_controllers.get_messages_list(encoded_jwt, label)
        unread_message_total = secure_messaging_controllers.get_unread_message_total(encoded_jwt)
        messages = {**messages, **unread_message_total}

        logger.info('Successfully retrieved message list', label=label)
        return make_response(jsonify(messages), 200)
