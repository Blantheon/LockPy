import argparse

# resctrict number of arguments: https://stackoverflow.com/questions/13310047/how-do-i-constrain-my-python-script-to-only-accepting-one-argument-argparse

parser = argparse.ArgumentParser(usage="%(prog)s [options]")
parser.add_argument('-f', '--filename', help='Absolute path | File for choose you\'r diceware dictionnary')
parser.add_argument('-et', '--entropy', type=int, help='Int | a minimal value of the entropy for the password')
parser.add_argument('-c', '--calculate', help='You\'r password | calculate the entropy of you\'r password')
parser.add_argument('-v', '--verbose', action=argparse.BooleanOptionalAction, default=False)
parser.add_argument('--version', action='version', version='Pswd Calculator 1.0')
args = parser.parse_args()
print(args.filename, args.entropy, args.verbose)
print(args)
