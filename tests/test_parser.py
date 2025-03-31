import unittest
from __init__ import path
import io
import contextlib
from sys import argv
from lockpy import parser
LIST_PATH = path[0].replace('modules', 'lists/en.txt')

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
        with self.assertRaises(ValueError) as cm:
            parser(['create'])
        self.assertEqual(cm.exception.args[0], f'A flag with an entropy greater than 0 should be selected when the subcommand create is used, see: python3 main.py create -h')


    # invalid flag
    def test_create_with_bad_parameter(self):
        with self.assertRaises(SystemExit) as cm, contextlib.redirect_stderr(self.f):
            parser(['create', '--my-invalid-flag'])
        self.assertEqual(cm.exception.code, 2)
        self.assertEqual(self.f.getvalue(), f'usage: {argv[0]} [options]\n{argv[0]}: error: unrecognized arguments: --my-invalid-flag\n')

    # str and dice flag together
    def test_str_and_dice_together(self):
        with self.assertRaises(SystemExit) as cm, contextlib.redirect_stderr(self.f):
            parser(['create', '-d', '95', '-s', '120'])
        self.assertEqual(cm.exception.code, 2)
        self.assertEqual(self.f.getvalue(), f'usage: {argv[0]} [options] create [-h] [-s Int | -d Int, str [Int, str ...]]\n{argv[0]} [options] create: error: argument -s/--string: not allowed with argument -d/--diceware\n')
    

class TestStrFlag(unittest.TestCase):

    def __init__(self, methodName = "runTest"):
        self.f = io.StringIO()
        super().__init__(methodName)


    # str flag without argument
    def test_empty_str_flag(self):
        with self.assertRaises(SystemExit) as cm, contextlib.redirect_stderr(self.f):
            parser(['create', '-s'])
        self.assertEqual(cm.exception.code, 2)
        self.assertEqual(self.f.getvalue(), f'usage: {argv[0]} [options] create [-h] [-s Int | -d Int, str [Int, str ...]]\n{argv[0]} [options] create: error: argument -s/--string: expected one argument\n')
    

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
    

    # str flag with 0 entropy
    def test_str_flag_zero_entropy(self):
        with self.assertRaises(ValueError) as cm:
            parser(['create', '-s', '0'])
        self.assertEqual(cm.exception.args[0], 'A flag with an entropy greater than 0 should be selected when the subcommand create is used, see: python3 main.py create -h')


class TestDicewareFlag(unittest.TestCase):

    def __init__(self, methodName = "runTest"):
        self.f = io.StringIO()
        super().__init__(methodName)


    # entropy of 0 with one argument
    def test_dice_zero_entropy_one_argument(self):
        with self.assertRaises(ValueError) as cm:
            parser(['create', '-d', '0'])
        self.assertEqual(cm.exception.args[0], 'The entropy could not be less or equal to zero')


    # entropy of 0 with 2 arguments
    def test_dice_zero_entropy_two_arguments(self):
        with self.assertRaises(ValueError) as cm:
            parser(['create', '-d', '0', 'bad_path'])
        self.assertEqual(cm.exception.args[0], 'The entropy could not be less or equal to zero')

    
    # negative entropy
    def test_dice_negative_entropy(self):
        with self.assertRaises(ValueError) as cm:
            parser(['create', '-d', '-56'])
        self.assertEqual(cm.exception.args[0], 'The diceware flag should take a positive int in first argument')


    #entropy less to 90
    def test_entropy_less_to_90(self):
        with self.assertWarns(UserWarning) as cm:
            resp = parser(['create', '-d', '26'])
        self.assertEqual(str(cm.warning), 'Be careful, for a strong password we recommend using at least 90 bit of entropy')
        self.assertEqual(resp, {'dice': (26, LIST_PATH)})


    # too many arguments
    def test_dice_too_many_arguments(self):
        with self.assertRaises(ValueError) as cm:
            parser(['create', '-d', '59', 'string1', 'string2'])
        self.assertEqual(cm.exception.args[0], f'The diceware flag take only one or two arguments in the following: int, str. See: python3 main.py create -h')


    # dice flag with one bad argument 
    def test_dice_bad_argument(self):
        with self.assertRaises(ValueError) as cm, contextlib.redirect_stderr(self.f):
            parser(['create', '-d', 'string_instead_int'])
        self.assertEqual(cm.exception.args[0], f'The diceware flag should take a positive int in first argument')


    # dice flag without argument
    def test_empty_dice_flag(self):
        with self.assertRaises(SystemExit) as cm, contextlib.redirect_stderr(self.f):
            parser(['create', '-d'])
        self.assertEqual(cm.exception.code, 2)
        self.assertEqual(self.f.getvalue(), f'usage: {argv[0]} [options] create [-h] [-s Int | -d Int, str [Int, str ...]]\n{argv[0]} [options] create: error: argument -d/--diceware: expected at least one argument\n')


    # dice flag with one bad arguments
    def test_dice_bad_arguments(self):
        with self.assertRaises(ValueError) as cm:
            parser(['create', '-d', 'string_instead_int', '95'])
        self.assertEqual(cm.exception.args[0], f'The diceware flag should take a positive int in first argument')


    def test_dice_bad_list(self):
        with self.assertWarns(UserWarning) as cm:
            resp = parser(['create', '-d', '95', '/home/bad_path'])
        self.assertEqual(str(cm.warning), 'The path you entered is invalid, the list that is used is the default english diceware list')
        self.assertEqual(resp, {'dice': (95, LIST_PATH)})

    def test_dice_one_good_argumen(self):
        self.assertEqual(parser(['create', '-d', '95']), {'dice': (95, LIST_PATH)})
    
    def test_dice_two_good_arguments(self):
        self.assertEqual(parser(['create', '-d', '95', LIST_PATH]), {'dice': (95, LIST_PATH)})



if __name__ == '__main__':
    argv = ['test_parser.py']
    unittest.main()