import os


class Config(object):
    DEBUG = os.getenv('DEBUG', False)
    TESTING = False
    NAME = 'ras-frontstage-api'
    VERSION = os.getenv('VERSION', '0.0.1')
    PORT = os.getenv('PORT', 8082)
    LOGGING_LEVEL = os.getenv('LOGGING_LEVEL', 'INFO')

    RAS_SECURE_MESSAGE_SERVICE_HOST = os.getenv('RAS_SECURE_MESSAGE_SERVICE_HOST', 'localhost')
    RAS_SECURE_MESSAGE_SERVICE_PORT = os.getenv('RAS_SECURE_MESSAGE_SERVICE_PORT', 5050)
    RAS_SECURE_MESSAGE_SERVICE_PROTOCOL = os.getenv('RAS_SECURE_MESSAGE_SERVICE_PROTOCOL', 'http')
    RAS_SECURE_MESSAGE_SERVICE = '{}://{}:{}/'.format(RAS_SECURE_MESSAGE_SERVICE_PROTOCOL,
                                                      RAS_SECURE_MESSAGE_SERVICE_HOST,
                                                      RAS_SECURE_MESSAGE_SERVICE_PORT)
    MESSAGE_LIMIT = os.getenv('MESSAGE_LIMIT', 1000)
    MESSAGES_LIST_URL = '{}messages?limit={}'.format(RAS_SECURE_MESSAGE_SERVICE, MESSAGE_LIMIT)
    UNREAD_MESSAGES_TOTAL_URL = '{}labels?name=unread'.format(RAS_SECURE_MESSAGE_SERVICE)


class DevelopmentConfig(Config):
    DEBUG = os.getenv('DEBUG', True)
    LOGGING_LEVEL = os.getenv('LOGGING_LEVEL', 'DEBUG')


class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    LOGGING_LEVEL = os.getenv('LOGGING_LEVEL', 'DEBUG')
