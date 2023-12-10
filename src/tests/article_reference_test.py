import unittest
from entities.book_reference import BookReference
from services.reference_service import ReferenceService


class FakeReferenceRepository:
    def __init__(self):
        self.references = []

    def get_all(self):
        return self.references

    def create_article(self, article):
        self.references.append(article)
        return article

    def delete_all(self):
        self.references = []

    def get_book_by_ref_key(self, ref_key):
        return True

    def delete_book_by_ref_key(self, ref_key):
        return True

class TestArticleReference(unittest.TestCase):
    def setUp(self):
        self.reference_service = ReferenceService(FakeReferenceRepository())
        self.test_article = {}
        self.test_article["type"] = "article"
        self.test_article["ref_key"] = "CBH91"
        self.test_article["author"] = "Allan Collins et al"
        self.test_article["title"] = "Cognitive apprenticeship"
        self.test_article["journal"] = "American Educator"
        self.test_article["year"] = "1991"
        self.test_article["volume"] = "6"
        self.test_article["pages"] = "38--46"
        self.reference_service.create_reference(self.test_article)

    def test_get_field_names(self):
       ref_list = self.reference_service.get_all()
       for ref in ref_list:
           fields = ref.get_field_names()

       self.assertEqual(fields, ["REF_KEY", "AUTHOR",
                        "TITLE", "JOURNAL",  "YEAR",
                        "VOLUME", "PAGES"])

    def test_get_field_lengths(self):
        ref_list = self.reference_service.get_all()
        for ref in ref_list:
            field_lengths = ref.get_field_lengths()

        self.assertEqual(field_lengths, [10, 25, 25, 25, 6, 6, 6])

    def test__str__(self):
        reference_list = self.reference_service.get_all()
        expected_article = reference_list[0]
        string = expected_article.__str__()

        expected_article_string = (
            "CBH91      Allan Collins et al       Cognitive apprenticeship  American Educator         1991   6      38--46  ")

        self.assertEqual(string, expected_article_string)

    def test__str__if_author_length_more_than_25(self):
        self.test_article["author"] = "Allan Collins and John Seely Brown and Ann Holum"
        self.reference_service.create_reference(self.test_article)
        reference_list = self.reference_service.get_all()
        expected_article = reference_list[1]
        string = expected_article.__str__()

        expected_article_string = (
            "CBH91      Allan Collins and John Se Cognitive apprenticeship  American Educator         1991   6      38--46  \n            ely Brown and Ann Holum                            ")

        self.assertEqual(string, expected_article_string)

    def test__str__if_title_length_more_than_25(self):
        self.test_article["title"] = "Cognitive apprenticeship: making thinking visible"
        self.test_article["author"] = "Allan Collins et al"
        self.reference_service.create_reference(self.test_article)
        reference_list = self.reference_service.get_all()
        expected_article = reference_list[1]
        string = expected_article.__str__()

        expected_article_string = (
            "CBH91      Allan Collins et al       Cognitive apprenticeship: American Educator         1991   6      38--46  \n                                       making thinking visible ")

        self.assertEqual(string, expected_article_string)

