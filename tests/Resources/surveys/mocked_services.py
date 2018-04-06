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

url_download_ci = f"{app.config['RAS_COLLECTION_INSTRUMENT_SERVICE']}/collection-instrument-api/1.0.2/download/68ad4018-2ddd-4894-89e7-33f0135887a2"
url_get_business_party = f"{app.config['RAS_PARTY_SERVICE']}/party-api/v1/businesses/id/1216a88f-ee2a-420c-9e6a-ee34893c29cf"
url_get_case = f"{app.config['RM_CASE_SERVICE']}/cases/abc670a5-67c6-4d96-9164-13b4017b8704"
url_get_case_by_enrolment = f"{app.config['RM_CASE_SERVICE']}/cases/iac/test_enrolment"
url_get_case_by_party_no_events = f"{app.config['RM_CASE_SERVICE']}/cases/partyid/test_party"
url_get_case_by_party = f"{app.config['RM_CASE_SERVICE']}/cases/partyid/07d672bc-497b-448f-a406-a20a7e6013d7?caseevents=true"
url_get_case_categories = f"{app.config['RM_CASE_SERVICE']}/categories"
url_get_collection_exercise = f"{app.config['RM_COLLECTION_EXERCISE_SERVICE']}/collectionexercises/14fb3e68-4dca-46db-bf49-04b84e07e77c"
url_get_collection_exercise_events = f"{app.config['RM_COLLECTION_EXERCISE_SERVICE']}/collectionexercises/14fb3e68-4dca-46db-bf49-04b84e07e77c/events"
url_get_collection_exercise_go_live = f"{app.config['RM_COLLECTION_EXERCISE_SERVICE']}/collectionexercises/14fb3e68-4dca-46db-bf49-04b84e07e77c/events/go_live"
url_get_ci = f"{app.config['RAS_COLLECTION_INSTRUMENT_SERVICE']}/collection-instrument-api/1.0.2/collectioninstrument/id/68ad4018-2ddd-4894-89e7-33f0135887a2"
url_get_iac = f"{app.config['RM_IAC_SERVICE']}/iacs/test_enrolment"
url_get_survey = f"{app.config['RM_SURVEY_SERVICE']}/surveys/test_survey_id"
url_post_add_survey = f"{app.config['RAS_PARTY_SERVICE']}/party-api/v1/respondents/add_survey"
url_post_case_event = f"{app.config['RM_CASE_SERVICE']}/cases/test_case_id/events"
url_post_case_event_uuid = f"{app.config['RM_CASE_SERVICE']}/cases/abc670a5-67c6-4d96-9164-13b4017b8704/events"
url_upload_ci = f"{app.config['RAS_COLLECTION_INSTRUMENT_SERVICE']}/survey_response-api/v1/survey_responses/abc670a5-67c6-4d96-9164-13b4017b8704"
