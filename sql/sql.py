import sqlite3
from typing import Generator

class Database():

    def __init__(self, path: str) -> None:
        self.path = 'sql/' + path
        self.table = None
        self.connect()


    def __enter__(self):
        self.con = sqlite3.connect(self.path)
        self.cursor = self.con.cursor()
        return self


    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.con.close()


    def connect(self) -> None:
        self.con = sqlite3.connect(self.path)
        self.cursor = self.con.cursor()


    def create_table(self, name: str) -> None:
        sql_command = f'''CREATE TABLE {name}(\
                        name TEXT PRIMARY KEY NOT NULL,\
                        user TEXT,\
                        password TEXT NOT NULL,\
                        url TEXT,\
                        description TEXT);'''
        self.cursor.execute(sql_command)


    def add_in_db(self, table: str, values: str) -> None:
        sql_command = f'INSERT INTO {table} VALUES {values};'
        try:
            self.cursor.execute(sql_command)
            self.con.commit()
            # if the table doesn't exist
        except sqlite3.OperationalError:
            self.create_table('password')
            self.add_in_db('password', values)
        

    def select_in_db(self, table: str, name: str) -> Generator[str, str, None]:
        sql_command = f'SELECT * FROM {table}'
        if name != 'all':
            sql_command +=  f' WHERE name="{name}"'
        
        self.cursor.execute(sql_command)
        line = self.cursor.fetchall()
        if not line:
            raise NameError('The service entered doesn\'t exist')
        
        yield line


    def update_db(self, table: str, column: str, new_value: str, name: str) -> None:
        sql_command = f'UPDATE {table} SET {column}="{new_value}" WHERE name="{name}";'
        self.cursor.execute(sql_command)
        self.con.commit()

    
    def delete_in_db(self, table: str, name: str) -> None:
        sql_command = f'DELETE FROM {table} WHERE name="{name}";'
        self.cursor.execute(sql_command)
        self.con.commit()



if __name__ == '__main__':
    with Database('test.db') as db:
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
db.delete_in_db('emp', ['fname', 'Rishabh'])"""
 

# To save the changes in the files. Never skip this.
# If we skip this, nothing will be saved in the database.
# db.con.commit()
