import unittest
from repositories.reference_repository import ReferenceRepository
from entities.book_reference import BookReference
from database_connection import get_db_connection


repository = ReferenceRepository(get_db_connection())


class TestReferenceRepository(unittest.TestCase):
    def setUp(self):
        repository.delete_all_books()
        self.test_book = BookReference("1", "Pekka", "Kokeilua",
                                       2002, "OTA")

    def test_create_book_works_with_valid_input(self):
        success = repository.create_book(self.test_book)

        self.assertTrue(success)

    def test_create_book_fails_with_invalid_input(self):
        success = repository.create_book("Not a book")
        print(success)
        self.assertFalse(success)

    def test_get_all_returns_list(self):
        repository.create_book(self.test_book)

        books = repository.get_all()
        expected_book = books[0]

        self.assertEqual(expected_book.ref_key, self.test_book.ref_key)
        self.assertEqual(expected_book.author, self.test_book.author)
        self.assertEqual(expected_book.title, self.test_book.title)
        self.assertEqual(expected_book.year, self.test_book.year)
        self.assertEqual(expected_book.publisher, self.test_book.publisher)

    def test_delete_all_books_works(self):
        repository.create_book(self.test_book)
        repository.delete_all_books()

        books = repository.get_all()

        self.assertEqual(len(books), 0)

    def test_delete_book_with_valid_ref_key(self):
        repository.create_book(self.test_book)
        success = repository.delete_book_by_ref_key("1")

        self.assertTrue(success)

    def test_delete_book_with_invalid_ref_key(self):
        success = repository.delete_book_by_ref_key("1")

        self.assertFalse(success)

    def test_get_book_by_ref_key_creates_correct_book_class(self):
        repository.create_book(self.test_book)
        fetched_book = repository.get_book_by_ref_key("1")

        ref_key = fetched_book.ref_key
        author = fetched_book.author
        title = fetched_book.title
        year = fetched_book.year
        publisher = fetched_book.publisher

        self.assertEqual(ref_key, self.test_book.ref_key)
        self.assertEqual(author, self.test_book.author)
        self.assertEqual(title, self.test_book.title)
        self.assertEqual(year, self.test_book.year)
        self.assertEqual(publisher, self.test_book.publisher)

    def test_get_book_returns_none_if_book_not_foun(self):
        fetched_book = repository.get_book_by_ref_key("1")

        self.assertIsNone(fetched_book)
