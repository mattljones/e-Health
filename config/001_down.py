import sqlite3

# Create a database
conn = sqlite3.connect('config/db_comp0066.db')

# Create cursor
c = conn.cursor()

# Drop tables
c.execute("""DROP TABLE users;""")
c.execute("""DROP TABLE gp;""")
c.execute("""DROP TABLE patient;""")
c.execute("""DROP TABLE admin;""")

# Check
print("DB successfully dropped")

# Commit to db
conn.commit()

# Close db
conn.close()
