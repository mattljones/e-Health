import sqlite3
import datetime

# Create connection to db
conn = sqlite3.connect('database/db_comp0066.db')

# Create cursor
c = conn.cursor()

# Insert into user
c.execute("""
    INSERT INTO
        gp (gp_id,
        gp_first_name,
        gp_last_name,
        gp_gender,
        gp_birth_date,
        gp_email,
        gp_password,
        gp_registration_date,
        gp_working_days,
        gp_department_id,
        gp_specialisation_id)
    VALUES
        (NULL,
        'Manuel',
        'Buri',
        'male',
        '2016-01-01',
        'manuel.buri@gmail.com',
        'test',
        datetime('now'),
        1,
        1,
        1);
""")


# Check
print("GP successfully inserted")

# Commit to db
conn.commit()

# Close db
conn.close()