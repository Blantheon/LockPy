from getpass import getuser


def find_path(path: str):
    path = path.replace('username', getuser())
    return path