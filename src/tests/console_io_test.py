import unittest
from unittest.mock import patch
from io import StringIO
from console_io import ConsoleIO

class TestConsole(unittest.TestCase):
    def setUp(self):
        self.test_console = ConsoleIO()

    def test_print_to_terminal(self):
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            #makes a mock of pythons standard output file to read data
            self.test_console.write("Hello world!")

            printed_output = mock_stdout.getvalue().strip()

            self.assertEqual(printed_output, "Hello world!")

    @patch('builtins.input', return_value='Goodbye world!') 
    #makes a mock of pythons own input
    def test_read(self, mock_input):
        result = self.test_console.read("Enter something: ")
        self.assertEqual(result, 'Goodbye world!')