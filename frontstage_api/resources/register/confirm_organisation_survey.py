import logging

from flask import jsonify, make_response, request
from flask_restplus import Resource
from structlog import wrap_logger

from frontstage_api import api, auth
from frontstage_api.controllers import case_controller, collection_exercise_controller, iac_controller, party_controller, survey_controller


logger = wrap_logger(logging.getLogger(__name__))


@api.route('/confirm-organisation-survey')
class ConfirmOrganisationSurvey(Resource):

    @staticmethod
    @auth.login_required
    def post():
        logger.info('Attempting to retrieve organisation and survey data')
        enrolment_code = request.get_json(force=True).get('enrolment_code')

        # Verify enrolment code is active
        iac = iac_controller.get_iac_from_enrolment(enrolment_code)
        if not iac['active']:
            return make_response(jsonify(iac), 401)

        # Get organisation name
        case = case_controller.get_case_by_enrolment_code(enrolment_code)
        business_party_id = case['caseGroup']['partyId']
        organisation_name = party_controller.get_party_by_business_id(business_party_id).get('name')

        # Get survey name
        collection_exercise_id = case['caseGroup']['collectionExerciseId']
        collection_exercise = collection_exercise_controller.get_collection_exercise(collection_exercise_id)
        survey_id = collection_exercise['surveyId']
        survey_name = survey_controller.get_survey(survey_id).get('longName')

        response_json = {
            "organisation_name": organisation_name,
            "survey_name": survey_name
        }
        logger.info('Successfully retrieved organisation and survey data')
        return make_response(jsonify(response_json), 200)
