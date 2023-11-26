import unittest
from unittest.mock import Mock, ANY
from repositories.reference_repository import ReferenceRepository
from app import App


class TestApp(unittest.TestCase):
    def setUp(self):
        self._io_mock = Mock()
        self._reference_repository_mock = Mock(
            wraps=ReferenceRepository("connection"))
        self.app = App(self._io_mock, self._reference_repository_mock)

    def test_app_creates_empty_list(self):
        self.assertEqual(len(self.app.list), 0)

    def test_run_stops_with_enter(self):
        self._io_mock.read.return_value = ""
        self.app.run()
        self._io_mock.write.assert_called_with(ANY)
        self._io_mock.write.assert_called_with(ANY)

    def test_run_help_works(self):
        self._io_mock.read.side_effect = ["help", ""]
        self.app.run()
        self._io_mock.write.assert_called_with(ANY)
        self._io_mock.write.assert_called_with(ANY)

        # help list starts here
        self._io_mock.write.assert_called_with(ANY)
        self._io_mock.write.assert_called_with(ANY)
        self._io_mock.write.assert_called_with(ANY)
        self._io_mock.write.assert_called_with(ANY)
        self._io_mock.write.assert_called_with(ANY)
        self._io_mock.write.assert_called_with(ANY)

        # 2 more calls before ending loop
        self._io_mock.write.assert_called_with(ANY)
        self._io_mock.write.assert_called_with(ANY)
