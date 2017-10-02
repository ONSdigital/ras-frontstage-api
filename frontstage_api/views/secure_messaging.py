import logging

from flask import Blueprint, jsonify, make_response, request
from structlog import wrap_logger

from frontstage_api import app
from frontstage_api.controllers import secure_messaging_controllers
from frontstage_api.decorators.jwt_decorators import get_jwt


logger = wrap_logger(logging.getLogger(__name__))

secure_message_bp = Blueprint('secure_message_bp', __name__, static_folder='static', template_folder='templates')


@app.route('/messages_list', methods=['GET'])
@get_jwt(request)
def get_message_list(encoded_jwt):
    messages = secure_messaging_controllers.get_messages_list(encoded_jwt)
    return make_response(jsonify(messages), 200)


@app.route('/unread_message_total', methods=['GET'])
@get_jwt(request)
def get_unread_message_total(encoded_jwt):
    total = secure_messaging_controllers.get_unread_message_total(encoded_jwt)
    return make_response(jsonify(total), 200)


