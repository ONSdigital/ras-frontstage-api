import logging
import os
from testfixtures import log_capture
import unittest

from structlog import wrap_logger

from logger_config import logger_initial_config


class TestLoggerConfig(unittest.TestCase):

    @log_capture()
    def test_success(self, l):
        os.environ['JSON_INDENT_LOGGING'] = '1'
        logger_initial_config(service_name='ras-frontstage-api')
        logger = wrap_logger(logging.getLogger())
        logger.error('Test')
        message = l.records[0].msg
        self.assertTrue('{\n "event": "Test",\n "level": "error",\n "service": "ras-frontstage-api"' in message)

    @log_capture()
    def test_indent_type_error(self, l):
        os.environ['JSON_INDENT_LOGGING'] = 'abc'
        logger_initial_config(service_name='ras-frontstage-api')
        logger = wrap_logger(logging.getLogger())
        logger.error('Test')
        message = l.records[0].msg
        self.assertTrue('{"event": "Test", "level": "error", "service": "ras-frontstage-api"' in message)

    @log_capture()
    def test_indent_value_error(self, l):
        logger_initial_config(service_name='ras-frontstage-api')
        logger = wrap_logger(logging.getLogger())
        logger.error('Test')
        message = l.records[0].msg
        self.assertTrue('{"event": "Test", "level": "error", "service": "ras-frontstage-api"' in message)
