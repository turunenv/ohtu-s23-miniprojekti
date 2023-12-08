import unittest
from unittest.mock import Mock, ANY, patch, MagicMock, call
from repositories.reference_repository import ReferenceRepository
from app import App
from io import StringIO

class TestApp(unittest.TestCase):
    def setUp(self):
        self._io_mock = Mock()
        self.mock_bibwriter = Mock()
        self._reference_repository_mock = Mock(
            wraps=ReferenceRepository("connection"))
        self.app = App(
            self._io_mock, self._reference_repository_mock, self.mock_bibwriter)
        self.mock_io = Mock()
        self.mock_rs = Mock()
        self.reference_service = Mock()
        self.mock_rs.reference_service = Mock()
        self.testApp = App(self.mock_io, self.mock_rs, self.mock_bibwriter)
        self.testApp.write_columns = Mock()

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
        self.assertEqual(self._io_mock.write.call_count, 16)

    def test_list_references_gets_list(self):
        self.book1 = Mock()
        self.book2 = Mock()
        self.test_list = [self.book1, self.book2]
        self.mock_rs.get_all.return_value = self.test_list
        self.testApp.list_references()

        self.mock_rs.get_all.assert_called()

    def test_list_references_calls_io_write(self):
        self.book1 = Mock()
        self.book2 = Mock()
        self.test_list = [self.book1, self.book2]
        self.mock_rs.get_all.return_value = self.test_list
        self.testApp.list_references()

        self.mock_io.write.assert_called_with(self.test_list[1])

    def test_delete_reference_cancels_when_command_is_given(self):
        self.mock_io.read.return_value = "cancel"
        self.testApp.delete_reference()

        self.mock_rs.ref_key_taken.assert_not_called()

    def test_delete_reference_asks_for_confirmation_and_cancels_when_wrong_input(self):
        self.mock_io.read.return_value = 123
        self.mock_rs.ref_key_taken.return_value = True
        self.mock_rs.get_book_by_ref_key.return_value = "reference"
        self.testApp.delete_reference()

        self.mock_rs.delete_book_by_ref_key.assert_not_called()
        self.mock_io.write.assert_called_with("Deletion cancelled")

    def test_delete_reference_with_wrong_ref_key(self):
        self.mock_io.read.return_value = 123
        self.mock_rs.ref_key_taken.return_value = False
        self.mock_rs.get_book_by_ref_key.return_value = "reference"
        self.testApp.delete_reference()

        self.mock_rs.get_book_by_ref_key.assert_not_called()

    def test_delete_reference_with_acceptable_ref_key(self):
        self.mock_io.read.side_effect = [123, "y"]
        self.mock_rs.ref_key_taken.return_value = True
        self.mock_rs.get_book_by_ref_key.return_value = "reference"
        self.mock_rs.delete_book_by_ref_key.return_value = True
        self.testApp.delete_reference()

        self.mock_rs.delete_book_by_ref_key.assert_called_with(123)
        self.mock_io.write.assert_called_with("DELETED!")

    def test_delete_reference_problem_deleting_from_db(self):
        self.mock_io.read.side_effect = [123, "y"]
        self.mock_rs.ref_key_taken.return_value = True
        self.mock_rs.get_book_by_ref_key.return_value = "reference"
        self.mock_rs.delete_book_by_ref_key.return_value = False
        self.testApp.delete_reference()

        self.mock_rs.delete_book_by_ref_key.assert_called_with(123)
        self.mock_io.write.assert_called_with(
            "Something went wrong with deleting the reference")

    def test_command_add_calls_add_reference(self):
        self.testApp.add_reference = Mock()
        self.mock_io.read.side_effect = ["add", ""]
        self.testApp.run()

        self.testApp.add_reference.assert_called_once()

    def test_command_delete_calls_delete_reference(self):
        self.testApp.delete_reference = Mock()
        self.mock_io.read.side_effect = ["delete", ""]
        self.testApp.run()

        self.testApp.delete_reference.assert_called_once()

    def test_command_list_calls_delete_references(self):
        self.testApp.list_references = Mock()
        self.mock_io.read.side_effect = ["list", ""]
        self.testApp.run()

        self.testApp.list_references.assert_called_once()

    def test_add_reference(self):
        self.testApp.io.read.side_effect = [
            'book', "ref", "auth", "title", "1999", "publisher"]
        self.testApp.reference_service.ref_key_taken.return_value = False
        self.testApp.reference_service.get_fields_of_reference_type.return_value = [
            "ref_key", "author", "title", "year", "publisher"]
        self.testApp.reference_service.create_reference.return_value = True
        self.testApp.add_reference()

        self.testApp.reference_service.get_fields_of_reference_type.assert_called_with(
            'book')
        self.testApp.reference_service.create_reference.assert_called_with(
            {'type': 'book', 'ref_key': 'ref', 'author': 'auth', 'title': 'title', 'year': '1999', 'publisher': 'publisher'})

    def test_add_reference_with_empty_user_input(self):
        self.mock_io.read.side_effect = ["book", " ", "aa"]
        self.mock_rs.get_fields_of_reference_type.return_value = ["title"]
        self.mock_rs.create_reference.return_value = False
        self.testApp.add_reference()

        self.mock_io.write.assert_called_with("Invalid input! Please check help-menu for instructions")

    def test_add_reference_with_taken_re_key(self):
        self.mock_io.read.side_effect = ["book", "1", "2"]
        self.mock_rs.get_fields_of_reference_type.return_value = ["ref_key"]
        self.mock_rs.create_reference.return_value = False
        self.mock_rs.ref_key_taken.side_effect = [True, False]
        self.testApp.add_reference()

        self.mock_io.write.assert_called_with(
            "This ref_key is already taken!!")

    def test_add_not_supported_reference_type(self):
        self.mock_io.read.return_value = "Film"
        self.mock_rs.get_fields_of_reference_type.return_value = None
        self.testApp.add_reference()

        self.mock_io.write.assert_called_with(
            "ERROR: Source type not supported!")

    def test_add_method_cancel_works(self):
        self.mock_io.read.side_effect = ["cancel", "book", "cancel",
                                         "book", "1", "cancel", "book", "", "cancel"]
        self.mock_rs.get_fields_of_reference_type.return_value = ["ref_key"]
        self.mock_rs.ref_key_taken.side_effect = [True, False]
        self.testApp.add_reference()

        self.mock_rs.get_fields_of_reference_type.assert_not_called()

        self.testApp.add_reference()

        self.testApp.add_reference()
        self.mock_io.write.assert_called_with(
            "This ref_key is already taken!!")

        self.testApp.add_reference()
        self.mock_io.write.assert_called_with("Invalid input! Please check help-menu for instructions")

    def test_write_columns_works(self):
        reference_mock = Mock()
        reference_mock.get_field_names.return_value = ["Title ", "Author "]
        reference_mock.get_field_lengths.return_value = [2, 2]

        expected = "\nTitle  Author  "
        self.app.write_columns(reference_mock)
        calls = [call(expected), call(f'{"":{"-"}>115}')]
        self._io_mock.write.assert_has_calls(calls)

    def test_create_bib_file_cancels(self):
        self.mock_io.read.return_value = ""
        self.testApp.create_bib_file()

        self.mock_io.write.assert_called_with("File creation cancelled")

    def test_create_bib_file_works(self):
        self.mock_io.read.return_value = "test"
        self.mock_rs.get_all.return_value = ["1"]
        self.mock_bibwriter.write_references_to_file.return_value = True
        self.testApp.create_bib_file()

        self.mock_bibwriter.write_references_to_file.assert_called_with("test.bib", [
                                                                        "1"])
        self.mock_io.write.assert_called_with(
            "1 references succesfully written to test.bib")

    def test_create_bib_file_fails(self):
        self.mock_io.read.return_value = "test.bib"
        self.mock_rs.get_all.return_value = ["1"]
        self.mock_bibwriter.write_references_to_file.return_value = False
        self.testApp.create_bib_file()

        self.mock_io.write.assert_called_with(
            "There was an error creating file test.bib.")
        
    def test_validate_input_works_with_year(self):
        self.field = "year"
        self.user_input = "1233"
        val = self.testApp.validate_input(self.field, self.user_input)
        self.assertIsNotNone(val)

    def test_validate_input_fails_with_year(self):
        self.field = "year"
        self.user_input = "1930's"
        val = self.testApp.validate_input(self.field, self.user_input)
        self.assertIsNone(val)

    def test_validate_input_works_with_volume(self):
        self.field = "volume"
        self.user_input = "1"
        val = self.testApp.validate_input(self.field, self.user_input)
        self.assertIsNotNone(val)

    def test_validate_input_fails_with_volume(self):
        self.field = "volume"
        self.user_input = "9th"
        val = self.testApp.validate_input(self.field, self.user_input)
        self.assertIsNone(val)

    def test_validate_input_works_with_pages(self):
        self.field = "pages"
        self.user_input = "12--33"
        val = self.testApp.validate_input(self.field, self.user_input)
        self.assertIsNotNone(val)

    def test_validate_input_fails_with_pages(self):
        self.field = "pages"
        self.user_input = "12-33"
        val = self.testApp.validate_input(self.field, self.user_input)
        self.assertIsNone(val)