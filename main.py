import argparse
import sys
from modules.__init__ import path
import modules.password_creators as password_mod


def check_diceware(arguments):
    # This function return a tuple or an int 
    if len(arguments) > 2:
        raise AttributeError(f'The diceware flag take only one ore two arguments in the following: int, str. See: python3 main.py create -h')
        
    if len(arguments) == 2:
        if not arguments[0].isnumeric():
            raise AttributeError('The diceware flag should take an int in first argument')
        # check location of flag with os module
        #if os.blablabla:

        return (int(arguments[0]), arguments[1])
    
    if not arguments[0].isnumeric():
        raise AttributeError('The diceware flag should take an int in argument')
    return int(arguments[0])


def parser(arguments: list[str]):
    parser = argparse.ArgumentParser(usage="%(prog)s [options]")
    subparsers = parser.add_subparsers(metavar='create', required=True)

    parser_create = subparsers.add_parser('create', help='Should be used with -s or -d flag, see: python3 main.py create -h')
    parser_create = parser_create.add_mutually_exclusive_group()
    parser_create.add_argument('-s', '--string', type=int, metavar='Int',help='the minimal entropy for the string password ')
    parser_create.add_argument('-d', '--diceware', nargs='+', metavar='Int, str', help='the minimal entropy for the diceware password | OPTIONAL: a second argument with the path to the list')

    #parser.add_argument('--calculate', type=str, default = False, help='You\'r password | calculate the entropy of you\'r password')
    #parser.add_argument('-v', '--verbose', action='store_true', default=False)
    parser.add_argument('--version', action='version', version='Pswd Calculator 1.0')
    args = parser.parse_args(arguments)
    if not args.string and not args.diceware:
        raise AttributeError(f'A flag should be selected when the subcommand create is used, see: python3 main.py create -h')

    if args.string:
        entropy_user = args.string
        string_password = password_mod.create_password_string(entropy_user)
        print(string_password)
    if args.diceware:
        # entropy_path == tuple(entropy, path) or tuple(entropy)
        entropy_path = check_diceware(args.diceware)
        print(entropy_path)


if __name__ == '__main__':
    parser(sys.argv[1:])