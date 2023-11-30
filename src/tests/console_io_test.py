import unittest
from unittest.mock import patch
from io import StringIO
from console_io import ConsoleIO

class TestConsole(unittest.TestCase):
    def setUp(self):
        self.test_console = ConsoleIO()

    def test_print_to_terminal(self):
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            self.test_console.write("Hello, world!")

            printed_output = mock_stdout.getvalue().strip()

            self.assertEqual(printed_output, "Hello, world!")
    
    def test_io_read(self):
        todo=''