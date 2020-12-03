import sqlite3

# Create a database
conn = sqlite3.connect('config/db_comp0066.db')

# Create cursor
c = conn.cursor()

# Create users table
# added CHECK for user_type to enforce hard coded database
c.execute("""
    CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
    user_first_name TEXT NOT NULL,
    user_last_name TEXT NOT NULL,
    user_brith_date DATE NOT NULL,
    user_email TEXT NOT NULL,
    user_password TEXT NOT NULL,
    user_registration_date DATETIME NOT NULL,
    user_type TEXT NOT NULL CHECK(user_type = "admin" or user_type = "gp" or user_type = "patient"));
""")

# Create gp table
c.execute("""
    CREATE TABLE IF NOT EXISTS gp (
    gp_id INTEGER PRIMARY KEY NOT NULL UNIQUE REFERENCES users (user_id) ON DELETE CASCADE ON UPDATE CASCADE);
""")

# Create patient table
c.execute("""
    CREATE TABLE IF NOT EXISTS patient (
    patient_id INTEGER PRIMARY KEY NOT NULL UNIQUE REFERENCES users (user_id) ON DELETE CASCADE ON UPDATE CASCADE,
    gp_id REFERENCES gp (gp_id) ON DELETE CASCADE ON UPDATE CASCADE NOT NULL);
""")

# Create gp_specialisation table
c.execute("""
    CREATE TABLE IF NOT EXISTS gp_specialisation (
    gp_specialisation_id INTEGER PRIMARY KEY NOT NULL UNIQUE,
    gp_specialisation_name TEXT NOT NULL UNIQUE);
""")

# Create gp_department table
c.execute("""
    CREATE TABLE gp_department (
    gp_department_id INTEGER PRIMARY KEY UNIQUE NOT NULL,
    gp_department TEXT UNIQUE NOT NULL);
""")

# Create availability table
c.execute("""
    CREATE TABLE availability (
    availability_id INTEGER  PRIMARY KEY UNIQUE NOT NULL,
    availability_status TEXT NOT NULL,
    avalability_date DATE NOT NULL,
    availability_status_change_time DATETIME NOT NULL,
    availability_agenda TEXT,
    availability_start_time DATETIME NOT NULL,
    availability_type TEXT NOT NULL,
    availability_notes TEXT NOT NULL,
    gp_id INTEGER  REFERENCES gp (gp_id) ON DELETE CASCADE ON UPDATE CASCADE NOT NULL,
    patient_id INTEGER  REFERENCES patient (gp_id) ON DELETE CASCADE ON UPDATE CASCADE NOT NULL);
""")

# Create Admin in user table
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
        ('Admin',
        'Admin',
        '2020-01-01',
        'admin@email.com',
        'admin',
        datetime('now'),
        'admin');
""")

# Check
print("DB successfully created")

# Commit to db
conn.commit()

# Close db
conn.close()
