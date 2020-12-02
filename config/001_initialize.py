import sqlite3

# Create a database
conn = sqlite3.connect('config/db_comp0066.db')

# Create cursor
c = conn.cursor()

# Create users table
c.execute("""
    CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
    user_first_name TEXT NOT NULL,
    user_last_name TEXT NOT NULL,
    user_brith_date DATE NOT NULL,
    user_email TEXT NOT NULL,
    user_password TEXT NOT NULL,
    user_registration_date DATETIME NOT NULL,
    user_type INT NOT NULL);
""")

# Create gp table
c.execute("""
    CREATE TABLE IF NOT EXISTS gp (
    gp_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
    user_id INT REFERENCES users (user_id) ON DELETE CASCADE ON UPDATE CASCADE);
""")

# Create patient table
c.execute("""
    CREATE TABLE IF NOT EXISTS patient (
    patient_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
    patient_gp_pair REFERENCES gp (gp_id) ON DELETE CASCADE ON UPDATE CASCADE NOT NULL,
    user_id REFERENCES users (user_id) ON DELETE CASCADE ON UPDATE CASCADE UNIQUE NOT NULL);
""")

# Create Admin table
c.execute("""
    CREATE TABLE IF NOT EXISTS admin (
    admin_id INTEGER PRIMARY KEY NOT NULL UNIQUE,
    user_id REFERENCES users (user_id) ON DELETE CASCADE ON UPDATE CASCADE UNIQUE NOT NULL);
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

# Create Admin in admin table
c.execute("""
    INSERT INTO admin (
        admin_id,
        user_id)
    VALUES
        ('1',
        '1');
""")

# Check
print("DB successfully created")

# Commit to db
conn.commit()

# Close db
conn.close()
