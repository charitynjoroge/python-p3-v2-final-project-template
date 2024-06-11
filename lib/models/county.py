import sqlite3


CONN = sqlite3.connect('country.db')
CURSOR = CONN.cursor()



class County:

    def __init__(self, id, name):
        self.id = id 
        self.name = name 

    
    def add_to_county_table(self):

        """
        adds a new record to the 'county' table in the specified database file.

        """

        insert_query = 'INSERT INTO citizen (name) VALUES (?)'
        CURSOR.execute(insert_query)

        CONN.commit()
        CONN.close() 