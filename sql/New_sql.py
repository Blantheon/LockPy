import apsw
import sqlite3
from getpass import getuser
import os
from io import BytesIO
from encrypt import Cryptography, VFSRamOnly

PATH = '/home/' + getuser() + '/Desktop/lockpy/sql/'

class Database():
    def __init__(self, path: str) -> None:
        self.path = PATH + path
        self.crypto = Cryptography()
        self.vfs: VFSRamOnly
        self.con : apsw.Connection
        self.state: str
        self.connect()
    
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # encrypt the buffer and write it in the hard drive
        '''if self.state == 'encrypted':
            data = self.vfs.files.buffer.read()
            self.crypto.encrypt(data)'''
        ...



    def connect(self):
        if os.path.isfile(self.path):
            # if the db exist then it's encrypted
            with open(self.path) as f:
                decrypted_data = self.crypto.decrypt(f.read())
            self.buffer = BytesIO(decrypted_data)
        else:
            # just to create the database with good headers/format
            con = sqlite3.connect(self.path)
            con.execute('CREATE TABLE empty(name TEXT PRIMARY KEY NOT NULL);')
            del con
            with open(self.path, 'rb') as f:
                self.buffer = BytesIO(f.read())
        self.vfs = VFSRamOnly(self.buffer)
        self.con = apsw.Connection('Inexistant', vfs=self.vfs.vfs_name)
        self.create_table()

    def create_table(self):
        tables = [i for i in self.con.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='password';")]
        print(tables)
        if not tables:
            sql_command = f'''CREATE TABLE password(\
                        name TEXT PRIMARY KEY NOT NULL,\
                        user TEXT,\
                        password TEXT NOT NULL,\
                        url TEXT,\
                        description TEXT);'''
            self.con.execute(sql_command)

    def add_in_db(self, values: str) -> None:
        sql_command = f'INSERT INTO password VALUES {values};'
        self.con.execute(sql_command)

    def select_in_db(self, name:str) -> None:
        sql_command = f'SELECT * FROM password'
        if name != 'all':
            sql_command +=  f' WHERE name="{name}"'
        lines = [i for i in self.con.execute(sql_command)]
        if not lines:
            raise ValueError('The service entered doesn\'t exist')
        for line in lines:
            d = {'Service': line[0], 'User': line[1], 'Passline': line[2], 'Url': line[3], 'Description': line[4]}
            print('-' * 28)
            print('\n'.join(f'{k}: {d[k]}' for k in d if d[k]))

    def update_db(self, values:dict[str: str]) -> None:
        name, column, new_value = values['name'], values['column'], values['value']
        sql_command = f'UPDATE password SET {column}="{new_value}" WHERE name="{name}";'
        self.con.execute(sql_command)
    
    def delete_in_db(self, name: str) -> None:
        sql_command = f'DELETE FROM password WHERE name="{name}";'
        self.con.execute(sql_command)


if __name__ == '__main__':
    os.remove(PATH + 'test.lp')
    os.remove(PATH + 'Test_writen.db')
    with Database('test.lp') as db:
        db.add_in_db('("google","googleman", "passW", "https://google.com", "A Big Description")')
        db.select_in_db('all')
        with open('Test_writen.db', 'wb') as fb:
            #db.vfs.files.buffer.seek(0)
            #db.vfs.files.buffer.truncate()
            fb.write(db.vfs.files.buffer.read())
        '''print(db.vfs.files.buffer.read())
        print('The len is: ' + f'{len(db.vfs.files.buffer.read())}')'''
    
        


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
