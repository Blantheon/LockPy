# This module will check if a password has been pawnend with the free APIkey of have i been pwned
import hashlib
import requests
from typing import Tuple


def check_password_pawned(password: str) -> Tuple[bool, int]:
    encoded_password = password.encode()
    hashed = hashlib.sha1(encoded_password).hexdigest().upper()
    start, last = hashed[0:5], hashed[5:]

    res = requests.get(f'https://api.pwnedpasswords.com/range/{start}')

    for line in res.text.splitlines():
        if last in line:
            num = line.split(':')[1]
            return f"You'r password have been compomised and appear a total of {num} time in their database"
    return 'You\'r password is not detected in the database of haveibeenpawn'





if __name__ == "__main__":
    print(check_password_pawned('password'))
    print(check_password_pawned('flmdsqgf35d4g35dsfhs1gfd3sgf'))