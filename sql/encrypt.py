from cryptography.fernet import Fernet
from getpass import getuser
from base64 import urlsafe_b64encode
from os import urandom
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
PATH = '/home/' + getuser() + '/Desktop/lockpy/sql/.salt.bin'


class Encryption():

    def __init__(self) -> None:
        with open (PATH, 'rb') as f:
            salt: bytes = f.read()
        self.new_key(salt)

        self.f = Fernet(self.key)


    def new_key(self, salt):
        self.pbkdf_derivation(salt)
        f = Fernet(self.key)
        

    def pbkdf_derivation(self, salt: bytes | None) -> None:
        if not salt:
            salt: bytes = urandom(16)

        password = input('Enter a password for the database: ').encode()
        pbkdf = PBKDF2HMAC(hashes.SHA256(), 32, salt, 1_000_000)
        self.key = urlsafe_b64encode(pbkdf.derive(password))
        
        with open(PATH, 'wb') as f:
            f.write(salt)


    def encrypt(self, data: bytes | str) -> None:
        if isinstance(data, str):
            data = data.encode()

        return self.f.encrypt(data)
    

    def decrypt(self, data: bytes) -> None:
        return self.f.decrypt(data)


e = Encryption()
