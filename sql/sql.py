import apsw
from getpass import getuser
import os
from io import BytesIO
import sys
from encrypt import Cryptography, VFSRamOnly

PATH = '/home/' + getuser() + '/Desktop/lockpy/sql/'

class Database():
    def __init__(self, path: str) -> None:
        self.path = PATH + path
        self.crypto = Cryptography()
        self.vfs: VFSRamOnly
        self.con : apsw.Connection
        self.state: str
        self.db_bytes: BytesIO
        self.connect()
    
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # encrypt the database
        '''self.vfs.files.buffer.seek(0)
        self.crypto.encrypt(self.vfs.files.buffer.read())
        self.con.close()'''
        os.remove(PATH + '.Nothing')



    def connect(self):
        if os.path.isfile(self.path):
            # if the db exist then it's encrypted
            with open(self.path, 'rb') as f:
                decrypted_data = self.crypto.decrypt(f.read())
            self.db_bytes = BytesIO(decrypted_data)
        else:
            # just to create the database with good headers/format
            con = apsw.Connection(self.path)
            con.execute('CREATE TABLE empty(name TEXT PRIMARY KEY NOT NULL);')
            con.execute('DROP TABLE empty;')
            del con
            with open(self.path, 'rb') as f:
                self.db_bytes = BytesIO(f.read())
        self.vfs = VFSRamOnly(self.db_bytes)
        self.con = apsw.Connection(PATH +'.Nothing', vfs=self.vfs.vfs_name)
        self.create_table()

    def create_table(self):
        tables = [i for i in self.con.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='password';")]
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
        for word in lines:
            d = {'Service': word[0], 'User': word[1], 'Passline': word[2], 'Url': word[3], 'Description': word[4]}
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
    if os.path.isfile(PATH + 'database.lp'):
        os.remove(PATH + 'database.lp')
    with Database('database.lp') as db:
        db.add_in_db('("google","Myman", "A Good Pass", "https://gge.com", "A Big ldfsjfldsv Description")')
        f = open('just_add.db', 'wb')
        f.write(db.vfs.files.buffer.read())
        f.close()

        db.update_db({'name': 'google', 'column': 'password', 'value': 'Pass'})
        f = open('updated.db', 'wb')
        f.write(db.vfs.files.buffer.read())
        f.close
        #db.select_in_db('all')
        db.select_in_db('google')
        


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
