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
    country Text,
    postalCode TEXT,
    contact TEXT
)''')

conn.execute('''CREATE TABLE categories
		(categoryId INTEGER PRIMARY KEY,
		name TEXT
		)''')

conn.execute(''' CREATE TABLE PRODUCTS(
    product_id Integer PRIMARY key,
    productName TEXT,
    price REAL,
    description TEXT,
    image TEXT,
    qty INTEGER,
    categoryId INTEGER,
    FOREIGN KEY(categoryId) REFERENCES categories(categoryId)
)''')

conn.execute('''CREATE TABLE cart
		(user_id INTEGER,
		product_id INTEGER,
		FOREIGN KEY(user_id) REFERENCES users(user_id),
		FOREIGN KEY(product_id) REFERENCES products(product_id)
		)''')

db = conn.cursor()

db.execute("INSERT INTO categories (name) VALUES ('Computers & tablets')")
db.execute("INSERT INTO categories (name) VALUES ('Cameras & photo')")
db.execute("INSERT INTO categories (name) VALUES ('Cell phones & accessories')")
db.execute("INSERT INTO categories (name) VALUES ('Jewelry & watches')")
db.execute("INSERT INTO categories (name) VALUES ('Pet supplies')")
db.execute("INSERT INTO categories (name) VALUES ('Sporting goods')")
db.execute("INSERT INTO categories (name) VALUES ('Kids toys')")
db.execute("INSERT INTO categories (name) VALUES ('Shoes')")
conn.commit()

conn.close