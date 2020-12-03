import sqlite3
import datetime

# Create connection to db
conn = sqlite3.connect('config/db_comp0066.db')

# Create cursor
c = conn.cursor()

# Insert into user
c.execute("""
    INSERT INTO
        users (
        user_first_name,
        user_last_name,
        user_brith_date,
        user_email,
        user_password,
        user_registration_date,
        user_type)
    VALUES
        ('Manuel',
        'Buri',
        '2016-01-01',
        'manuel.buri@gmail.com',
        'test',
        datetime('now'),
        'gp');
""")

# Insert into gp
c.execute("""
    INSERT INTO
        gp 
    VALUES
        ('Manuel',
        'Buri');
""")

# Check
print("User successfully inserted")

# Commit to db
conn.commit()

# Close db
conn.close()



BEGIN TRANSACTION;

-- Table: gp
CREATE TABLE gp (gp_id INT PRIMARY KEY NOT NULL UNIQUE, user_id INT REFERENCES users (user_id) ON DELETE CASCADE ON UPDATE CASCADE);

-- Table: patient
CREATE TABLE patient (patient_id INTEGER PRIMARY KEY NOT NULL UNIQUE REFERENCES users (user_id) ON DELETE CASCADE ON UPDATE CASCADE, gp_id REFERENCES gp (gp_id) ON DELETE CASCADE ON UPDATE CASCADE NOT NULL, patient_NHS_blood_donor TEXT NOT NULL, patient_NHS_organ_donor TEXT NOT NULL, patient_status TEXT NOT NULL);

-- Table: users
CREATE TABLE users (user_id INT PRIMARY KEY UNIQUE NOT NULL, user_first_name TEXT NOT NULL, user_last_name REAL NOT NULL, user_brith_date DATE NOT NULL, user_email TEXT NOT NULL, user_password TEXT NOT NULL, user_registration_date DATETIME NOT NULL, user_type INT NOT NULL);

COMMIT TRANSACTION;
PRAGMA foreign_keys = on;
