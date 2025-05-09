import argparse
import sys
import warnings
from getpass import getuser
import os
from typing import Tuple
import modules.create_modules.password_creators as password_mod
import modules.check_modules.entropy as entropy
import modules.check_modules.ibeenpwned as pawned
from sql.sql import Database

PATH = '/home/' + getuser() + '/Desktop/lockpy/lists/en.txt'

# These class are used to do verification on user input and call function after that
class NewPassword():
    @staticmethod
    def create_password_str(entropy_user: int) -> str:
        if int(entropy_user) < 0:
            raise ValueError('Negative entropy is not allowed')
        elif int(entropy_user < 90):
            warnings.warn('For a strong password we recommend using at least 90 bit of entropy')

        return password_mod.create_password_string(entropy_user)

    @staticmethod
    def create_password_dice(entropy_path: list[str, int]) -> str:
        entropy_user, list_path = entropy_path
        return password_mod.create_password_diceware(entropy_user, list_path)    

    @staticmethod
    def save_and_create_password(d, methods):
        # set to format's NewPassword methods
        if d.get('create'):
            if d['create'][0] == 'dice':
                d['create'] = ('dice', check_diceware([d['create'][1]]))
            else:
                d['create'] = (d['create'][0], int(d['create'][1]))
            
            key_method, entropy = d['create'][0], d['create'][1]
            password = methods[key_method](entropy)
            print(f'You\'r new password with an entropy of {password[1]} is:\n{repr(password[0])}')

            # set it in dictionnary
            d['password'] = repr(password[0]).strip('"\'')
        
        d.pop('create')
        if isinstance(d['description'], list):
            d['description'] = ' '.join(d['description'])
        if isinstance(d['password'], list):
            d['password'] = ' '.join(d['password'])
        if isinstance(d['user'], list):
            d['user'] = ' '.join(d['user'])
        return d


class CheckMethods():
    @staticmethod
    def calculate_password_entropy(password: str) -> str:
        nb_spaces = password.count(' ')
        if nb_spaces <= 2:
            print('The password is treated as a string password')
            return entropy.calculate_entropy_string(password)
        else:
            print('The password is treated like a diceware password')
            return entropy.calculate_entropy_diceware(password)

    @staticmethod
    def check_pawned(password: str) -> str:
        return pawned.check_password_pawned(password)


def construct_message(key_method: str, user: str, response: str):
    if key_method in ['str', 'dice']:
        return f'The new password with an entropy of {response[1]} is:\n{repr(response[0])}'
    elif key_method == 'calculate':
        return f'The entropy of the password {user} is: {response}'
    else:
        # the message is directly returned by the function
        return response


def check_diceware(arguments: list[str]) -> Tuple[int, str]:
    if len(arguments) > 2:
        raise ValueError(f'The diceware flag take only one or two arguments in the following: int, str. See: python3 lockpy.py create -h')
    if not arguments[0].isnumeric():
        raise ValueError('The diceware flag should take a positive int in first argument')
    if int(arguments[0]) <= 0:
        raise ValueError('The entropy could not be less or equal to zero')
    if int(arguments[0]) < 90:
        warnings.warn('For a strong password we recommend using at least 90 bit of entropy')
        print('\n')

    if len(arguments) == 2:
        # check location of the flag lists with os module
        if os.path.isfile(arguments[1]):
            return (int(arguments[0]), arguments[1])
        else:
            warnings.warn('The path entered is invalid, the list used is the default english diceware list')
            print('\n')

    return (int(arguments[0]), PATH)


def check_parsing(args: argparse.Namespace) -> Tuple[str, ...]:
    if args.command == 'create':
        if not args.string and not args.diceware:
            raise ValueError(f'A flag with an entropy greater than 0 should be selected when the subcommand create is used, see: python3 lockpy.py create -h')
        elif args.diceware:
            return ('create',('dice', check_diceware(args.diceware)))
        else:
            return ('create', ('str', args.string))
    
    if args.command == 'check':
        if args.calculate:
            return ('check', ('calculate', args.calculate))
        elif args.pawn:
            return ('check', ('pawn', args.pawn))
        else:
            raise ValueError('A flag should be selected when the subcommand check is used, see: python3 lockpy.py create -h')
    
    if args.command == 'save':
        if args.password and args.create:
            raise ValueError('The password flag and the create flag can\'t be used together')
        if not args.password and not args.create:
            raise ValueError('A flag between password ans create should be selected')
        if args.create and len(args.create) != 2 or args.create and not args.create[1].isnumeric():
            raise ValueError('The create flag should have two arguments like method (str or dice) and the entropy (95)')
        if args.create and args.create[0] != 'str' and args.create and args.create[0] != 'dice':
            raise ValueError('The create option should take \'str\' or \'dice\' in first argument') 
        if args.create and int(args.create[1]) <= 0:
            raise ValueError('The entropy have to be superior to zero') 

        return ('save', {'name': args.name, 'user': args.user, 'password': args.password, 'url'
        '': args.link, 'description': args.description, 'create': args.create})
        
    if args.command == 'retrieve':
        if args.name:
            return ('retrieve', args.name)
        elif args.all:
            return ('retrieve', 'all')
        else:
            raise ValueError('The retrieve subcommand should take a valid flag (-n or -a)')
        
    if args.command == 'delete':
        return ('delete', args.name)
    
    if args.command == 'update':
        column = args.column.strip().lower()
        if len(args.new_value) > 1 and column not in ['description', 'password']:
            raise ValueError('The only columns that accept multiple words are "description" and "password"')

        return ('update', {'name': args.name, 'column': column, 'value': ' '.join(args.new_value)})


def parser(arguments: list[str]) -> tuple[str, tuple[str]]:
    parser = argparse.ArgumentParser(usage="%(prog)s [options]")
    parser.add_argument('--version', action='version', version='LockPy 1.0')
    subparsers = parser.add_subparsers(required=True, dest='command')

    parser_create = subparsers.add_parser('create', 
                                          help='create a new password, see: python3 lockpy.py create -h')
    parser_create = parser_create.add_mutually_exclusive_group()
    parser_create.add_argument('-s', '--string',
                               type=int, metavar='Entropy', help='the minimal entropy for the string password ')
    parser_create.add_argument('-d', '--diceware', 
                               nargs='+', metavar='Entropy, path', help='the minimal entropy for the diceware password | OPTIONAL: a second argument with the path to the list')
    
    parser_check = subparsers.add_parser('check', 
                                         help="check the efficacity of you'r password, see python3 lockpy.py check -h")
    parser_check = parser_check.add_mutually_exclusive_group()
    parser_check.add_argument('-c', '--calculate',
                              type=str, metavar='Password', help='calculate entropy of a password')
    parser_check.add_argument('-p', '--pawn',
                              type=str, metavar='Password', help='check if a password has leaked on haveibeenpawned')
    
    parser_save = subparsers.add_parser('save',
                                        help='Save a password in database')
    parser_save.add_argument('-n', '--name', 
                            required=True, type=str, metavar='Service', help='The name of the service for the password')
    parser_save.add_argument('-p', '--password', 
                            type=str, metavar='Password', nargs='+', help='The password to save')
    parser_save.add_argument('-u', '--user', 
                            type=str, metavar='User', nargs='+', help='The Username to save')
    parser_save.add_argument('-c', '--create',
                             type=str, metavar='Password type | entropy', nargs='+', help='Create a new string or dice password to save')
    parser_save.add_argument('-l', '--link',
                             type=str, metavar='link', help='The url of the password\'s site')
    parser_save.add_argument('-d', '--description',
                             type=str, metavar='Description', nargs='+' ,help='A description saved in the database')

    parser_take = subparsers.add_parser('retrieve',
                                        help='Pick a password in the database')
    parser_take = parser_take.add_mutually_exclusive_group()
    parser_take.add_argument('-n', '--name',
                             type=str, metavar='Service', help='Retrieve informations of the service\'s name in the database')
    parser_take.add_argument('-a', '--all',
                             action='store_true', help='Retrieve all the database')

    parser_delete = subparsers.add_parser('delete',
                                           help='Delete an entry in the database')
    parser_delete.add_argument('name',
                               type=str, metavar='Name', help='Delete the raw in the database with the name entered')

    parser_update = subparsers.add_parser('update',
                                          help='Update the column in the database with the name entered')
    parser_update.add_argument('-n', '--name', 
                               type=str, metavar='Name ', required=True, help='The name of the raw')
    parser_update.add_argument('-c', '--column',
                               type=str, metavar='Column', required=True, help='The column (name, password, user, ...) to be updated')
    parser_update.add_argument('-nv', '--new-value',
                               type=str, nargs='+', metavar='New Value', required=True, help='The new value to set in the column')

    args = parser.parse_args(arguments)
    return check_parsing(args)

def main(args):
    subparse_choosed, user_values = parser(args)
    methods = {'str': NewPassword.create_password_str,
            'dice': NewPassword.create_password_dice,
            'calculate': CheckMethods.calculate_password_entropy,
            'pawn': CheckMethods.check_pawned,
            'retrieve': lambda s: s.select_in_db,
            'delete': lambda s: s.delete_in_db,
            'update': lambda s: s.update_db}

    if subparse_choosed in ['create', 'check']:
        key_method, user_input = user_values       
        response_to_user = methods[key_method](user_input)
        print(construct_message(key_method, user_input, response_to_user))
    
    if subparse_choosed == 'save':
        d = NewPassword.save_and_create_password(user_values, methods)

        with Database('database.lp') as db:
            db.add_in_db(f'({', '.join(f'"{d[i]}"' if d[i] else 'NULL' for i in d )})')
    
    if subparse_choosed in ['retrieve', 'delete', 'update']:
        with Database('database.lp') as db:
            methods[subparse_choosed](db)(user_values)


if __name__ == '__main__':
    a = 'retrieve google'
    main(sys.argv[1:])