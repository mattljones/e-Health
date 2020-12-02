import sqlite3

# Create a database
conn = sqlite3.connect('db_comp0066.db')

# Create cursor
c = conn.cursor()

# Create users table
c.execute("""CREATE TABLE users (
    user_id                INT      PRIMARY KEY UNIQUE NOT NULL,
    user_first_name        TEXT     NOT NULL,
    user_last_name         REAL     NOT NULL,
    user_brith_date        DATE     NOT NULL,
    user_email             TEXT     NOT NULL,
    user_password          TEXT     NOT NULL,
    user_registration_date DATETIME NOT NULL,
    user_type              INT      NOT NULL
);
""")

# Create gp table
c.execute("""CREATE TABLE gp (
    gp_id   INT PRIMARY KEY
                NOT NULL
                UNIQUE,
    user_id INT REFERENCES users (user_id) ON DELETE CASCADE ON UPDATE CASCADE
);
""")

# Create patient table
c.execute("""CREATE TABLE patient (
    patient_id      INTEGER PRIMARY KEY NOT NULL UNIQUE,
    patient_gp_pair         REFERENCES gp (gp_id) ON DELETE CASCADE ON UPDATE CASCADE NOT NULL,
    user_id                 REFERENCES users (user_id) ON DELETE CASCADE ON UPDATE CASCADE UNIQUE NOT NULL
);
""")

# Check
print("DB successfully created")

# Commit to db
conn.commit()

# Close db
conn.close()