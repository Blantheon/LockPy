import unittest
from __init__ import path
from lockpy import main
import contextlib
import io



class TestMain(unittest.TestCase):

    def __init__(self, methodName = "runTest"):
        self.f = io.StringIO()
        contextlib.redirect_stdout(self.f)
        super().__init__(methodName)

    def test_string_password(self):
        with contextlib.redirect_stdout(self.f):
            main(['create', '-s', '95'])
        self.assertIn('The new password with an entropy of ', self.f.getvalue())


    def test_diceware_password(self):
        with contextlib.redirect_stdout(self.f):
            main(['create', '-d', '95'])
        self.assertIn('The new password with an entropy of ', self.f.getvalue())


    def test_calculate_password(self):
        with contextlib.redirect_stdout(self.f):
            main(['check', '-c', 'Password'])
        self.assertIn('The entropy of the password Password is: ', self.f.getvalue())
    

    def test_check_ibeenpawnd(self):
        with contextlib.redirect_stdout(self.f):
            main(['check', '-p', 'Password'])
        self.assertIn('The password have been compromised and appear a total of ', self.f.getvalue())



if __name__ == '__main__':
    unittest.main()