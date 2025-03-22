import argparse
import sys
import modules.entropy as entropy

# resctrict number of arguments: https://stackoverflow.com/questions/13310047/how-do-i-constrain-my-python-script-to-only-accepting-one-argument-argparse

def check_diceware(arguments):
    if len(arguments) > 2:
        raise AttributeError(f'The diceware flag take only one ore two arguments in the following: int, str. See: python3 {sys.argv[0]} create -h')
        
    if len(arguments) == 2:
        if not arguments[0].isnumeric():
            raise AttributeError('The diceware flag should take an int in first argument')
        # check location of flag with os module
        #if os.blablabla:

        return (int(arguments[0]), arguments[1])
    
    if not arguments[0].isnumeric():
        raise AttributeError('The diceware flag should take an int in argument')
    return int(arguments[0])


parser = argparse.ArgumentParser(usage="%(prog)s [options]")
subparsers = parser.add_subparsers(help="l8. Subcommand help", dest='subcommand')

parser_create = subparsers.add_parser('create', help='Int | the minimal entropy for you\'r new password')
parser_create = parser_create.add_mutually_exclusive_group()
parser_create.add_argument('-s', '--str', type=int, help='Int | the minimal entropy for a string password ')
parser_create.add_argument('-d', '--diceware', nargs='+', help='Create a diceware password')

#parser.add_argument('--calculate', type=str, default = False, help='You\'r password | calculate the entropy of you\'r password')
parser.add_argument('-v', '--verbose', action='store_true', default=False)
parser.add_argument('--version', action='version', version='Pswd Calculator 1.0')
args = parser.parse_args()

if args.subcommand:
    if not args.str and not args.diceware:
        raise AttributeError(f'A flag should be selected when the subcommand create is used, see: python3 {sys.argv[0]} create -h')

    if args.str:
        entropy_user = args.str
        entropy.create_password_string(entropy_user)
    if args.diceware:
        # entropy_path == tuple(entropy, path) or tuple(entropy)
        entropy_path = check_diceware(args.diceware)
    print(entropy_path)

if __name__ == '__main__':
    pass