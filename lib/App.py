
from models.setup import database_table
from models.citizen import Citizen
from models.county import County

import sqlite3


CONN = sqlite3.connect('country.db')
CURSOR = CONN.cursor()



def main():
  
    # Initialize the database table 
    database_table()

    while True:
        print("\nCitizen Management System")
        print("1. Add Citizen")
        print("2. Update Citizen")
        print("3. Delete Citizen")
        print("4. Delete County")
        print("5. Find Citizen by ID")
        print("6. List Citizens")
        print("7. Exit")

        choice = input("Enter your choice (1-7): ")

        if choice == '1':
            # Add citizen
            citizen_name = input("Enter citizen's name: ")
            citizen_email = input("Enter citizen's email (optional): ")
            county_name = input("Enter citizen's county: ")

            try:
                 # Ensure name has at least 5 characters
                if len(citizen_name) < 5:
                    raise ValueError("Name must be at least 5 characters long.")

                # Ensure email is a Gmail address (if provided)
                if citizen_email and not citizen_email.endswith('@gmail.com'):
                    raise ValueError("Email must be a Gmail address (ending with @gmail.com).")


                # Create county (if not already existing)
                CURSOR.execute('INSERT INTO county (name) VALUES (?) ON CONFLICT DO NOTHING', (county_name,))
                CONN.commit()
                #

                # Create citizen
                CURSOR.execute('INSERT INTO citizen (name, email, county_name) VALUES (?, ?, ?)', (citizen_name, citizen_email, county_name))
                CONN.commit()
                print("Citizen added successfully!")
            except sqlite3.Error as e:
                print(f"Error adding citizen: {e}")

        elif choice == '2':
            # Update citizen
            citizen_id = int(input("Enter citizen ID to update: "))

            try:
                # Check if citizen exists
                CURSOR.execute('SELECT * FROM citizen WHERE id = ?', (citizen_id,))
                existing_citizen = CURSOR.fetchone()

                if existing_citizen:
                    new_name = input("Enter new name (Required): ") or existing_citizen["name"]
                    new_email = input("Enter new email(Required) : ") or existing_citizen["email"]
                    new_county = input("Enter new county (Required): ") or existing_citizen["county_name"]

                    CURSOR.execute('UPDATE citizen SET name = ?, email = ?, county_name = ? WHERE id = ?', (new_name, new_email, new_county, citizen_id, ))

                    # Update county table (if county name has changed)
                    if new_county != existing_citizen[3]:
                        # Check if the new county already exists
                        CURSOR.execute('SELECT id FROM county WHERE name = ?', (new_county,))
                        new_county_id = CURSOR.fetchone()
                    
                            # Create new county
                        CURSOR.execute('INSERT INTO county (name) VALUES (?)', (new_county,))
                        CONN.commit()
                            # Get the newly created county ID
                        new_county_id = CURSOR.execute('SELECT last_insert_rowid()').fetchone()[0]
                            # Update citizen's county_id to the new county
                        CURSOR.execute('UPDATE citizen SET county_id = ? WHERE id = ?', (new_county_id, citizen_id,))


                    CONN.commit()
                    print("Citizen updated successfully!")
                else:
                    print(f"Citizen with ID {citizen_id} not found.")
            except sqlite3.Error as e:
                print(f"Error updating citizen: {e}")
            except ValueError:
                print("Invalid citizen ID (must be an integer).")

        elif choice == '3':
            # Delete citizen
            citizen_id = int(input("Enter citizen ID to delete: "))

            try:
                
                existing_citizen = Citizen.delete_citizen(citizen_id)

                if existing_citizen:
                    CURSOR.execute('DELETE FROM citizen WHERE id = ?', (citizen_id,))
                    CONN.commit() 
                    print("Citizen deleted successfully!")
                else:
                    print(f"Citizen with ID {citizen_id} not found.")
            except sqlite3.Error as e:
                print(f"Error deleting citizen: {e}")
            except ValueError:
                print("Invalid citizen ID (must be an integer).")

        elif choice == '4':
            # Delete county
            county_id = int(input("Enter county ID to delete: "))

            try:

                existing_county = County.delete_by_id(county_id)

                if existing_county:
                    CURSOR.execute('DELETE FROM county WHERE id = ?', (county_id,))
                    CONN.commit() 
                    print("County deleted successfully!")
                else:
                    print(f"County with ID {county_id} not found.")
            except sqlite3.Error as e:
                print(f"Error deleting county: {e}")
            except ValueError:
                print("Invalid county ID (must be an integer).")



        elif choice == '5':
            # Find citizen by ID
            citizen_id = int(input("Enter citizen's ID to find: "))

            try:
                # Use Citizen.find_by_id 
                existing_citizen = Citizen.find_by_id(citizen_id)

                if existing_citizen:
                    # tuple
                    print("\nCitizen Details:") 
                    print(f"Name: {existing_citizen.name}")
                    print(f"Email: {existing_citizen.email}")
                    print(f"County: {existing_citizen.get_county}")
                    
                else:
                    print(f"Citizen with ID {citizen_id} not found.")
            except sqlite3.Error as e:
                print(f"Error finding citizen: {e}")
            except ValueError:
                if not isinstance(citizen_id, int):
                    print("Invalid citizen ID (must be an integer).")



        elif choice == '6':
            # List Citizens
            print("\nList of Citizens:")
            # Fetch all citizen data from the table
            CURSOR.execute('SELECT * FROM citizen')
            citizens = CURSOR.fetchall()  # all rows as a list of tuples

            if citizens:
                # Print header
                print("ID\tName\t\tEmail\t\tCounty")
                print("-" * 60)  # Max lengths for attributes are reasonable

                # Loop through each citizen data (tuple) and print details
                for citizen_data in citizens:
                    citizen_id, name, email, county = citizen_data
                    print(f"{citizen_id}\t{name:20}\t{email:25}\t{county}")  # Adjusted formatting
            else:
                print("No citizens found in the database.")


        elif choice == '7':
                    #Exit
                    print("Goodbye!!!")
                    break

        else:
            print("Invalid choice. Please enter a number between 1 and 5.")

   
    CONN.close()


if __name__ == "__main__":
    main()
