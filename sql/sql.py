import sqlite3

class Database():

    def __init__(self, path: str):
        self.name = path

    
    def __del__(self):
        # To save the changes in the files. Never skip this.
        # If we skip this, nothing will be saved in the database.
        db.con.commit()


    def connect(self):
        self.con = sqlite3.connect(self.name)
        self.cursor = self.con.cursor()


    def select_all(self):
        self.cursor.execute('SELECT * FROM emp')
        all_db = db.cursor.fetchall()
        for line in all_db: 
            print(line)


    def add_in_db(self, table: str, values: str):
        sql_command = f'INSERT INTO {table} VALUES {values};'
        self.cursor.execute(sql_command)


    def update_db(self, table: str, column: str, new_value: str, condition: list[str, str]):
        sql_command = f'UPDATE {table} SET {column}="{new_value}" WHERE {condition[0]}="{condition[1]}";'
        self.cursor.execute(sql_command)

    
    def delete_in_db(self, table: str, condition: list[str, str]):
        sql_command = f'DELETE FROM {table} WHERE {condition[0]}="{condition[1]}";'
        self.cursor.execute(sql_command)



db = Database('test.db')
db.connect()



"""# SQL format to insert the data in the table
sql_value = '(45, "Blant","Heon", "M", "2014-03-28")'
db.add_in_db('emp', sql_value)
 
# SQL format to update value
db.update_db('emp', 'lname', 'Jyoti', ['fname', 'Rishabh'])

# SQL formmat to delete a raws
db.delete_in_db('emp', ['fname', 'Rishabh'])"""

db.select_all()
 
# close the connection
db.con.close()