import sqlite3

connection = sqlite3.connect('data.db')
cursor = connection.cursor()

create_user_table = "CREATE TABLE users (id INTEGER PRIMARY KEY, username text, password text)"
cursor.execute(create_user_table)

create_item_table = "CREATE TABLE items (id INTEGER PRIMARY KEY, name text, price float)"
cursor.execute(create_item_table)

connection.commit()
connection.close()