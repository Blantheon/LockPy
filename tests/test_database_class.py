import unittest
from __init__ import path
import sqlite3
import contextlib
import io
from sql.sql import Database
import os
from getpass import getuser


class TestDatabaseClass(unittest.TestCase):
    
    def __init__(self, methodName = "runTest"):
        self.f = io.StringIO()
        super().__init__(methodName)

    def setUp(self):
        with Database('test.lp') as db:
            db.add_in_db('("google", "username", "Diceware Password", Null, "A Description")')
            return super().setUp()

    def tearDown(self):
        os.remove('/home/' + getuser() + '/Desktop/lockpy/sql/test.lp')
        return super().tearDown()

    def test_create_table(self):
        # The table is created at the connection
        with Database('test.lp') as db:
            with self.assertRaises(sqlite3.OperationalError) as cm:
                db.create_table()

        self.assertEqual(cm.exception.args[0], 'table password already exists')
        self.assertTrue(os.path.isfile('/home/' + getuser() + '/Desktop/lockpy/sql/test.lp'))

    def test_retrieve_in_db(self):
        with Database('test.lp') as db, contextlib.redirect_stdout(self.f):
            db.select_in_db('all')
            db.select_in_db('google')
        self.assertEqual(self.f.getvalue(), f'{'-' * 28}\nService: google\nUser: username\nPassword: Diceware Password\nDescription: A Description\n' * 2)

    def test_delete_in_db(self):
        with Database('test.lp') as db:
            db.delete_in_db('This raw does not exist')
            db.delete_in_db('google')

            with self.assertRaises(ValueError) as cm:
                db.select_in_db('all')
        
        self.assertEqual(cm.exception.args[0], 'The service entered doesn\'t exist')

    def test_update_db(self):
        with Database('test.lp') as db, contextlib.redirect_stdout(self.f):
            db.update_db({'name': 'ljl', 'column': 'url', 'value': 'https://google.com/'})
            db.update_db({'name': 'google', 'column': 'url', 'value': 'https://google.com/'})
            db.select_in_db('all')
        self.assertEqual(self.f.getvalue(), f'{'-' * 28}\nService: google\nUser: username\nPassword: Diceware Password\nUrl: https://google.com/\nDescription: A Description\n')


if __name__ == '__main__':
    unittest.main()
    