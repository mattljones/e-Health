import sqlite3
import datetime

# Create connection to db
conn = sqlite3.connect('config/db_comp0066.db')

# Create cursor
c = conn.cursor()

# Insert into user
c.execute("""INSERT INTO users (
                                user_first_name,
                                user_last_name,
                                user_brith_date,
                                user_email,
                                user_password,
                                user_registration_date,
                                user_type)
            VALUES ('Manuel',
            'Buri',
            '2016-01-01',
            'manuel.buri@gmail.com',
            'test',
            datetime('now'),
            'gp'
);
""")

# Check
print("User successfully inserted")

# Commit to db
conn.commit()

# Close db
conn.close()
