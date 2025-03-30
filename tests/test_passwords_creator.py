import unittest
from __init__ import path
import modules.password_creators as password_creators

class TestStringPasswordsCreators(unittest.TestCase):
    def test_create_password_string(self):
        password = password_creators.create_password_string(3)
        self.assertGreaterEqual(password[1], 3)
        
        password = password_creators.create_password_string(50)
        self.assertGreaterEqual(password[1], 50)
        
        password = password_creators.create_password_string(150)
        self.assertGreaterEqual(password[1], 150)


class TestDicewarePasswordCreator(unittest.TestCase):
    def test_all_word(self):
        with open('/home/blantheon/Desktop/lockpy/lists/en.txt', 'r') as f:
            lines = f.readlines()
            lst = []
            for number in range(11111, 66667):  
                num_str = str(number)  # Convert number to string
                
                # Check if any digit is in the forbidden set {'7', '8', '9', '0'}
                if not any(digit in {'7', '8', '9', '0'} for digit in num_str):  
                    lst.append(num_str)


            for index, num in enumerate(lst):
                self.assertEqual(password_creators.binary_search(str(num), lines), lines[index].strip('\t\n123456'))
    
    def test_entropy_final_password(self):
        password = password_creators.create_password_diceware(50, path[0].replace('modules', 'lists/en.txt'))
        self.assertGreaterEqual(password[1], 50)

        password = password_creators.create_password_diceware(100, path[0].replace('modules', 'lists/en.txt'))
        self.assertGreaterEqual(password[1], 100)

        password = password_creators.create_password_diceware(150, path[0].replace('modules', 'lists/en.txt'))
        self.assertGreaterEqual(password[1], 150)

if __name__ == '__main__':
    unittest.main()