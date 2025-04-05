import argparse
import sys
import warnings
from getpass import getuser
import os
from typing import Tuple
import modules.create_modules.password_creators as password_mod


def check_diceware(arguments: list[str]) -> Tuple[int, str]:
    if len(arguments) > 2:
        raise ValueError(f'The diceware flag take only one or two arguments in the following: int, str. See: python3 main.py create -h')
    if not arguments[0].isnumeric():
        raise ValueError('The diceware flag should take a positive int in first argument')
    if int(arguments[0]) <= 0:
        raise ValueError('The entropy could not be less or equal to zero')
    if int(arguments[0]) < 90:
        warnings.warn('Be careful, for a strong password we recommend using at least 90 bit of entropy')
        print('\n')

    if len(arguments) == 2:
        # check location of the flag lists with os module
        if os.path.isfile(arguments[1]):
            return (int(arguments[0]), arguments[1])
        else:
            warnings.warn('The path you entered is invalid, the list that is used is the default english diceware list')
            print('\n')

    return (int(arguments[0]), '/home/' + getuser() + '/Desktop/lockpy/lists/en.txt')


def parser(arguments: list[str]):
    parser = argparse.ArgumentParser(usage="%(prog)s [options]")
    parser.add_argument('--version', action='version', version='LockPy 1.0')
    subparsers = parser.add_subparsers(required=True)
    
    parser_create = subparsers.add_parser('create', help='To Write, see: python3 main.py create -h')
    parser_create = parser_create.add_mutually_exclusive_group()
    parser_create.add_argument('-s', '--string', type=int, metavar='Int',help='the minimal entropy for the string password ')
    parser_create.add_argument('-d', '--diceware', nargs='+', metavar='Int, str', help='the minimal entropy for the diceware password | OPTIONAL: a second argument with the path to the list')

    
    parser_check = subparsers.add_parser('check', help='To Write')
    parser_check = parser_check.add_mutually_exclusive_group()
    parser_check.add_argument('-c', '--calculate',type=str, metavar='Str', help='To Write')
    parser_check.add_argument('-p', '--pawn', type=str, metavar='Str', help='To Write')
    
    
    args = parser.parse_args(arguments)
    

    # This big tree of if will disappear and become a class in few times
    if not args.string and not args.diceware:
        raise ValueError(f'A flag with an entropy greater than 0 should be selected when the subcommand create is used, see: python3 main.py create -h')
    elif args.diceware:
        return {'dice': check_diceware(args.diceware)}
    else:
        return {'str': args.string}
    


if __name__ == '__main__':
    # options = {'str': int(entropy)} or {'dict': (int(entropy), str(path to list))}
    options = parser(sys.argv[1:])
    
    if options.get('str'):
        entropy_user = options['str']
        if int(entropy_user) < 0:
            raise ValueError('Negative entropy is not allowed')
        password = password_mod.create_password_string(entropy_user)
    if options.get('dice'):
        entropy_user, list_path = options['dice']
        password = password_mod.create_password_diceware(entropy_user, list_path)
    
    print(f'You\'r new password with an entropy of {password[1]} is:\n{repr(password[0])}')
