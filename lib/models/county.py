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


    
    def update_county_name(cls, county_id, new_name):
        """
        Updates the name of a county in the database.

        """

        try:
            CURSOR.execute('UPDATE county SET name = ? WHERE id = ?', (new_name, county_id))
            CONN.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error updating county: {e}")
            return False
        finally:
            CURSOR.close()

    
    def delete_county(cls, county_id):
        """
        Deletes a county record from the database.

        """

        try:
            CURSOR.execute('DELETE FROM county WHERE id = ?', (county_id,))
            CONN.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error deleting county: {e}")
            return False
        finally:
            CURSOR.close()

    
    def find_by_name(cls, name):
        """
        Finds county records in the database that match the provided name (partial match).

        """

        CURSOR = CONN.cursor()
        CURSOR.execute('SELECT * FROM county WHERE name LIKE ?', (f'%{name}%',))
        counties = CURSOR.fetchall()
        return [cls(*county) for county in counties]  # Create County objects from results

