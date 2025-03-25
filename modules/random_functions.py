from getpass import getuser
from sys import path


def find_path(path: str):
    path = path.replace('username', getuser())
    return path

path.insert(0, find_path('/home/username/Desktop/password_generator/modules'))