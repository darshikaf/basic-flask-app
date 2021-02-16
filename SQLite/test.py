import sqlite3

connection = sqlite3.connect('data.db')

cursor = connection.cursor()

create_table = "CREATE TABLE user (id int, username text, password text)"
cursor.execute(create_table)

user = (1, 'jax', 'asdf')
insert_user = "INSERT INTO user VALUES(?, ?, ?)"
cursor.execute(insert_user, user)

users = [
    (2, 'anne', 'asdf'),
    (3, 'joe', 'fghj')
]

cursor.executemany(insert_user, users)

select_users = "SELECT * FROM user"
for row in cursor.execute(select_users):
    print (row)

connection.commit()

connection.close()