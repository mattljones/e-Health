import sqlite3
import datetime

# Create connection to db
conn = sqlite3.connect('config/db_comp0066.db')

# Create cursor
c = conn.cursor()

# Insert into user
c.execute("""
    INSERT IGNORE INTO
        user_type
    VALUES
        (0, 'admin'), (1, 'gp'), (2, 'patient');
""")

# Check
print("User successfully inserted")

# Commit to db
conn.commit()

# Close db
conn.close()
