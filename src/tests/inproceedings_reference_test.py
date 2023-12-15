import unittest
from entities.reference import Reference
from entities.inproceedings_reference import InProceedingsReference

class TestInProceedingsReference(unittest.TestCase):
    def setUp(self):
        self.test_inproceedings = InProceedingsReference(
            "aaa", "tove jansson", "muumit", 
            "muumilaakso", 2000
            )
        self.test_inproceedings_with_long_author = InProceedingsReference(
            "aaa", "tove jansson and all the other authors", "muumit", 
            "muumilaakso", 2000
            )
        self.test_inproceedings_with_long_ref_key = InProceedingsReference(
            "very_long_ref_key", "tove jansson", "muumit", 
            "muumilaakso", 200
            )

    def test_get_field_names_returns_all_names(self):
        field_names = self.test_inproceedings.get_field_names()
        self.assertEqual(len(field_names), 5)

    def test_get_field_lengths_returns_correct_list(self):
        lengths = self.test_inproceedings.get_field_lengths()
        expected = [10, 25, 25, 25, 6]

        self.assertEqual(lengths, expected)

    def test_string_representation(self):
        str_repr = str(self.test_inproceedings)
        expected_str = "aaa        tove jansson              muumit                    muumilaakso               2000   "

        self.assertEqual(str_repr, expected_str)

    def test_string_representation_with_long_author_works(self):
        str_repr = self.test_inproceedings_with_long_author.__str__()
        expected_str = "aaa        tove jansson and all the  muumit                    muumilaakso               2000   "
        expected_str += "\n           other authors                                                                "

        self.assertEqual(str_repr, expected_str)

    def test_string_representation_with_long_ref_key_works(self):
        str_repr = self.test_inproceedings_with_long_ref_key.__str__()
        expected_str = "very_long_ tove jansson              muumit                    muumilaakso               2000   "
        expected_str += "\nref_key                                                                                 "
