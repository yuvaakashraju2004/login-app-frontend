import sqlite3

# Connect to the SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('users.db')
cursor = conn.cursor()

# Create a table to store user credentials
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
)
''')

# Insert a sample user (for testing)
cursor.execute('''
INSERT OR IGNORE INTO users (username, password)
VALUES ('admin', 'admin123')
''')

# Commit the changes and close the connection
conn.commit()
conn.close()