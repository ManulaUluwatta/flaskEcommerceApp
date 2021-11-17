import sqlite3

#create connection
conn = sqlite3.connect('database.db')

#table creation

conn.execute('''CREATE TABLE USERS(
    user_id INTEGER PRIMARY KEY,
    email TEXT,
    password TEXT,
    firstName TEXT,
    lastName TEXT,
    addressLine1 TEXT,
    addressLine2 TEXT,
    city TEXT,
    state TEXT,
    postalCode TEXT,
    contact TEXT
)''')

conn.close