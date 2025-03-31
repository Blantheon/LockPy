# This module will check if a password has been pawnend with the free APIkey of have i been pwned
import hashlib
import requests
from typing import Tuple


def check_password_pawned(password: str) -> Tuple[bool, int]:
    pass