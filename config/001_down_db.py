import sqlite3

# Create a database
conn = sqlite3.connect('db_comp0066.db')

# Create cursor
c = conn.cursor()

# Create users table
c.execute("""DROP TABLE users;""")

# Create gp table
c.execute("""DROP TABLE gp;""")

# Create patient table
c.execute("""DROP TABLE patient;""")

# Check
print("DB successfully dropped")

# Commit to db
conn.commit()

# Close db
conn.close()
