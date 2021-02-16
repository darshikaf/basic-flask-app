import sqlite3

connection = sqlite3.connect('data.db')

cursor = connection.cursor()

create_user_table = "CREATE TABLE user (id INTEGER PRIMARY KEY, username text, password text)"
cursor.execute(create_user_table)

# insert_user = "INSERT INTO user VALUES(?, ?, ?)"

# users = [
#     (1, 'jax', 'asdf')
#     (2, 'anne', 'asdf'),
#     (3, 'joe', 'fghj')
# ]
# cursor.executemany(insert_user, users)

# select_users = "SELECT * FROM user"
# for row in cursor.execute(select_users):
#     print (row)

create_item_table = "CREATE TABLE item (name text, price float)"
cursor.execute(create_item_table)

# insert_item = "INSERT INTO item VALUES(?, ?, ?)"

# items = [
#     ('sword', 27.99),
#     ('arrow', 1.99),
# ]

# cursor.executemany(insert_item, items)

# select_items = "SELECT * FROM item"
# for row in cursor.execute(select_items):
#     print (row)

connection.commit()

connection.close()