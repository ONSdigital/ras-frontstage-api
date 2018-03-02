import datetime
import logging
import time
import uuid

from flask import current_app
from frontstage_api.controllers import collection_exercise_controller, \
    collection_instrument_controller, party_controller, survey_controller
from frontstage_api.exceptions.exceptions import InvalidEqPayLoad
from structlog import wrap_logger

logger = wrap_logger(logging.getLogger(__name__))


class EqPayload(object):

    def create_payload(self, case):
        """
        Creates the payload needed to communicate with EQ, built from the Case, Collection Exercise, Party,
        Survey and Collection Instrument services
        :case_id: The unique UUID references of a case
        :return Payload for EQ
        """

        tx_id = str(uuid.uuid4())
        logger.info('Creating payload for JWT', case_id=case['id'], tx_id=tx_id)

        # Collection Instrument
        ci_id = case['collectionInstrumentId']
        ci = collection_instrument_controller.get_collection_instrument(ci_id)
        if ci['type'] != 'EQ':
            raise InvalidEqPayLoad('Collection instrument {} type is not EQ'.format(ci_id))

        classifiers = ci['classifiers']
        if not classifiers or not classifiers.get('eq_id') or not classifiers.get('form_type'):
            raise InvalidEqPayLoad('Collection instrument {} classifiers are incorrect or missing'.format(ci_id))

        eq_id = ci['classifiers']['eq_id']
        form_type = ci['classifiers']['form_type']

        # Collection Exercise
        collex_id = case["caseGroup"]["collectionExerciseId"]
        collex = collection_exercise_controller.get_collection_exercise(collex_id)
        collex_event_dates = self._get_collex_event_dates(collex_id)

        # Party
        party_id = case['caseGroup']['partyId']
        party = party_controller.get_party_by_business_id(party_id, collection_exercise_id=collex_id)

        # Survey
        survey_id = collex['surveyId']
        survey = survey_controller.get_survey(survey_id)

        account_service_url = current_app.config['ACCOUNT_SERVICE_URL']
        iat = time.time()
        exp = time.time() + (5 * 60)

        return {
            'jti': str(uuid.uuid4()),
            'tx_id': tx_id,
            'user_id': case['partyId'],
            'iat': int(iat),
            'exp': int(exp),
            'eq_id': eq_id,
            'period_str': collex['userDescription'],
            'period_id': collex['exerciseRef'],
            'form_type': form_type,
            'collection_exercise_sid': collex['id'],
            'ref_p_start_date': collex_event_dates['ref_p_start_date'],
            'ref_p_end_date': collex_event_dates['ref_p_end_date'],
            'ru_ref': party['sampleUnitRef'],
            'ru_name': party['name'],
            'return_by': collex_event_dates['return_by'],
            'survey_id': survey['surveyRef'],
            'case_id': case['id'],
            'case_ref': case['caseRef'],
            'account_service_url': account_service_url
        }

    def _get_collex_event_dates(self, collex_id):
        """
        Maps the required collection exercise dates to a dic
        :param collex_id: The unique UUID references of a collection exercise
        :return A dict of event dates associate with the Exercise
        """

        collex_events = collection_exercise_controller.get_collection_exercise_events(collex_id)
        return {
             "ref_p_start_date": self._find_event_date_by_tag('ref_period_start', collex_events, collex_id),
             "ref_p_end_date": self._find_event_date_by_tag('exercise_end', collex_events, collex_id),
             "return_by": self._find_event_date_by_tag('return_by', collex_events, collex_id)
        }

    def _find_event_date_by_tag(self, search_param, collex_events, collex_id):
        """
        Finds the required date from the list of all the events
        :param search_param: the string name of the date searching for
        :param collex_events: All the Collection Exercise dates
        :return exercise
        """

        for event in collex_events:
            if event['tag'] == search_param and event.get('timestamp'):
                return self._format_string_long_date_time_to_short_date(event['timestamp'])
        raise InvalidEqPayLoad('Event not found for collection {} for search param {}'.format(collex_id, search_param))

    @staticmethod
    def _format_string_long_date_time_to_short_date(string_date):
        """
        Formats the date from a string to %Y-%m-%d eg 2018-01-20
        :param string_date: The date in string format should be in format %Y-%m-%dT%H:%M:%S.%fZ
        :return formatted date
        """

        try:
            formatted_date = datetime.datetime.strptime(string_date, '%Y-%m-%dT%H:%M:%S.%fZ').strftime('%Y-%m-%d')
        except ValueError:
            raise InvalidEqPayLoad('Unable to format {}, expected format %Y-%m-%dT%H:%M:%S.%fZ'.format(string_date))
        return formatted_date
