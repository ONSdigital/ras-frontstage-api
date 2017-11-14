import logging

from flask import request
from flask_restplus import Resource
from structlog import wrap_logger

from frontstage_api import api, auth
from frontstage_api.controllers import case_controller
from frontstage_api.exceptions.exceptions import InvalidSurveyList


logger = wrap_logger(logging.getLogger(__name__))


@api.route('/surveys-list')
class GetSurveysList(Resource):

    @staticmethod
    @auth.login_required
    def get():
        party_id = request.args['party_id']
        survey_list = request.args['list']
        logger.info('Attempting to retrieve surveys list', party_id=party_id, survey_list=survey_list)

        cases = case_controller.get_case_by_party_id(party_id, case_events=True)
        # Filter out the cases relevant to the request
        if survey_list == 'todo':
            filtered_cases = [case for case in cases if case_controller.calculate_case_status(case) in ['Not Started', 'Downloaded']]
        elif survey_list == 'history':
            filtered_cases = [case for case in cases if case_controller.calculate_case_status(case) in ['Complete']]
        else:
            raise InvalidSurveyList(survey_list)
        surveys_data = [case_controller.build_full_case_data(case=case) for case in filtered_cases]

        logger.info('Successfully retrieved surveys list', party_id=party_id, survey_list=survey_list)
        return surveys_data
