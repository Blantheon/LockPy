import sqlite3

class Database():

    def __init__(self, path):
        self.name = path


    def connect(self):
        self.con = sqlite3.connect(self.name)
        self.cursor = self.con.cursor().execute()




db = Database('test.db')
db.connect()
db.cursor()