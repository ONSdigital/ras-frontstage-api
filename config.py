import os


class Config(object):
    DEBUG = os.getenv('DEBUG', False)
    TESTING = False
    NAME = 'ras-frontstage-api'
    VERSION = os.getenv('VERSION', '0.0.1')
    PORT = os.getenv('PORT', 8083)
    LOGGING_LEVEL = os.getenv('LOGGING_LEVEL', 'INFO')
    SECURITY_USER_NAME = os.getenv('SECURITY_USER_NAME')
    SECURITY_USER_PASSWORD = os.getenv('SECURITY_USER_PASSWORD')
    BASIC_AUTH = (SECURITY_USER_NAME, SECURITY_USER_PASSWORD)
    DJANGO_CLIENT_ID = os.getenv('DJANGO_CLIENT_ID')
    DJANGO_CLIENT_SECRET = os.getenv('DJANGO_CLIENT_SECRET')
    DJANGO_BASIC_AUTH = (DJANGO_CLIENT_ID, DJANGO_CLIENT_SECRET)

    RM_CASE_SERVICE_HOST = os.getenv('RM_CASE_SERVICE_HOST', 'localhost')
    RM_CASE_SERVICE_PORT = os.getenv('RM_CASE_SERVICE_PORT', 8171)
    RM_CASE_SERVICE_PROTOCOL = os.getenv('RM_CASE_SERVICE_PROTOCOL', 'http')
    RM_CASE_SERVICE = '{}://{}:{}/'.format(RM_CASE_SERVICE_PROTOCOL, RM_CASE_SERVICE_HOST, RM_CASE_SERVICE_PORT)
    RM_CASE_GET_BY_PARTY = '{}cases/partyid/{}'.format(RM_CASE_SERVICE, '{}')

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
    PARTY_BY_RESPONDENT_ID = '{}party-api/v1/respondents/id/{}'.format(RAS_PARTY_SERVICE, '{}')
    RAS_PARTY_GET_BY_EMAIL_URL = '{}party-api/v1/respondents/email/{}'.format(RAS_PARTY_SERVICE, '{}')

    RAS_OAUTH_SERVICE_HOST = os.getenv('RAS_OAUTH_SERVICE_HOST', 'localhost')
    RAS_OAUTH_SERVICE_PORT = os.getenv('RAS_OAUTH_SERVICE_PORT', 8040)
    RAS_OAUTH_SERVICE_PROTOCOL = os.getenv('RAS_OAUTH_SERVICE_PROTOCOL', 'http')
    RAS_OAUTH_SERVICE = '{}://{}:{}/'.format(RAS_OAUTH_SERVICE_PROTOCOL, RAS_OAUTH_SERVICE_HOST, RAS_OAUTH_SERVICE_PORT)
    OAUTH_TOKEN_URL = '{}api/v1/tokens/'.format(RAS_OAUTH_SERVICE)


class DevelopmentConfig(Config):
    DEBUG = os.getenv('DEBUG', True)
    LOGGING_LEVEL = os.getenv('LOGGING_LEVEL', 'DEBUG')
    SECURITY_USER_NAME = os.getenv('SECURITY_USER_NAME', 'test_user')
    SECURITY_USER_PASSWORD = os.getenv('SECURITY_USER_PASSWORD', 'test_password')


class TestingConfig(DevelopmentConfig):
    DEBUG = True
    TESTING = True
    LOGGING_LEVEL = os.getenv('LOGGING_LEVEL', 'DEBUG')
