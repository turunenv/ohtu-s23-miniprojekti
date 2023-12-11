import unittest
from entities.book_reference import BookReference
from services.reference_service import ReferenceService


class FakeReferenceRepository:
    def __init__(self):
        self.references = []

    def get_all(self):
        return self.references

    def create_book(self, book):
        self.references.append(book)
        return book

    def delete_all(self):
        self.references = []

    def get_reference_by_ref_key(self, ref_key):
        return True

    def delete_book_by_ref_key(self, ref_key):
        return True


class TestBookReference(unittest.TestCase):
    def setUp(self):
        self.reference_service = ReferenceService(FakeReferenceRepository())
        self.test_book = {}
        self.test_book["type"] = "book"
        self.test_book["ref_key"] = "KEY"
        self.test_book["author"] = "test_author"
        self.test_book["title"] = "test_title"
        self.test_book["year"] = "2023"
        self.test_book["publisher"] = "OTA"
        self.reference_service.create_reference(self.test_book)

        self.test_book2 = {}
        self.test_book2["type"] = "book"
        self.test_book2["ref_key"] = "KEY2"
        self.test_book2["author"] = "test_author_with_long_name"
        self.test_book2["title"] = "test_title2"
        self.test_book2["year"] = "2023"
        self.test_book2["publisher"] = "OTA"
        self.reference_service.create_reference(self.test_book2)

        self.test_book3 = {}
        self.test_book3["type"] = "book"
        self.test_book3["ref_key"] = "KEY3"
        self.test_book3["author"] = "test_author"
        self.test_book3["title"] = "test_title_with_too_long_name_it_cant_fit"
        self.test_book3["year"] = "2023"
        self.test_book3["publisher"] = "OTA"
        self.reference_service.create_reference(self.test_book3)

    def test_get_field_names(self):
        ref_list = self.reference_service.get_all()
        for ref in ref_list:
            fields = ref.get_field_names()

        self.assertEqual(fields, ["REF_KEY", "AUTHOR",
                         "TITLE", "YEAR", "PUBLISHER"])

    def test_get_field_lengths(self):
        ref_list = self.reference_service.get_all()
        for ref in ref_list:
            field_lengths = ref.get_field_lengths()

        self.assertEqual(field_lengths, [10, 25, 35, 6, 15])

    def test__str__(self):
        reference_list = self.reference_service.get_all()
        expected_book = reference_list[0]
        string = expected_book.__str__()

        expected_book_string = (
            "KEY        test_author               test_title                          2023   OTA            ")

        self.assertEqual(string, expected_book_string)

    def test__str__if_author_length_more_than_25(self):
        reference_list = self.reference_service.get_all()
        expected_book = reference_list[1]
        string = expected_book.__str__()

        expected_book_string = (
            "KEY2       test_author_with_long_nam test_title2                         2023   OTA            \n           e                                                            ")

        self.assertEqual(string, expected_book_string)

    def test__str__if_title_length_more_than_35(self):
        reference_list = self.reference_service.get_all()
        expected_book = reference_list[2]
        string = expected_book.__str__()

        expected_book_string = (
            f"KEY3       test_author               test_title_with_too_long_name_it_ca 2023   OTA            \n                                     nt_fit                             ")

        self.assertEqual(string, expected_book_string)
