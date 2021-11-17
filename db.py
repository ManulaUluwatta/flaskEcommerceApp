import sqlite3

conn = sqlite3.connect('database.db')
db = conn.cursor()

print("ready")
db.execute("INSERT INTO categories (name) VALUES ('Computers & tablets')")
db.execute("INSERT INTO categories (name) VALUES ('Cameras & photo')")
db.execute("INSERT INTO categories (name) VALUES ('Cell phones & accessories')")
db.execute("INSERT INTO categories (name) VALUES ('Jewelry & watches')")
db.execute("INSERT INTO categories (name) VALUES ('Pet supplies')")
db.execute("INSERT INTO categories (name) VALUES ('Sporting goods')")
db.execute("INSERT INTO categories (name) VALUES ('Kids toys')")
db.execute("INSERT INTO categories (name) VALUES ('Shoes')")
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

