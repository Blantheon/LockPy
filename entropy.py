from string import ascii_lowercase, ascii_uppercase
from math import log2

def calculate_entropy_string(password: str) -> int:
    # calculate range of a given password before calculate entropy
    VALUES = {'lower': 26, 'upper': 26, 'int': 10, 'special' : 32}
    check = {'lower': False, 'upper': False, 'int': False, 'special': False}
    res = 0
    password = set(password)
    for char in password:
        # the maximum value
        if res == 94: break
        
        if char in ascii_lowercase and not check['lower']:
            res += VALUES['lower']
            check['lower'] = True
        if char in ascii_uppercase and not check['upper']:
            res += VALUES['upper']
            check['upper'] = True
        if char.isdigit() and not check['int']:
            res += VALUES['int']
            check['int'] = True
        if not char.isalnum() and not check['special']:
            res += VALUES['special']
            check['special'] = True
    
    return len(password) * log2(res)
