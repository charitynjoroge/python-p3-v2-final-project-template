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


        try:
            CURSOR.execute('''UPDATE citizen SET name = ? WHERE id = ?''', (new_name, citizen_id))
            CONN.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error updating citizen: {e}")
            return False
        finally:
            CURSOR.close()

    
    
    def delete_citizen(cls, citizen_id):
        """
        Deletes a citizen record from the database.

        """
        try:
            CURSOR.execute('DELETE FROM citizen WHERE id = ?', (citizen_id,))
            CONN.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error deleting citizen: {e}")
            return False
        finally:
            CURSOR.close()

    
    def find_by_name(cls, name):
        """
        Finds citizen records in the database that match the provided name (partial match).

        """

        CURSOR = CONN.cursor()
        CURSOR.execute('SELECT * FROM citizen WHERE name LIKE ?', (f'%{name}%',))
        citizens = CURSOR.fetchall()
        return [cls(*citizen) for citizen in citizens]  


    def find_by_id(cls, citizen_id):
        """
        Finds a citizen record in the database by ID.

        Args:
            conn (sqlite3.Connection): The database connection object.
            citizen_id (int): The ID of the citizen to search for.

        Returns:
            Citizen: The Citizen object matching the ID, or None if not found

        """
        CURSOR = CONN.cursor()
        CURSOR.execute('SELECT * FROM citizen WHERE id = ?', (citizen_id,))
        citizen_data = CURSOR.fetchone()
        if citizen_data:
            return cls(*citizen_data)  
        else:
            return None  # Return None if not found
        
    
def find_by_county_id(county_id):
    """
    Finds citizen records in the database that belong to the specified county ID.

    Args:
        conn (sqlite3.Connection): The database connection object.
        county_id (int): The ID of the county to search for citizens.

    Returns:
        list[tuple]: A list of tuples containing citizen data (assuming column order).
    """

    try:
        CURSOR.execute('SELECT * FROM citizen WHERE county_id = ?', (county_id,))
        citizens = CURSOR.fetchall()
        return citizens
    except sqlite3.Error as e:
        print(f"Error finding citizens: {e}")
        return []  # Return empty list on error
    