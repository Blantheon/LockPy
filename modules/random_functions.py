from getpass import getuser
from typing import Tuple


def find_path(path: str):
    path = path.replace('username', getuser())
    return path