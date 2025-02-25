import sqlite3

# Connect to the SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('example.db')

# Create a cursor object
cursor = conn.cursor()

# Create a table
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    age INTEGER,
    email TEXT NOT NULL UNIQUE
)
''')

# Insert data into the table
cursor.execute('''
INSERT INTO users (name, age, email)
VALUES ('John Doe', 30, 'john.doe@example.com')
''')

# Commit the transaction
conn.commit()

# Query data from the table
cursor.execute('SELECT * FROM users')
rows = cursor.fetchall()

# Print the results
for row in rows:
    print(row)

# Update data in the table
cursor.execute('''
UPDATE users
SET age = 31
WHERE name = 'John Doe'
''')

# Commit the transaction
conn.commit()

# Delete data from the table
cursor.execute('''
DELETE FROM users
WHERE name = 'John Doe'
''')

# Commit the transaction
conn.commit()

# Close the connection
conn.close()