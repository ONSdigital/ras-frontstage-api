import json
from frontstage_api import app


with open('tests/test_data/party/business_party.json') as json_data:
    business_party = json.load(json_data)

with open('tests/test_data/case/case.json') as json_data:
    case = json.load(json_data)

with open('tests/test_data/case/case_list.json') as json_data:
    case_list = json.load(json_data)

with open('tests/test_data/case/categories.json') as json_data:
    categories = json.load(json_data)

with open('tests/test_data/collection_exercise/collection_exercise.json') as json_data:
    collection_exercise = json.load(json_data)

with open('tests/test_data/collection_exercise/collection_exercise_before_go_live.json') as json_data:
    collection_exercise_before_go_live = json.load(json_data)

with open('tests/test_data/collection_exercise/collection_exercise_events.json') as json_data:
    collection_exercise_events = json.load(json_data)

with open('tests/test_data/collection_instrument/collection_instrument_eq.json') as json_data:
    collection_instrument_eq = json.load(json_data)

with open('tests/test_data/collection_instrument/collection_instrument_seft.json') as json_data:
    collection_instrument_seft = json.load(json_data)

with open('tests/test_data/case/completed_case.json') as json_data:
    completed_case = json.load(json_data)

with open('tests/test_data/case/completed_by_phone_case.json') as json_data:
    completed_by_phone_case = [json.load(json_data)]

with open('tests/test_data/collection_exercise/go_live_event.json') as json_data:
    go_live_event = json.load(json_data)

with open('tests/test_data/collection_exercise/go_live_event_before.json') as json_data:
    go_live_event_before = json.load(json_data)

with open('tests/test_data/survey/survey.json') as json_data:
    survey = json.load(json_data)

url_download_collection_instrument = app.config['RAS_CI_DOWNLOAD'].format('68ad4018-2ddd-4894-89e7-33f0135887a2')
url_get_business_party = app.config['RAS_PARTY_GET_BY_BUSINESS_ID'].format('1216a88f-ee2a-420c-9e6a-ee34893c29cf')
url_get_case = app.config['RM_CASE_GET_BY_ID'].format('abc670a5-67c6-4d96-9164-13b4017b8704')
url_get_case_by_enrolment = app.config['RM_CASE_GET_BY_IAC'].format('test_enrolment')
url_get_case_by_party_no_events = app.config['RM_CASE_GET_BY_PARTY'].format('test_party')
url_get_case_by_party = app.config['RM_CASE_GET_BY_PARTY'].format('07d672bc-497b-448f-a406-a20a7e6013d7') + '?caseevents=true'
url_get_case_categories = app.config['RM_CASE_GET_CATEGORIES']
url_get_collection_exercise = app.config['RM_COLLECTION_EXERCISE_GET'].format('14fb3e68-4dca-46db-bf49-04b84e07e77c')
url_get_collection_exercise_events = app.config['RM_COLLECTION_EXERCISE_EVENTS'].format('14fb3e68-4dca-46db-bf49-04b84e07e77c')
url_get_collection_exercise_go_live = url = app.config['RM_COLLECTION_EXERCISE_EVENT'].format('14fb3e68-4dca-46db-bf49-04b84e07e77c', 'go_live')
url_get_collection_instrument = app.config['RAS_CI_DETAILS'].format('68ad4018-2ddd-4894-89e7-33f0135887a2')
url_get_iac = app.config['RM_IAC_GET'].format('test_enrolment')
url_get_survey = app.config['RM_SURVEY_GET'].format('test_survey_id')
url_post_add_survey = app.config['RAS_PARTY_ADD_SURVEY']
url_post_case_event = app.config['RM_CASE_POST_CASE_EVENT'].format('test_case_id')
url_post_case_event_uuid = app.config['RM_CASE_POST_CASE_EVENT'].format('abc670a5-67c6-4d96-9164-13b4017b8704')
url_upload_collection_instrument = app.config['RAS_CI_UPLOAD'].format('abc670a5-67c6-4d96-9164-13b4017b8704')
