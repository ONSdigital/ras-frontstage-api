import os

from flask import Flask

from frontstage_api.logger_config import logger_initial_config


app = Flask(__name__)

app_config = 'config.{}'.format(os.environ.get('APP_SETTINGS', 'Config'))
app.config.from_object(app_config)

logger_initial_config(service_name='ras-frontstage-api', log_level=app.config['LOGGING_LEVEL'])


import frontstage_api.views.secure_messaging  # NOQA
