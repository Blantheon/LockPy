from string import ascii_lowercase, ascii_uppercase
from math import log2

def calculate_entropy_string(password: str) -> int:
    # calculate range of a given password before calculate entropy
    VALUES = {'lower': 26, 'upper': 26, 'int': 10, 'special' : 32}
    check = {'lower': True, 'upper': True, 'int': True, 'special': True}
    res = 0
    password_set = set(password)
    for char in password_set:
        if char.isalpha():
            if char.islower() and check['lower']:
                res += VALUES['lower']
                check['lower'] = False
            if char.isupper() and check['upper']:
                res += VALUES['upper']
                check['upper'] = False
        
        elif char.isnumeric():
            if check['int']:
                res += VALUES['int']
                check['int'] = False
            
        elif check['special']:
            res += VALUES['special']
            check['special'] = False
    
    # expression for calculate entropy
    return len(password) * log2(res)