import os


class Config(object):
    DEBUG = False
    TESTING = False
    PORT = 8082
    LOGGING_LEVEL = os.getenv('LOGGING_LEVEL', 'INFO')


class DevelopmentConfig(Config):
    DEBUG = True
    LOGGING_LEVEL = os.getenv('LOGGING_LEVEL', 'DEBUG')


class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    LOGGING_LEVEL = os.getenv('LOGGING_LEVEL', 'DEBUG')
