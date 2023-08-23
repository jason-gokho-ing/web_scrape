import sqlite3 as sql

# create a connection
connection = sql.connect("data.db")

# cursor serves as an object that executes SQL methods
cursor = connection.cursor()

# query data inside cursor object
cursor.execute("SELECT * FROM events WHERE band = 'Tigers'")
# used to catch all instances of the select criteria
result = cursor.fetchall()

# Insert new rows
new_rows = [('Pigs', 'Pigs City', '2013.11.10'),
            ('Hens', 'Hens City', '2023.05.12')]

# insert values into new rows
cursor.executemany("INSERT INTO events VALUES(?,?,?)", new_rows)

#  write changes into database
connection.commit()


# query to see table
cursor.execute("SELECT * FROM events")
rows = cursor.fetchall()
print(rows)
