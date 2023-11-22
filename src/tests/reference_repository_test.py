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

    def test_delet_all_books_works(self):
        repository.create_book(self.test_book)
        repository.delete_all_books()

        books = repository.get_all()

        self.assertEqual(len(books), 0)
