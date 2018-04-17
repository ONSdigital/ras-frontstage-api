from datetime import datetime, timezone
import logging

from flask import request
from flask_restplus import Resource, reqparse
from iso8601 import parse_date
from structlog import wrap_logger

from frontstage_api import auth, surveys_api
from frontstage_api.controllers import case_controller
from frontstage_api.exceptions.exceptions import InvalidSurveyList


logger = wrap_logger(logging.getLogger(__name__))

parser = reqparse.RequestParser()
parser.add_argument('list', location='args', required=True)
parser.add_argument('party_id', location='args', required=True)


@surveys_api.route('/surveys-list')
class GetSurveysList(Resource):

    @staticmethod
    @auth.login_required
    @surveys_api.expect(parser)
    def get():
        respondent_id = request.args['party_id']
        survey_list = request.args['list']
        logger.info('Retrieving surveys list', respondent_id=respondent_id, survey_list=survey_list)

        cases = case_controller.get_case_by_party_id(respondent_id, case_events=True)

        # Filter out the cases relevant to the request
        if survey_list == 'todo':
            filtered_cases = [case
                              for case in cases
                              if case.get('caseGroup', {}).get('caseGroupStatus') not in ['COMPLETE', 'COMPLETEDBYPHONE']]
        elif survey_list == 'history':
            filtered_cases = [case
                              for case in cases
                              if case.get('caseGroup', {}).get('caseGroupStatus') in ['COMPLETE', 'COMPLETEDBYPHONE']]
        else:
            raise InvalidSurveyList(survey_list)
        surveys_data = [case_controller.build_full_case_data(case=case) for case in filtered_cases]
        now = datetime.now(timezone.utc)
        live_cases = [survey for survey in surveys_data if parse_date(survey['go_live']['timestamp']) < now]
        enrolled_cases = [case for case in live_cases if _case_is_enrolled(case, respondent_id)]

        logger.info('Successfully retrieved surveys list', respondent_id=respondent_id, survey_list=survey_list)
        return enrolled_cases


def _case_is_enrolled(case, respondent_id):
    association = next(association
                       for association in case['business_party']['associations']
                       if association['partyId'] == respondent_id)
    enrolment_status = next(enrolment['enrolmentStatus']
                            for enrolment in association.get('enrolments')
                            if enrolment['surveyId'] == case['survey']['id'])
    return enrolment_status == 'ENABLED'
