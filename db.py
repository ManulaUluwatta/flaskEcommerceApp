import sqlite3

conn = sqlite3.connect('database.db')
db = conn.cursor()
categories = [
    "Computers & tablets",
    "Cameras & photo",
    "Cell phones & accessories",
    "Jewelry & watches",
    "Pet supplies",
    "Sporting goods",
    "Kids toys",
    "Outdoor sports",
    "Shoes"
]

print("ready")
db.execute("INSERT INTO categories (name) VALUES ('Jewelry & watches')")
db.execute("INSERT INTO categories (name) VALUES ('Pet supplies')")
db.execute("INSERT INTO categories (name) VALUES ('Sporting goods')")
db.execute("INSERT INTO categories (name) VALUES ('Kids toys')")
db.execute("INSERT INTO categories (name) VALUES ('Outdoor sports')")
db.execute("INSERT INTO categories (name) VALUES ('Shoes')")
# conn.execute('''INSERT INTO categories (name) VALUES ('Computers & tablets')''')
conn.commit()
conn.close()
# Computers & tablets
# Cameras & photo
# TV, audio & surveillance
# Cell phones & accessories
# Jewelry & watches
# Shoes
# Home & garden
# Crafts
# Pet supplies
# Sporting goods
# Outdoor sports
# Kids toys

