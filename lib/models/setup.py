import sqlite3


CONN = sqlite3.connect('country.db')
CURSOR = CONN.cursor()


def database_table():

    CURSOR.execute('''CREATE TABLE IF NOT EXISTS county (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              name TEXT NOT NULL
             )''')


    CURSOR.execute('''CREATE TABLE IF NOT EXISTS citizen (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              name TEXT NOT NULL,
              email TEXT UNIQUE,
              county_name TEXT
             )''')

    CONN.commit()
    # CONN.close() 

database_table() 
