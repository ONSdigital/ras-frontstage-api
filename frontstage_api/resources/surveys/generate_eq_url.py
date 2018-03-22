import logging

from flask import request, current_app
from flask_restplus import Resource, reqparse
from structlog import wrap_logger

from frontstage_api import auth, surveys_api
from frontstage_api.controllers import case_controller
from frontstage_api.controllers.encrypter import Encrypter
from frontstage_api.controllers.eq_payload import EqPayload

logger = wrap_logger(logging.getLogger(__name__))

parser = reqparse.RequestParser()
parser.add_argument('case_id', location='args', required=True)
parser.add_argument('party_id', location='args', required=True)


@surveys_api.route('/generate-eq-url')
class GenerateEqUrl(Resource):

    @staticmethod
    @auth.login_required
    @surveys_api.expect(parser)
    def get():
        """
        Generate EQ URL with JWT by creating payload from services and then encrypting.
        :return EQ URL
        """
        case_id = request.args['case_id']
        party_id = request.args['party_id']
        logger.info('Generating EQ URL', case_id=case_id, party_id=party_id)

        case = case_controller.get_case_by_case_id(case_id)
        case_controller.check_case_permissions(party_id, case['partyId'], case_id=case_id)

        payload = EqPayload().create_payload(case)

        json_secret_keys = current_app.config['JSON_SECRET_KEYS']
        encrypter = Encrypter(json_secret_keys)
        token = encrypter.encrypt(payload)

        eq_url = current_app.config['EQ_URL']+token

        category = 'EQ_LAUNCH'
        case_controller.post_case_event(case_id,
                                        party_id=party_id,
                                        category=category,
                                        description='Instrument {} launched by {} for case {}'.format(
                                            case['collectionInstrumentId'], party_id, case_id))

        return {"eq_url": eq_url}
