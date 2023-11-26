import unittest
from app import App


class TestApp(unittest.TestCase):
    def setUp(self):
        self.testApp = App(io=0, rs=0)

    def test_app_creates_empty_list(self):
        self.assertEqual(len(self.testApp.list), 0)
