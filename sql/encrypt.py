from cryptography.fernet import Fernet, InvalidToken
from getpass import getuser
from base64 import urlsafe_b64encode
from os import urandom
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

PATH = '/home/' + getuser() + '/Desktop/lockpy/sql'


class Encryption():
    def __init__(self) -> None:
        with open (f'{PATH}/.salt.bin', 'rb') as f:
            salt: bytes = f.read()
        self.pbkdf_derivation(salt)
        self.f = Fernet(self.key)

    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        # implement an errasing of the secret key in memory
        ...

    def pbkdf_derivation(self, salt: bytes | None) -> None:
        to_write = False
        if not salt:
            salt: bytes = urandom(16)
            to_write = True

        password = input('Enter a password for the database: ').encode()
        pbkdf = PBKDF2HMAC(hashes.SHA256(), 32, salt, 1_000_000)
        self.key = urlsafe_b64encode(pbkdf.derive(password))
        
        if to_write:
            with open(f'{PATH}/.salt.bin', 'wb') as f:
                f.write(salt)

    def encrypt(self, data: bytes | str) -> None:
        if isinstance(data, str):
            data = data.decode()
        encrypted_data: bytes = self.f.encrypt(data)
        with open(f'{PATH}/database.lp.enc', 'wb') as f:
            f.write(encrypted_data)

    def decrypt(self, data: bytes) -> None:
        try:
            decrypted_data =  self.f.decrypt(data)
        except InvalidToken:
            raise InvalidToken('The password entered is invalid')
        
        return decrypted_data


if __name__ == '__main__':
    e = Encryption()
    with open(f'{PATH}/database.lp.enc', 'rb') as f2:
        enc = f2.read()
        e.decrypt(enc)