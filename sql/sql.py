import sqlite3
from typing import Generator
from getpass import getuser

PATH = '/home/' + getuser() + '/Desktop/lockpy/sql/'

class Database():
    def __init__(self, path: str) -> None:
        self.path = PATH + path
        self.connect()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.con.close()

    def connect(self) -> None:
        self.con = sqlite3.connect(self.path)
        self.cursor = self.con.cursor()
        # check if the table exist
        sql_command = "SELECT name FROM sqlite_master WHERE type='table' AND name='password';"
        self.cursor.execute(sql_command)
        response = self.cursor.fetchall()
        if not response:
            self.create_table()

    def create_table(self) -> None:
        sql_command = f'''CREATE TABLE password(\
                        name TEXT PRIMARY KEY NOT NULL,\
                        user TEXT,\
                        password TEXT NOT NULL,\
                        url TEXT,\
                        description TEXT);'''
        self.cursor.execute(sql_command)

    def add_in_db(self, values: str) -> None:
        sql_command = f'INSERT INTO password VALUES {values};'
        self.cursor.execute(sql_command)
        self.con.commit()        

    def select_in_db(self, name: str) -> None:
        sql_command = f'SELECT * FROM password'
        if name != 'all':
            sql_command +=  f' WHERE name="{name}"'
        self.cursor.execute(sql_command)
        lines = self.cursor.fetchall()
        if not lines:
            raise ValueError('The service entered doesn\'t exist')
        for word in lines:
            d = {'Service': word[0], 'User': word[1], 'Password': word[2], 'Url': word[3], 'Description': word[4]}
            print('-' * 28)
            print('\n'.join(f'{k}: {d[k]}' for k in d if d[k]))

    def update_db(self, values: dict[str]) -> None:
        name, column, new_value = values['name'], values['column'], values['value']
        sql_command = f'UPDATE password SET {column}="{new_value}" WHERE name="{name}";'
        self.cursor.execute(sql_command)
        self.con.commit()
    
    def delete_in_db(self, name: str) -> None:
        sql_command = f'DELETE FROM password WHERE name="{name}";'
        self.cursor.execute(sql_command)
        self.con.commit()


if __name__ == '__main__':
    with Database('test.lp') as db:
        db.add_in_db()

"""
# SQL query to view different table
db.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
print(db.cursor.fetchall()[0][0])

# SQL format to insert the data in the table
sql_value = '(45, "Blant","Heon", "M", "2014-03-28")'
db.add_in_db('emp', sql_value)
 
# SQL format to update value
db.update_db('emp', 'lname', 'Jyoti', ['fname', 'Rishabh'])

# SQL formmat to delete a raws
db.delete_in_db('emp', ['fname', 'Rishabh'])
"""
