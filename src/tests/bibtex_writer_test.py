import unittest
from unittest.mock import Mock
from bibtex_writer import BibTexWriter
from entities.book_reference import BookReference


class TestBibTexWriter(unittest.TestCase):
    def setUp(self):
        self.file_io = Mock()
        self.bibtex_writer = BibTexWriter(self.file_io)

        book1 = BookReference("aaa", "Irving", "test1", 1999, "tammi")
        book2 = BookReference("bbb", "Virtanen", "test2", 1999, "tammi")

        self.references = [book1, book2]

    def test_write_references_to_file_calls_file_io_write_the_correct_amount(self):
        self.bibtex_writer.write_references_to_file("test.bib", self.references)

        self.assertEqual(self.file_io.write.call_count, 2)

    def test_write_references_to_file_with_overwrite_only_overwrites_once(self):
        self.bibtex_writer.write_references_to_file("test.bib", self.references, over_write=True)

        self.file_io.write.assert_any_call("test.bib", self.references[0].create_bib_string(), True)
        self.file_io.write.assert_called_with("test.bib", self.references[1].create_bib_string(), False)

    def test_write_references_to_file_returns_false_on_os_error(self):
        def side_effect(*args):
            raise OSError
        
        self.file_io.write = Mock(side_effect=side_effect)

        ret_val = self.bibtex_writer.write_references_to_file("test.bib", self.references)

        self.assertEqual(ret_val, False)