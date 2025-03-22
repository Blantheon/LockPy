import unittest
from sys import path
path.insert(0, '/home/royon/Desktop/password_generator/modules')
import entropy

class Test_entropy_module(unittest.TestCase):
    def test_calculate_range(self):
        # test without a given range
        self.assertEqual(entropy.calculate_entropy_string('Bankruptcies'), 68.41)
        self.assertEqual(entropy.calculate_entropy_string('1Bankruptcies2'), 83.36)
        self.assertEqual(entropy.calculate_entropy_string('1Bankruptcies2&%'), 104.87)
        # test with the given range
        self.assertEqual(entropy.calculate_entropy_string('Bankruptcies', 52), 68.41)
        self.assertEqual(entropy.calculate_entropy_string('1Bankruptcies2', 62), 83.36)
        self.assertEqual(entropy.calculate_entropy_string('1Bankruptcies2&%', 94), 104.87)
    
    def test_entropy_of_password_created(self):
        password = entropy.create_password_string(3)
        self.assertGreaterEqual(password[1], 3)
        
        password = entropy.create_password_string(50)
        self.assertGreaterEqual(password[1], 50)
        
        password = entropy.create_password_string(150)
        self.assertGreaterEqual(password[1], 150)



if __name__ == '__main__':
    unittest.main()