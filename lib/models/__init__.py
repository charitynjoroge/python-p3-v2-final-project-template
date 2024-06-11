import sqlite3


CONN = sqlite3.connect('country.db')
CURSOR = CONN.cursor()
