import unittest
from unittest.mock import Mock
from services.doi_service import DOIService

class TestDOIService(unittest.TestCase):
    def setUp(self):
        self.mock_io = Mock()
        self.data1 = {
            "type": "book",
            "author": [{"given": "Ray", "family": "Bradbury"}],
            "title": "Fahrenheit 451",
            "other_data": "10231824",
            "more_data": [{"1": "a", "2": "b"}],
            "published": {"date-parts":[[1976, 12, 4]]},
            "publisher": "Grafton"
        }
        self.data2 = {
            "type": "article",
            "author": [{"given": "Shannon M.", "family": "Silva"},
                       {"given": "Carolyn G.", "family": "Lambert"}],
            "title": "Restorative Justice Legislation...",
            "other_data": "10231824",
            "more_data": [{"1": "a", "2": "b"}],
            "published": {"date-parts":[[2015]]},
            "volume": '14',
            "publisher": "Informa UK Limited",
            "page": "77-95"
        }
        self.doi_service = DOIService(self.mock_io)

    def test_create_book_works(self):
        book = self.doi_service.create_book(self.data1, "REF1")
        self.assertEqual(book, {"type": "book",
            "ref_key": "REF1",
            "author": "Bradbury, Ray",
            "title": "Fahrenheit 451",
            "year": "1976",
            "publisher": "Grafton"})

    def test_create_article_works(self):
        article = self.doi_service.create_article(self.data2, "REF2")
        print(article)
        self.assertEqual(article, {"type": "article",
            "ref_key": "REF2",
            "author": "Silva, Shannon M. and Lambert, Carolyn G.",
            "title": "Restorative Justice Legislation...",
            "year": "2015",
            "volume": '14',
            "journal": "Informa UK Limited",
            "pages": "77--95"})

    def test_resolve_url_works_with_identifier(self):
        url = self.doi_service.resolve_url("10.1093/ajae/aaq063")
        self.assertEqual(url, "http://doi.org/10.1093/ajae/aaq063")
    
    def test_resolve_url_works_with_full_url(self):
        original = "https://doi.org/10.1016/b978-0-12-326460-2.x5000-7"
        url = self.doi_service.resolve_url("https://doi.org/10.1016/b978-0-12-326460-2.x5000-7")
        self.assertEqual(url, original)