import logging

from flask import jsonify, make_response, request
from flask_restplus import Resource
from structlog import wrap_logger

from frontstage_api import api
from frontstage_api.controllers import django_controller, party_controller


logger = wrap_logger(logging.getLogger(__name__))


@api.route('/sign-in')
class SignIn(Resource):

    @staticmethod
    def post():
        message_json = request.get_json(force=True)
        username = message_json['username']
        password = message_json['password']

        oauth2_token = django_controller.sign_in(username, password)
        party_id = party_controller.get_party_by_email(username).get('id')

        response_json = {**oauth2_token, "party_id": party_id}

        return make_response(jsonify(response_json), 200)
