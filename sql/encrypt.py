from cryptography.fernet import Fernet
from getpass import getuser
from base64 import urlsafe_b64encode
from os import urandom
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

class Encryption():

    def __init__(self, key=None) -> None:
        if not key:
            self.new_key()

        self.f = Fernet(self.key)


    def new_key(self, password: str = None):
        self.key: bytes = Fernet.generate_key()
        pbkdf = self.pbkdf_derivation(password)
        f = Fernet(urlsafe_b64encode(pbkdf))
        print(f)
        
        
        
        '''with open('/home/' + getuser() + '/Desktop/lockpy/sql/.password.key') as f:
            f.write(self.key)'''


    def pbkdf_derivation(self, password: str | None) -> bytes:
        if not password:
            password = input('Enter a password for the database: ')

        password = password.encode()
        salt: bytes = urandom(16)
        kdf = PBKDF2HMAC(hashes.SHA256(), 32, salt, 1_000_000)
        key: bytes = kdf.derive(password)
        
        with open('/home/' + getuser() + '/Desktop/lockpy/sql/.salt.bin', 'w') as f:
            f.write(salt)
        return key
    
    def encrypt(self, data: bytes | str) -> None:
        if isinstance(data, str):
            data = data.encode()

        return self.f.encrypt(data)
    

    def decrypt(self, data: bytes) -> None:
        return self.f.decrypt(data)


e = Encryption()
