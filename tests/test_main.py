import unittest
import sys
from io import StringIO
from unittest.mock import patch
from __init__ import path
from main import main


class TestMain(unittest.TestCase):
    @patch('sys.stderr', new_callable=StringIO)
    @patch('sys.argv', new=['main.py'])
    
    def test_incomplete_parsing1(self, mock_stderr):
        with self.assertRaises(SystemExit):
            main()
        self.assertIn('error: the following arguments are required: create', mock_stderr.getvalue())
    
    @patch('sys.stderr', new_callable=StringIO)
    @patch('sys.argv', new=['main.py', 'create'])

    def test_incomplete_parsing2(self, mock_stdout):
        with self.assertRaises(AttributeError):
            main()
        self.assertIn('A flag should be selected when the subcommand create is used, see: python3 main.py create -h', mock_stdout.getvalue())




unittest.main()