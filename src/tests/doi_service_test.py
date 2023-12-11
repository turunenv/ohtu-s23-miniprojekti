import unittest
from unittest.mock import MagicMock, Mock, patch
from services.doi_service import DOIService
from requests.exceptions import HTTPError

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
            "type": "journal-article",
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
        
    def test_create_book_works_with_no_author(self):
        del self.data1["author"]
        book = self.doi_service.create_book(self.data1, "REF1")
        self.assertEqual(book, {"type": "book",
            "ref_key": "REF1",
            "author": "Undefined",
            "title": "Fahrenheit 451",
            "year": "1976",
            "publisher": "Grafton"})

    def test_create_article_works(self):
        article = self.doi_service.create_article(self.data2, "REF2")
        expected = {
            "type": "article",
            "ref_key": "REF2",
            "author": "Silva, Shannon M. and Lambert, Carolyn G.",
            "title": "Restorative Justice Legislation...",
            "year": "2015",
            "volume": '14',
            "journal": "Informa UK Limited",
            "pages": "77--95"
            }
        self.assertEqual(article, expected)

    def test_create_article_works_with_container_title(self):
        del self.data2["publisher"]
        self.data2["container-title"] = "Informa UK Limited"
        article = self.doi_service.create_article(self.data2, "REF2")
        expected = {
            "type": "article",
            "ref_key": "REF2",
            "author": "Silva, Shannon M. and Lambert, Carolyn G.",
            "title": "Restorative Justice Legislation...",
            "year": "2015",
            "volume": '14',
            "journal": "Informa UK Limited",
            "pages": "77--95"
            }
        self.assertEqual(article, expected)

    def test_resolve_url_works_with_identifier(self):
        url = self.doi_service.resolve_url("10.1093/ajae/aaq063")
        self.assertEqual(url, "https://doi.org/10.1093/ajae/aaq063")
    
    def test_resolve_url_works_with_full_url(self):
        original = "https://doi.org/10.1016/b978-0-12-326460-2.x5000-7"
        url = self.doi_service.resolve_url("https://doi.org/10.1016/b978-0-12-326460-2.x5000-7")
        self.assertEqual(url, original)

    @patch('services.doi_service.DOIService.retrieve_data')
    def test_get_doi_works_for_book(self, mock_retrieve_data):
        mock_retrieve_data.return_value = self.data1
        book = self.doi_service.get_doi("any_url", "ref1")
        expected = {
            "type": "book",
            "ref_key": "ref1",
            "author": "Bradbury, Ray",
            "title": "Fahrenheit 451",
            "year": "1976",
            "publisher": "Grafton"
        }
        self.assertEqual(book, expected)

    @patch('services.doi_service.DOIService.retrieve_data')
    def test_get_doi_works_for_article(self, mock_retrieve_data):
        mock_retrieve_data.return_value = self.data2
        article = self.doi_service.get_doi("any_url", "REF2")
        expected = {
            "type": "article",
            "ref_key": "REF2",
            "author": "Silva, Shannon M. and Lambert, Carolyn G.",
            "title": "Restorative Justice Legislation...",
            "year": "2015",
            "volume": '14',
            "journal": "Informa UK Limited",
            "pages": "77--95"
            }
        self.assertEqual(article, expected)

    @patch('services.doi_service.DOIService.retrieve_data')
    def test_get_doi_fails_unsupported_reference_type(self, mock_retrieve_data):
        mock_retrieve_data.return_value = {"type": "wrong"}
        self.doi_service.get_doi("any_url", "ref1")
        self.mock_io.write.assert_called_with("This reference type is not supported")
    
    @patch('services.doi_service.DOIService.retrieve_data')
    def test_get_doi_fails_key_error(self, mock_retrieve_data):
        mock_retrieve_data.return_value = {"key": "error"}
        self.doi_service.get_doi("any_url", "ref1")
        self.mock_io.write.assert_called_with(f'{" ":<4}Some necessary information was missing')

    @patch('services.doi_service.DOIService.retrieve_data')
    def test_get_doi_return_empty(self, mock_retrieve_data):
        mock_retrieve_data.return_value = {}
        book = self.doi_service.get_doi("any_url", "ref1")
        self.assertEqual(book, {})
    
    @patch('services.doi_service.requests')
    def test_retrieve_data_works(self, mock_requests):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = self.data2
        mock_requests.get.return_value = mock_response

        data = self.doi_service.retrieve_data("any_url")
        expected = {
            "type": "journal-article",
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
        self.assertEqual(data, expected)

    def test_retrieve_data_fails_unexpected(self):
        self.doi_service.retrieve_data("any_url")
        self.mock_io.write.assert_called_with("There was an unexpected network error")

    def test_retrieve_data_fails_http(self):
        self.doi_service.retrieve_data("https://doi.org/10.101ss6/b978-0-12-326460-2.x5000-7")
        self.mock_io.write.assert_called_with('DOI not found')