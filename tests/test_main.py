import unittest
from __init__ import path
import io
import contextlib
from main import parser


class TestPrimaryParsing(unittest.TestCase):


    def __init__(self, methodName = "runTest"):
        self.f = io.StringIO()
        super().__init__(methodName)


    # empty command line
    def test_empty_parsing1(self):
        with self.assertRaises(SystemExit) as cm, contextlib.redirect_stderr(self.f):
            parser('')
        self.assertEqual(cm.exception.code, 2)
        self.assertEqual(self.f.getvalue() , 'usage: test_main.py [options]\ntest_main.py: error: the following arguments are required: create\n')


    def test_invalid_parsing(self):
        with self.assertRaises(SystemExit) as cm, contextlib.redirect_stderr(self.f):
            parser(['Bad_Parsing'])
        self.assertEqual(cm.exception.code, 2)
        self.assertEqual(self.f.getvalue(), 'usage: test_main.py [options]\ntest_main.py: error: argument create: invalid choice: \'Bad_Parsing\' (choose from \'create\')\n')

    

class TestCreateParsing(unittest.TestCase):
    

    def __init__(self, methodName = "runTest"):
        self.f = io.StringIO()
        super().__init__(methodName)


    # no flag with create argument
    def test_empty_parsing(self):
        with self.assertRaises(AttributeError) as cm:
            parser(['create'])
        self.assertEqual(cm.exception.args[0], 'A flag should be selected when the subcommand create is used, see: python3 main.py create -h')


    # invalid flag
    def test_empty_create(self):
        with self.assertRaises(SystemExit) as cm, contextlib.redirect_stderr(self.f):
            parser(['create', '--my-invalid-flag'])
        self.assertEqual(cm.exception.code, 2)
        self.assertEqual(self.f.getvalue(), 'usage: test_main.py [options]\ntest_main.py: error: unrecognized arguments: --my-invalid-flag\n')


    def test_empty_str_flag(self):
        with self.assertRaises(SystemExit) as cm, contextlib.redirect_stderr(self.f):
            parser(['create', '-s'])
        self.assertEqual(cm.exception.code, 2)
        self.assertEqual(self.f.getvalue(), '''usage: test_main.py [options] create [-h] [-s Int | -d Int, str [Int, str ...]]\ntest_main.py [options] create: error: argument -s/--string: expected one argument\n''')
     
unittest.main()