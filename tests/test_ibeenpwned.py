import unittest
from __init__ import path
from modules.check_modules.ibeenpwned import check_password_pawned


class TestIBeenPwned(unittest.TestCase):
    
    def test_with_known_password(self):
        self.assertIn("The password have been compromised", check_password_pawned('Password'))
    

    def test_with_unknow_password(self):
        self.assertEqual(check_password_pawned('KLkHJBN,;N:fd2 s2 0 g3sdf2s 132 gsq20 SF 0G'), 'The password is not detected in the database of haveibeenpawned')


if __name__ == '__main__':
    unittest.main()