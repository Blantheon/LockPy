from cryptography.fernet import Fernet
from getpass import getuser



class Encryption():

    def __init__(self, key=None) -> None:
        if not key:
            self.generate_key()

        self.f = Fernet(self.key)

    def generate_key(self):
        self.key = Fernet.generate_key()
        # The key is written in clear
        # TO ADD: write a hash of the key
        with open('/home/' + getuser() + '/Desktop/lockpy/sql/.password.key') as f:
            f.write(self.key)

    
    def encrypt(self, data: bytes | str) -> None:
        if isinstance(data, str):
            data = bytes(data)

        return self.f.encrypt(data)
    

    def decrypt(self, data: bytes) -> None:
        return self.f.decrypt(data)