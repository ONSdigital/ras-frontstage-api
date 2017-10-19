import unittest
from unittest.mock import MagicMock

from frontstage_api.decorators.jwt_decorators import get_jwt
from frontstage_api.exceptions.exceptions import NoJWTError


class TestDecorators(unittest.TestCase):

    @staticmethod
    def decorator_test(request):
        @get_jwt(request)
        def test_function(encoded_jwt):
            pass
        test_function()

    def test_get_jwt(self):
        request = MagicMock()

        # This test passes if no exceptions are raised
        self.decorator_test(request)

    def test_get_jwt_no_jwt(self):
        request = MagicMock(headers={})

        with self.assertRaises(NoJWTError):
            self.decorator_test(request)
