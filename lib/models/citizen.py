import sqlite3


CONN = sqlite3.connect('country.db')
CURSOR = CONN.cursor()




class Citizen:
    def __init__(self, id, name, email=None, county=None):
        self.id = id 
        self.name = name
        self.email = email 
        self.county = county

   

    def add_to_citizen_table(self):

        """
        adds a new record to the 'citizen' table in the specified database file.

        """

        insert_query = 'INSERT INTO citizen (name, email, county) VALUES (?, ?, ?)'
        CURSOR.execute(insert_query)

        CONN.commit()
        CONN.close() 

        
    def update_citizen_name( citizen_id, new_name):
        """
        Updates the name of a citizen in the database.

        """

        cursor = CONN.cursor()

        try:
            CURSOR.execute('''UPDATE citizen SET name = ? WHERE id = ?''', (new_name, citizen_id))
            CONN.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error updating citizen: {e}")
            return False
        finally:
        # Close the cursor even if an exception occurs
            CURSOR.close()
