# This module will check if a password has been pawnend with the free APIkey of have i been pwned
import hashlib
import requests
from typing import Tuple


def check_password_pawned(password: str) -> Tuple[bool, int]:
    encoded_password = password.encode()
    hashed = hashlib.sha1(encoded_password).hexdigest()
    start, last = hashed[0:5], hashed[5:]

    res = requests.get(f'https://api.pwnedpasswords.com/range/{}')





check_password_pawned('password')