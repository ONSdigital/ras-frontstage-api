import os


class Config(object):
    DEBUG = os.getenv('DEBUG', False)
    TESTING = False
    NAME = 'ras-frontstage-api'
    VERSION = os.getenv('VERSION', '0.0.3')
    PORT = os.getenv('PORT', 8083)
    LOGGING_LEVEL = os.getenv('LOGGING_LEVEL', 'INFO')
    SECURITY_USER_NAME = os.getenv('SECURITY_USER_NAME')
    SECURITY_USER_PASSWORD = os.getenv('SECURITY_USER_PASSWORD')
    BASIC_AUTH = (SECURITY_USER_NAME, SECURITY_USER_PASSWORD)
    DJANGO_CLIENT_ID = os.getenv('DJANGO_CLIENT_ID')
    DJANGO_CLIENT_SECRET = os.getenv('DJANGO_CLIENT_SECRET')
    DJANGO_BASIC_AUTH = (DJANGO_CLIENT_ID, DJANGO_CLIENT_SECRET)
    MAX_UPLOAD_LENGTH = os.getenv('MAX_UPLOAD_LENGTH', 20 * 1024 * 1024)

    RM_CASE_SERVICE_HOST = os.getenv('RM_CASE_SERVICE_HOST', 'localhost')
    RM_CASE_SERVICE_PORT = os.getenv('RM_CASE_SERVICE_PORT', 8171)
    RM_CASE_SERVICE_PROTOCOL = os.getenv('RM_CASE_SERVICE_PROTOCOL', 'http')
    RM_CASE_SERVICE = '{}://{}:{}/'.format(RM_CASE_SERVICE_PROTOCOL, RM_CASE_SERVICE_HOST, RM_CASE_SERVICE_PORT)
    RM_CASE_GET_BY_ID = '{}cases/{}'.format(RM_CASE_SERVICE, '{}')
    RM_CASE_GET_BY_PARTY = '{}cases/partyid/{}'.format(RM_CASE_SERVICE, '{}')
    RM_CASE_GET_BY_IAC = '{}cases/iac/{}'.format(RM_CASE_SERVICE, '{}')
    RM_CASE_GET_CATEGORIES = '{}categories'.format(RM_CASE_SERVICE)
    RM_CASE_POST_CASE_EVENT = '{}cases/{}/events'.format(RM_CASE_SERVICE, '{}')

    RAS_SECURE_MESSAGE_SERVICE_HOST = os.getenv('RAS_SECURE_MESSAGE_SERVICE_HOST', 'localhost')
    RAS_SECURE_MESSAGE_SERVICE_PORT = os.getenv('RAS_SECURE_MESSAGE_SERVICE_PORT', 5050)
    RAS_SECURE_MESSAGE_SERVICE_PROTOCOL = os.getenv('RAS_SECURE_MESSAGE_SERVICE_PROTOCOL', 'http')
    RAS_SECURE_MESSAGE_SERVICE = '{}://{}:{}/'.format(RAS_SECURE_MESSAGE_SERVICE_PROTOCOL,
                                                      RAS_SECURE_MESSAGE_SERVICE_HOST,
                                                      RAS_SECURE_MESSAGE_SERVICE_PORT)
    MESSAGE_LIMIT = os.getenv('MESSAGE_LIMIT', 1000)
    MESSAGE_URL = '{}message'.format(RAS_SECURE_MESSAGE_SERVICE)
    DRAFT_URL = '{}draft'.format(RAS_SECURE_MESSAGE_SERVICE)
    THREAD_URL = '{}thread'.format(RAS_SECURE_MESSAGE_SERVICE)
    MESSAGES_LIST_URL = '{}messages?limit={}'.format(RAS_SECURE_MESSAGE_SERVICE, MESSAGE_LIMIT)
    UNREAD_MESSAGES_TOTAL_URL = '{}labels?name=unread'.format(RAS_SECURE_MESSAGE_SERVICE)
    SEND_MESSAGE_URL = '{}message/send'.format(RAS_SECURE_MESSAGE_SERVICE)
    DRAFT_SAVE_URL = '{}draft/save'.format(RAS_SECURE_MESSAGE_SERVICE)
    DRAFT_MODIFY_URL = '{}draft/{}/modify'.format(RAS_SECURE_MESSAGE_SERVICE, '{}')
    REMOVE_UNREAD_LABEL_URL = '{}message/{}/modify'.format(RAS_SECURE_MESSAGE_SERVICE, '{}')

    RAS_PARTY_SERVICE_HOST = os.getenv('RAS_PARTY_SERVICE_HOST', 'localhost')
    RAS_PARTY_SERVICE_PORT = os.getenv('RAS_PARTY_SERVICE_PORT', 8081)
    RAS_PARTY_SERVICE_PROTOCOL = os.getenv('RAS_PARTY_SERVICE_PROTOCOL', 'http')
    RAS_PARTY_SERVICE = '{}://{}:{}/'.format(RAS_PARTY_SERVICE_PROTOCOL, RAS_PARTY_SERVICE_HOST, RAS_PARTY_SERVICE_PORT)
    RAS_PARTY_GET_BY_RESPONDENT_ID = '{}party-api/v1/respondents/id/{}'.format(RAS_PARTY_SERVICE, '{}')
    RAS_PARTY_GET_BY_EMAIL_URL = '{}party-api/v1/respondents/email/{}'.format(RAS_PARTY_SERVICE, '{}')
    RAS_PARTY_RESET_PASSWORD_REQUEST = '{}party-api/v1/respondents/request_password_change'.format(RAS_PARTY_SERVICE)
    RAS_PARTY_VERIFY_PASSWORD_TOKEN = '{}party-api/v1/tokens/verify/{}'.format(RAS_PARTY_SERVICE, '{}')
    RAS_PARTY_CHANGE_PASSWORD = '{}party-api/v1/respondents/change_password/{}'.format(RAS_PARTY_SERVICE, '{}')
    RAS_PARTY_GET_BY_BUSINESS_ID = '{}party-api/v1/businesses/id/{}'.format(RAS_PARTY_SERVICE, '{}')
    RAS_PARTY_POST_RESPONDENTS = '{}party-api/v1/respondents'.format(RAS_PARTY_SERVICE)
    RAS_PARTY_VERIFY_EMAIL = '{}party-api/v1/emailverification/{}'.format(RAS_PARTY_SERVICE, '{}')
    RAS_PARTY_ADD_SURVEY = '{}party-api/v1/respondents/add_survey'.format(RAS_PARTY_SERVICE)

    RAS_OAUTH_SERVICE_HOST = os.getenv('RAS_OAUTH_SERVICE_HOST', 'localhost')
    RAS_OAUTH_SERVICE_PORT = os.getenv('RAS_OAUTH_SERVICE_PORT', 8040)
    RAS_OAUTH_SERVICE_PROTOCOL = os.getenv('RAS_OAUTH_SERVICE_PROTOCOL', 'http')
    RAS_OAUTH_SERVICE = '{}://{}:{}/'.format(RAS_OAUTH_SERVICE_PROTOCOL, RAS_OAUTH_SERVICE_HOST, RAS_OAUTH_SERVICE_PORT)
    OAUTH_TOKEN_URL = '{}api/v1/tokens/'.format(RAS_OAUTH_SERVICE)

    RM_IAC_SERVICE_HOST = os.getenv('RM_IAC_SERVICE_HOST', 'localhost')
    RM_IAC_SERVICE_PORT = os.getenv('RM_IAC_SERVICE_PORT', 8121)
    RM_IAC_SERVICE_PROTOCOL = os.getenv('RM_IAC_SERVICE_PROTOCOL', 'http')
    RM_IAC_SERVICE = '{}://{}:{}/'.format(RM_IAC_SERVICE_PROTOCOL, RM_IAC_SERVICE_HOST, RM_IAC_SERVICE_PORT)
    RM_IAC_GET = '{}iacs/{}'.format(RM_IAC_SERVICE, '{}')

    RM_COLLECTION_EXERCISE_SERVICE_HOST = os.getenv('RM_COLLECTION_EXERCISE_SERVICE_HOST', 'localhost')
    RM_COLLECTION_EXERCISE_SERVICE_PORT = os.getenv('RM_COLLECTION_EXERCISE_SERVICE_PORT', 8145)
    RM_COLLECTION_EXERCISE_SERVICE_PROTOCOL = os.getenv('RM_COLLECTION_EXERCISE_SERVICE_PROTOCOL', 'http')
    RM_COLLECTION_EXERCISE_SERVICE = '{}://{}:{}/'.format(RM_COLLECTION_EXERCISE_SERVICE_PROTOCOL,
                                                          RM_COLLECTION_EXERCISE_SERVICE_HOST,
                                                          RM_COLLECTION_EXERCISE_SERVICE_PORT)
    RM_COLLECTION_EXERCISE_GET = '{}collectionexercises/{}'.format(RM_COLLECTION_EXERCISE_SERVICE, '{}')
    RM_COLLECTION_EXERCISE_EVENTS = '{}collectionexercises/{}/events'.format(RM_COLLECTION_EXERCISE_SERVICE, '{}')

    RM_SURVEY_SERVICE_HOST = os.getenv('RM_SURVEY_SERVICE_HOST', 'localhost')
    RM_SURVEY_SERVICE_PORT = os.getenv('RM_SURVEY_SERVICE_PORT', 8080)
    RM_SURVEY_SERVICE_PROTOCOL = os.getenv('RM_SURVEY_SERVICE_PROTOCOL', 'http')
    RM_SURVEY_SERVICE = '{}://{}:{}/'.format(RM_SURVEY_SERVICE_PROTOCOL, RM_SURVEY_SERVICE_HOST, RM_SURVEY_SERVICE_PORT)
    RM_SURVEY_GET = '{}surveys/{}'.format(RM_SURVEY_SERVICE, '{}')

    RAS_COLLECTION_INSTRUMENT_SERVICE_HOST = os.getenv('RAS_COLLECTION_INSTRUMENT_SERVICE_HOST', 'localhost')
    RAS_COLLECTION_INSTRUMENT_SERVICE_PORT = os.getenv('RAS_COLLECTION_INSTRUMENT_SERVICE_PORT', 8002)
    RAS_COLLECTION_INSTRUMENT_SERVICE_PROTOCOL = os.getenv('RAS_COLLECTION_INSTRUMENT_SERVICE_PROTOCOL', 'http')
    RAS_COLLECTION_INSTRUMENT_SERVICE = '{}://{}:{}/'.format(RAS_COLLECTION_INSTRUMENT_SERVICE_PROTOCOL,
                                                             RAS_COLLECTION_INSTRUMENT_SERVICE_HOST,
                                                             RAS_COLLECTION_INSTRUMENT_SERVICE_PORT)
    RAS_CI_SIZE = '{}collection-instrument-api/1.0.2/instrument_size/{}'.format(RAS_COLLECTION_INSTRUMENT_SERVICE, '{}')
    RAS_CI_DOWNLOAD = '{}collection-instrument-api/1.0.2/download/{}'.format(RAS_COLLECTION_INSTRUMENT_SERVICE, '{}')
    RAS_CI_UPLOAD = '{}survey_response-api/v1/survey_responses/{}'.format(RAS_COLLECTION_INSTRUMENT_SERVICE, '{}')
    RAS_CI_DETAILS = '{}collection-instrument-api/1.0.2/collectioninstrument/id/{}'\
        .format(RAS_COLLECTION_INSTRUMENT_SERVICE, '{}')
    JSON_SECRET_KEYS = os.getenv('JSON_SECRET_KEYS')
    EQ_URL = os.getenv('EQ_URL')
    ACCOUNT_SERVICE_URL = os.getenv('ACCOUNT_SERVICE_URL')


class DevelopmentConfig(Config):
    DEBUG = os.getenv('DEBUG', True)
    LOGGING_LEVEL = os.getenv('LOGGING_LEVEL', 'DEBUG')
    SECURITY_USER_NAME = os.getenv('SECURITY_USER_NAME', 'admin')
    SECURITY_USER_PASSWORD = os.getenv('SECURITY_USER_PASSWORD', 'secret')
    BASIC_AUTH = (SECURITY_USER_NAME, SECURITY_USER_PASSWORD)
    DJANGO_CLIENT_ID = os.getenv('DJANGO_CLIENT_ID', 'ons@ons.gov')
    DJANGO_CLIENT_SECRET = os.getenv('DJANGO_CLIENT_SECRET', 'password')
    DJANGO_BASIC_AUTH = (DJANGO_CLIENT_ID, DJANGO_CLIENT_SECRET)


class TestingConfig(DevelopmentConfig):
    DEBUG = True
    TESTING = True
    LOGGING_LEVEL = os.getenv('LOGGING_LEVEL', 'DEBUG')
    JSON_SECRET_KEYS = open("./tests/jwt-test-keys/test_key.json").read()
    EQ_URL = 'https://eq-test/session?token='
    ACCOUNT_SERVICE_URL ='http://frontstage-url/surveys'
