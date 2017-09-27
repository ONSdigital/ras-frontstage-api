import unittest

from frontstage_api import app


class TestApplication(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_get(self):
        response = self.app.get("/")
        self.assertEqual(response.status_code, 200)
