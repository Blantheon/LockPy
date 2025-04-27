from cryptography.fernet import Fernet
from getpass import getuser
import hashlib
from os import urandom
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

class Encryption():

    def __init__(self, key=None) -> None:
        if not key:
            self.new_key()

        self.f = Fernet(self.key)

    def new_key(self, password: str = None):
        self.key = Fernet.generate_key()
        if not password:
            password = input('Enter a password for the database: ')

        # TO ADD: write a crypted key
        salt: bytes = urandom(16)
        kdf = PBKDF2HMAC(hashes.SHA256(), 32, salt, 1_000_000)
        print(kdf.derive(b'password'))
        
        '''with open('/home/' + getuser() + '/Desktop/lockpy/sql/.password.key') as f:
            f.write(self.key)'''

    
    def encrypt(self, data: bytes | str) -> None:
        if isinstance(data, str):
            data = bytes(data)

        return self.f.encrypt(data)
    

    def decrypt(self, data: bytes) -> None:
        return self.f.decrypt(data)


e = Encryption()
