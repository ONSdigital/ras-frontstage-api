import os

from flask import Flask


app = Flask(__name__)

app_config = 'config.{}'.format(os.environ.get('APP_SETTINGS', 'Config'))
app.config.from_object(app_config)


import frontstage_api.views.secure_messaging  # NOQA
