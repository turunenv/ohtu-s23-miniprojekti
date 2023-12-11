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
        success = repository.delete_reference_by_ref_key("1")

        self.assertTrue(success)

    def test_delete_book_with_invalid_ref_key(self):
        success = repository.delete_reference_by_ref_key("1")

        self.assertFalse(success)

    def test_get_reference_by_ref_key_creates_correct_book_class(self):
        repository.create_book(self.test_book)
        fetched_book = repository.get_reference_by_ref_key("1")

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
        fetched_book = repository.get_reference_by_ref_key("1")

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

        repository.delete_reference_by_ref_key("1")

        references = repository.get_all()
        expected_book_2 = references[0]

        self.assertNotEqual(expected_book_2, expected_article)
        self.assertNotEqual(expected_book_2, expected_book_1)

    def test_get_reference_by_ref_key_creates_article_when_ref_is_article_type(self):
        repository.create_article(self.test_article)
        fetched_reference = repository.get_reference_by_ref_key("2")

        ref_key = fetched_reference.ref_key
        author = fetched_reference.author
        title = fetched_reference.title

        self.assertEqual(ref_key, self.test_article.ref_key)
        self.assertEqual(author, self.test_article.author)
        self.assertEqual(title, self.test_article.title)

    def test_create_and_get_tag_id_works(self):
        test_tag = "Chemistry"
        succes = repository.create_tag(test_tag)

        self.assertTrue(succes)

        tag_id = repository.get_tag_id(test_tag)
        self.assertEqual(tag_id, 1)

        no_tag_id = repository.get_tag_id("NA")
        self.assertIsNone(no_tag_id)

    def test_create_tag_relation_works(self):
        tag_id = 1
        ref_key = "abc"
        success = repository.create_tag_relation(tag_id, ref_key)

        self.assertTrue(success)

    def test_create_tag_relation_fails_with_duplicate_tag(self):
        tag_id = 1
        ref_key = "1"
        first_add = repository.create_tag_relation(tag_id, ref_key)

        self.assertTrue(first_add)

        second_try = repository.create_tag_relation(tag_id, ref_key)

        self.assertFalse(second_try)

    def test_get_tagged_returns_correct_list(self):
        testbook2 = BookReference(
                                "3",
                                "So",
                                "Testin2",
                                2010,
                                "OTAWA"
        )

        testarticle2 = ArticleReference(
                                "4",
                                "Matt Smith",
                                "Wowzie",
                                "journal2",
                                2011,
                                1,
                                "10-12"
        )

        repository.create_book(self.test_book)
        repository.create_article(self.test_article)
        repository.create_book(testbook2)
        repository.create_article(testarticle2)

        repository.create_tag_relation(1, "3")
        repository.create_tag_relation(1, "4")

        searched_tags = repository.get_tagged(1)

        expected_book = searched_tags[0]
        expected_article = searched_tags[1]

        self.assertEqual(expected_book.title, testbook2.title)
        self.assertEqual(expected_article.author, testarticle2.author)
