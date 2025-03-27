import unittest
from __init__ import path
import modules.password_creators as password_creators

class TestPasswordsCreators(unittest.TestCase):
    def test_create_password_string(self):
        password = password_creators.create_password_string(3)
        self.assertGreaterEqual(password[1], 3)
        
        password = password_creators.create_password_string(50)
        self.assertGreaterEqual(password[1], 50)
        
        password = password_creators.create_password_string(150)
        self.assertGreaterEqual(password[1], 150)


if __name__ == '__main__':
    unittest.main()