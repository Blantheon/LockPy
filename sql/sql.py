import sqlite3

class Database():

    def __init__(self, path):
        self.name = path


    def connect(self):
        self.con = sqlite3.connect(self.name)
        self.cursor = self.con.cursor()




db = Database('test.db')
db.connect()
sql = '''CREATE TABLE emp ( 
staff_number INTEGER PRIMARY KEY, 
fname VARCHAR(20), 
lname VARCHAR(30), 
gender CHAR(1), 
joining DATE);'''
db.cursor.execute(sql)
db.con.close()