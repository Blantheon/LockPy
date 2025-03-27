import unittest
from __init__ import path
import io
from argparse import ArgumentError
import contextlib
from sys import argv
from main import parser


class TestPrimaryParsing(unittest.TestCase):


    def __init__(self, methodName = "runTest"):
        self.f = io.StringIO()
        super().__init__(methodName)


    # empty command line
    def test_empty_parsing(self):
        with self.assertRaises(SystemExit) as cm, contextlib.redirect_stderr(self.f):
            parser('')
        self.assertEqual(cm.exception.code, 2)
        self.assertEqual(self.f.getvalue() , f'usage: {argv[0]} [options]\n{argv[0]}: error: the following arguments are required: create\n')


    # invalvalid parameter
    def test_invalid_parsing(self):
        with self.assertRaises(SystemExit) as cm, contextlib.redirect_stderr(self.f):
            parser(['Bad_Parsing'])
        self.assertEqual(cm.exception.code, 2)
        self.assertEqual(self.f.getvalue(), f'usage: {argv[0]} [options]\n{argv[0]}: error: argument create: invalid choice: \'Bad_Parsing\' (choose from \'create\')\n')

    

class TestCreateParsing(unittest.TestCase):
    

    def __init__(self, methodName = "runTest"):
        self.f = io.StringIO()
        super().__init__(methodName)


    # no flag with create argument
    def test_empty_create_parsing(self):
        with self.assertRaises(AttributeError) as cm:
            parser(['create'])
        self.assertEqual(cm.exception.args[0], f'A flag should be selected when the subcommand create is used, see: python3 main.py create -h')


    # invalid flag
    def test_create_with_bad_parameter(self):
        with self.assertRaises(SystemExit) as cm, contextlib.redirect_stderr(self.f):
            parser(['create', '--my-invalid-flag'])
        self.assertEqual(cm.exception.code, 2)
        self.assertEqual(self.f.getvalue(), f'usage: {argv[0]} [options]\n{argv[0]}: error: unrecognized arguments: --my-invalid-flag\n')


    # str flag without argument
    def test_empty_str_flag(self):
        with self.assertRaises(SystemExit) as cm, contextlib.redirect_stderr(self.f):
            parser(['create', '-s'])
        self.assertEqual(cm.exception.code, 2)
        self.assertEqual(self.f.getvalue(), f'usage: {argv[0]} [options] create [-h] [-s Int | -d Int, str [Int, str ...]]\n{argv[0]} [options] create: error: argument -s/--string: expected one argument\n')
    

    # dice flag without argument
    def test_empty_dice_flag(self):
        with self.assertRaises(SystemExit) as cm, contextlib.redirect_stderr(self.f):
            parser(['create', '-d'])
        self.assertEqual(cm.exception.code, 2)
        self.assertEqual(self.f.getvalue(), f'usage: {argv[0]} [options] create [-h] [-s Int | -d Int, str [Int, str ...]]\n{argv[0]} [options] create: error: argument -d/--diceware: expected at least one argument\n')


    # str and dice flag together
    def test_str_and_dice_together(self):
        with self.assertRaises(SystemExit) as cm, contextlib.redirect_stderr(self.f):
            parser(['create', '-d', '95', '-s', '120'])
        self.assertEqual(cm.exception.code, 2)
        self.assertEqual(self.f.getvalue(), f'usage: {argv[0]} [options] create [-h] [-s Int | -d Int, str [Int, str ...]]\n{argv[0]} [options] create: error: argument -s/--string: not allowed with argument -d/--diceware\n')
    

    # str flag with a bad argument
    def test_str_bad_argument(self):
        with self.assertRaises(SystemExit) as cm, contextlib.redirect_stderr(self.f):
            parser(['create', '-s', 'string'])
        self.assertEqual(cm.exception.code, 2)
        self.assertEqual(self.f.getvalue(), f'usage: {argv[0]} [options] create [-h] [-s Int | -d Int, str [Int, str ...]]\n{argv[0]} [options] create: error: argument -s/--string: invalid int value: \'string\'\n')


    # str flag with too many arguments
    def test_str_too_many_arguments(self):
        with self.assertRaises(SystemExit) as cm, contextlib.redirect_stderr(self.f):
            parser(['create', '-s', '95', 'string'])
        self.assertEqual(cm.exception.code, 2)
        self.assertEqual(self.f.getvalue(), f'usage: {argv[0]} [options]\n{argv[0]}: error: unrecognized arguments: string\n')

    # too many arguments
    def test_dice_too_many_arguments(self):
        with self.assertRaises(ValueError) as cm:
            parser(['create', '-d', '59', 'string1', 'string2'])
        self.assertEqual(cm.exception.args[0], f'The diceware flag take only one ore two arguments in the following: int, str. See: python3 main.py create -h')


    # dice flag with one bad argument 
    def test_dice_bad_argument(self):
        with self.assertRaises(ValueError) as cm, contextlib.redirect_stderr(self.f):
            parser(['create', '-d', 'string_instead_int'])
        self.assertEqual(cm.exception.args[0], f'The diceware flag should take an int in argument')


    # dice flag with one bad arguments
    def test_dice_bad_arguments(self):
        with self.assertRaises(ValueError) as cm:
            parser(['create', '-d', 'string_instead_int', '95'])
        self.assertEqual(cm.exception.args[0], f'The diceware flag should take an int in first argument')



if __name__ == '__main__':
    argv = ['test_parser.py']
    unittest.main()