import os

from flask import Flask
from flask_restplus import Api

from logger_config import logger_initial_config


app = Flask(__name__)
api = Api(app)

app_config = 'config.{}'.format(os.environ.get('APP_SETTINGS', 'Config'))
app.config.from_object(app_config)

logger_initial_config(service_name='ras-frontstage-api', log_level=app.config['LOGGING_LEVEL'])


import frontstage_api.error_handlers  # NOQA # pylint: disable=wrong-import-position
import frontstage_api.resources.secure_messaging  # NOQA # pylint: disable=wrong-import-position
import frontstage_api.resources.info  # NOQA # pylint: disable=wrong-import-position
