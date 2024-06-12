import sqlite3


CONN = sqlite3.connect('country.db')
CURSOR = CONN.cursor()




class Citizen:


    MIN_NAME_LENGTH = 5


    def __init__(self, id, name, email=None, county=None):
        self.id = id 
        self.name = name
        self.email = email 
        self.county = county


    

    @property  # Getter for email
    def email(self):
        return self._email

    @email.setter  # Setter for email
    def email(self, new_email):
        if new_email is None or new_email[-len('@gmail.com'):] == '@gmail.com':
            self._email = new_email
        else:
            raise ValueError("Email must be a Gmail address (ending with @gmail.com)")


    @property  # Getter for name
    def name(self):
        return self._name

    @name.setter  # Setter for name
    def name(self, new_name):
        if new_name is None or len(new_name) >= Citizen.MIN_NAME_LENGTH:
            self._name = new_name
        else:
            raise ValueError(f"Name must be at least {Citizen.MIN_NAME_LENGTH} digits long.")


    @property
    def get_county(self):
        return self.county 
   
    @classmethod
    def add_to_citizen_table(self):

        """
        adds a new record to the 'citizen' table in the specified database file.

        """

        insert_query = 'INSERT INTO citizen (name, email, county) VALUES (?, ?, ?)'
        CURSOR.execute(insert_query, (self.name, self.email, self.county))

        CONN.commit()
        CONN.close() 


    
    @classmethod
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
        


    # @classmethod
    # def find_by_id(cls, citizen_id):
    #     """
    #     Finds a citizen record in the database by ID.

    #     """
    #     CURSOR = CONN.cursor()
    #     CURSOR.execute('SELECT * FROM citizen WHERE id = ?', (citizen_id,))
    #     citizen_data = CURSOR.fetchone()
    #     if citizen_data:
    #         return cls(*citizen_data)  
    #     else:
    #         return None  # Return None if not found
        
    @classmethod
    def find_by_id(cls, citizen_id):
        """
        Finds a citizen record in the database by ID.

        """
        CURSOR = CONN.cursor()
        CURSOR.execute('SELECT * FROM citizen WHERE id = ?', (citizen_id,))
        citizen_data = CURSOR.fetchone()
        if citizen_data:
        # Assuming citizen_data is a tuple containing attributes
            id, name, email, county = citizen_data
            return cls(id, name, email, county)
        else:
            return None  # Return None
        
        