import logging

from structlog import wrap_logger

from frontstage_api import app


logging = wrap_logger(logging.getLogger(__name__))


@app.route('/', methods=['GET'])
def hello():
    return 'Hello'
