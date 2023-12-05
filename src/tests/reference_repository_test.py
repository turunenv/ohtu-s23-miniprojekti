import unittest
from repositories.reference_repository import ReferenceRepository
from entities.book_reference import BookReference
from entities.article_reference import ArticleReference
from database_connection import get_db_connection


repository = ReferenceRepository(get_db_connection())


class TestReferenceRepository(unittest.TestCase):
    def setUp(self):
        repository.delete_all_books()
        self.test_book = BookReference("1", "Pekka", "Kokeilua",
                                       2002, "OTA")
        self.test_article = ArticleReference("2", "Matti",
                                             "Cool article",
                                             "journal", 2023,
                                             "vol 3", "56-62")

    def test_create_book_works_with_valid_input(self):
        success = repository.create_book(self.test_book)

        self.assertTrue(success)

    def test_create_book_fails_with_invalid_input(self):
        success = repository.create_book("Not a book")
        print(success)
        self.assertFalse(success)

    def test_get_all_returns_list(self):
        repository.create_book(self.test_book)
        repository.create_article(self.test_article)

        references = repository.get_all()
        expected_book = references[0]
        expected_article = references[1]

        self.assertEqual(expected_book.ref_key, self.test_book.ref_key)
        self.assertEqual(expected_book.author, self.test_book.author)
        self.assertEqual(expected_book.title, self.test_book.title)
        self.assertEqual(expected_book.year, self.test_book.year)
        self.assertEqual(expected_book.publisher, self.test_book.publisher)
        self.assertEqual(expected_article.ref_key, self.test_article.ref_key)
        self.assertEqual(expected_article.author, self.test_article.author)

    def test_delete_all_books_works(self):
        repository.create_book(self.test_book)
        repository.create_article(self.test_article)
        repository.delete_all_books()

        references = repository.get_all()

        self.assertEqual(len(references), 0)

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

    def test_get_book_returns_none_if_book_not_found(self):
        fetched_book = repository.get_book_by_ref_key("1")

        self.assertIsNone(fetched_book)

    def test_create_article_works_with_valid_input(self):
        success = repository.create_article(self.test_article)

        self.assertTrue(success)

    def test_create_article_fails_with_invalid_input(self):
        success = repository.create_article("Not an article")

        self.assertFalse(success)
    
    def test_delete_by_ref_key_deletes_only_wanted(self):
        repository.create_article(self.test_article)
        repository.create_book(self.test_book)

        references = repository.get_all()
        expected_article = references[0]
        expected_book_1 = references[1]

        repository.delete_book_by_ref_key("1")

        references = repository.get_all()
        expected_book_2 = references[0]

        self.assertNotEqual(expected_book_2, expected_article)
        self.assertNotEqual(expected_book_2, expected_book_1)

    def test_get_book_by_ref_key_creates_article_when_ref_is_article_type(self):
        repository.create_article(self.test_article)
        fetched_reference = repository.get_book_by_ref_key("2")

        ref_key = fetched_reference.ref_key
        author = fetched_reference.author
        title = fetched_reference.title

        self.assertEqual(ref_key, self.test_article.ref_key)
        self.assertEqual(author, self.test_article.author)
        self.assertEqual(title, self.test_article.title)
