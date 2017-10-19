import unittest

from frontstage_api import app


class TestSecureMessaging(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_info_no_git_info(self):
        response = self.app.get("/info")

        self.assertEqual(response.status_code, 200)
        self.assertTrue('"name": "ras-frontstage-api"'.encode() in response.data)

    def test_info_with_git_info(self):
        response = self.app.get("/info")

        self.assertEqual(response.status_code, 200)
        self.assertTrue('"name": "ras-frontstage-api"'.encode() in response.data)
        self.assertTrue('"test": "test"'.encode() in response.data)