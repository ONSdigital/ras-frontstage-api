import logging
import os

from structlog import wrap_logger


if not os.getenv('APP_SETTINGS'):
    os.environ['APP_SETTINGS'] = 'DevelopmentConfig'

from frontstage_api import app  # NOQA

logger = wrap_logger(logging.getLogger(__name__))


if __name__ == '__main__':
    logger.info('* starting listening port "{}"'.format(app.config['PORT']))
    app.run(debug=app.config['DEBUG'], host='0.0.0.0', port=int(app.config['PORT']))
