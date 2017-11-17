import logging

from flask import jsonify, make_response, request
from flask_restplus import fields, Resource
from structlog import wrap_logger

from frontstage_api import auth, sign_in_api
from frontstage_api.controllers import django_controller, party_controller


logger = wrap_logger(logging.getLogger(__name__))

sign_in_details = sign_in_api.model('SignInDetails', {
        'username': fields.String(required=True, description='username'),
        'password': fields.String(required=True, description='password')
})


@sign_in_api.route('/')
class SignIn(Resource):

    @staticmethod
    @auth.login_required
    @sign_in_api.expect(sign_in_details, validate=True)
    def post():
        logger.info('Attempting to retrieved sign-in details')
        message_json = request.get_json(force=True)
        username = message_json['username']
        password = message_json['password']

        oauth2_token = django_controller.sign_in(username, password)
        party_id = party_controller.get_party_by_email(username).get('id')

        response_json = {**oauth2_token, "party_id": party_id}
        logger.info('Successfully retrieved sign-in details')
        return make_response(jsonify(response_json), 200)
