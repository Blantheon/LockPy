from string import printable
from math import log2
from typing import Tuple
from random import choice

def calculate_entropy_string(password: str, range_password=0) -> int:
    if not range_password:
        # calculate range_password of a given password before calculate entropy
        VALUES = {'lower': 26, 'upper': 26, 'int': 10, 'special' : 32}
        check = {'lower': True, 'upper': True, 'int': True, 'special': True}
        
        
        password_set = set(password)
        for char in password_set:
            if char.isalpha():
                if char.islower() and check['lower']:
                    range_password += VALUES['lower']
                    check['lower'] = False
                if char.isupper() and check['upper']:
                    range_password += VALUES['upper']
                    check['upper'] = False
            
            elif char.isnumeric():
                if check['int']:
                    range_password += VALUES['int']
                    check['int'] = False
                
            elif check['special']:
                range_password += VALUES['special']
                check['special'] = False
    
    # expression for calculate entropy
    return round(len(password) * log2(range_password), 2)


def create_password_string(entropy: int) -> Tuple[str, int]:
    ENTROPY_BY_CHAR = 6.55
    step = round(entropy / ENTROPY_BY_CHAR) + 1
    password = ''.join(choice(printable) for _ in range(step))
    
    return password, calculate_entropy_string(password, 94)


if __name__ == '__main__':
    print(create_password_string(int(input('Enter int: '))))