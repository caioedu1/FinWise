import sqlite3

conn = sqlite3.connect('db.sqlite3')

cursor = conn.cursor()

cursor.execute('DROP INDEX IF EXISTS stocks_stocks_user_id_f75e91a8;')

