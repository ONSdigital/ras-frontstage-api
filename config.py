class Config(object):
    DEBUG = False
    TESTING = False
    PORT = 8082


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    DEBUG = True
    TESTING = True
