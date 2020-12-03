import sqlite3

# Create a database
conn = sqlite3.connect('config/db_comp0066.db')

# Create cursor
c = conn.cursor()

# Drop tables
c.execute("""DROP TABLE IF EXISTS users;""")
c.execute("""DROP TABLE IF EXISTS gp;""")
c.execute("""DROP TABLE IF EXISTS patient;""")
c.execute("""DROP TABLE IF EXISTS availability;""")
c.execute("""DROP TABLE IF EXISTS gp_department;""")
c.execute("""DROP TABLE IF EXISTS gp_specialisation;""")

# Check
print("DB successfully dropped")

# Commit to db
conn.commit()

# Close db
conn.close()
