from random import choice, randint
from entropy import calculate_entropy_string
from string import printable
from typing import Tuple
from getpass import getuser


def create_password_string(entropy: int) -> Tuple[str, int]:
    ENTROPY_BY_CHAR = 6.55
    step = round(entropy / ENTROPY_BY_CHAR) + 1
    password = ''.join(choice(printable) for _ in range(step))
    
    return (password, calculate_entropy_string(password, 94))


def binary_search(number: int, lines: str) -> str:
    '''# implement binary search for construct the diceware password
    index = len(lines) // 2
    
    if lines[index][0:5] == number:
        return lines[index]'''
    pass


def create_password_diceware(entropy: int, lst=False) -> Tuple[str, int]:
    if not lst:
        lst = '/home/' + getuser() + '/Desktop/password_generator/lists/en.txt'
        
    with open(lst, 'r') as file:
        lines = file.readlines()
        ENTROPY_BY_WORD = 12.92
        number_of_words = round(entropy / ENTROPY_BY_WORD)
        words = []
        
        if number_of_words * ENTROPY_BY_WORD < entropy:
            number_of_words += 1

        for _ in range(number_of_words):
            number = ''
            for _ in range(5):
                number += str(randint(1, 6))
            
            number = int(number)
            words.append(binary_search(number, lines))