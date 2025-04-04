from random import choice, randint
from __init__ import path
from check_modules.entropy import calculate_entropy_string, calculate_entropy_diceware
from string import printable
from typing import Tuple


def binary_search(number: str, lines: str) -> str:
    # implement binary search for construct the diceware password
    higher = len(lines) - 1
    lower = 0
    while lower <= higher:
        
        index = (higher + lower) // 2

        if lines[index][0:5] == number:
            return lines[index].strip('\n\t123456')
        
        if lines[index][0:5] < number:
            lower = index + 1

        if lines[index][0:5] > number:
            higher = index - 1
    print(number)
    raise ValueError('The number is not in the list, please be sure you\'r list use 5 number beetwen 1 and 6')


def create_password_string(entropy: int) -> Tuple[str, int]:
    ENTROPY_BY_CHAR = 6.55
    step = round(entropy / ENTROPY_BY_CHAR) + 1
    password = ''.join(choice(printable) for _ in range(step))
    
    return (password, calculate_entropy_string(password, 94))


def create_password_diceware(entropy: int, lst) -> Tuple[str, int]:
        
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
            
            words.append(binary_search(number, lines))
            password = ' '.join(words)
        return (password, calculate_entropy_diceware(password))
