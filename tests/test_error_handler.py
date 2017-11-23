import unittest

from frontstage_api import app
from frontstage_api.exceptions.exceptions import (FileTooLarge, NoJWTError, ApiError, InvalidCaseCategory,
                                                  InvalidSurveyList, InvalidRequestMethod, NoSurveyPermission)
from frontstage_api.error_handlers import (file_too_large, no_jwt_in_header, api_error_method, invalid_case_category,
                                           invalid_survey_list, invalid_request_method, no_survey_permission)


class TestErrorHandlers(unittest.TestCase):

    def setUp(self):
        self.app_context = app.app_context()
        self.app_request_context = app.test_request_context()

    def test_file_too_large_handler(self):
        error = FileTooLarge('case_id', 'party_id', 100)

        with self.assertLogs() as cm:
            response, code = file_too_large(error)

        self.assertIn('INFO', cm[1][0])
        self.assertIn('"file_size": 100', cm[1][0])
        self.assertIn('"case_id": "case_id"', cm[1][0])
        self.assertIn('"party_id": "party_id"', cm[1][0])
        self.assertIn("error", response)
        self.assertIn("data", response['error'])
        self.assertIn("message", response['error']['data'])
        self.assertEqual(400, code)

    def test_no_jwt_in_header_handler(self):
        error = NoJWTError()

        response, code = no_jwt_in_header(error)

        self.assertEqual(401, code)
        self.assertEqual({'message': 'No JWT provided in request header'}, response)

    def test_api_error_method_handler_not_500(self):
        error = ApiError('url', 400, 'data', 'description', key='value')

        with self.app_context, self.app_request_context:
            with self.assertLogs() as cm:
                response, code = api_error_method(error)

        self.assertIn('INFO', cm[1][0])
        self.assertIn('"status": 400', cm[1][0])
        self.assertIn('"description"', cm[1][0])
        self.assertIn('"key": "value"', cm[1][0])
        self.assertIn(b"error", response.data)
        self.assertIn(b"data", response.data)
        self.assertEqual(400, code)

    def test_api_error_method_handler_500(self):
        error = ApiError('url', 500, 'data', 'description')

        with self.app_context, self.app_request_context:
            with self.assertLogs() as cm:
                response, code = api_error_method(error)

        self.assertIn('ERROR', cm[1][0])
        self.assertIn('"status": 500', cm[1][0])
        self.assertIn('"description"', cm[1][0])
        self.assertIn(b"error", response.data)
        self.assertIn(b"data", response.data)
        self.assertEqual(500, code)

    def test_api_error_method_handler_no_status_code(self):
        error = ApiError('url', None, 'data', 'description')

        with self.app_context, self.app_request_context:
            with self.assertLogs() as cm:
                response, code = api_error_method(error)

        self.assertIn('ERROR', cm[1][0])
        self.assertIn('"status": null', cm[1][0])
        self.assertIn('"description"', cm[1][0])
        self.assertIn(b"error", response.data)
        self.assertIn(b"data", response.data)
        self.assertEqual(500, code)

    def test_invalid_case_category_handler(self):
        error = InvalidCaseCategory("category")

        with self.assertLogs() as cm:
            response, code = invalid_case_category(error)

        self.assertIn('ERROR', cm[1][0])
        self.assertIn('"category": "category"', cm[1][0])
        self.assertIn("message", response)
        self.assertIn("category", response)
        self.assertEqual("category", response['category'])
        self.assertEqual(500, code)

    def test_invalid_survey_list_handler(self):
        error = InvalidSurveyList("survey_list")

        with self.assertLogs() as cm:
            response, code = invalid_survey_list(error)

        self.assertIn('INFO', cm[1][0])
        self.assertIn('"survey_list": "survey_list"', cm[1][0])
        self.assertIn("message", response)
        self.assertIn("survey_list", response)
        self.assertEqual("survey_list", response['survey_list'])
        self.assertEqual(400, code)

    def test_invalid_request_method_handler(self):
        error = InvalidRequestMethod('method', 'url')

        with self.assertLogs() as cm:
            response, code = invalid_request_method(error)

        self.assertIn('ERROR', cm[1][0])
        self.assertIn('"method": "method"', cm[1][0])
        self.assertIn('"url": "url"', cm[1][0])
        self.assertIn("message", response)
        self.assertIn("method", response)
        self.assertIn("url", response)
        self.assertEqual(500, code)

    def test_no_survey_permission_handler(self):
        error = NoSurveyPermission('party_id', 'case_id', 'case_party_id')

        with self.assertLogs() as cm:
            response, code = no_survey_permission(error)

        self.assertIn('WARNING', cm[1][0])
        self.assertIn('"party_id": "party_id"', cm[1][0])
        self.assertIn('"case_id": "case_id"', cm[1][0])
        self.assertIn("message", response)
        self.assertIn("party_id", response)
        self.assertIn("case_id", response)
        self.assertIn("case_party_id", response)
        self.assertEqual(403, code)
