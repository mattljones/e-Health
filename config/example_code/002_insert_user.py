import sqlite3
import datetime

# Create connection to db
conn = sqlite3.connect('database/db_comp0066.db')

# Create cursor
c = conn.cursor()

# Insert into user
c.execute("""
    INSERT INTO
        patient (
        gp_id,
        patient_first_name,
        patient_last_name,
        patient_gender,
        patient_birth_date,
        patient_email,
        patient_password,
        patient_registration_date,
        patient_NHS_blood_donor,
        patient_NHS_organ_donor,
        patient_status)
    VALUES
        ('0',
        'Manuel',
        'Buri',
        'male',
        '2016-01-01',
        'manuel.buri@gmail.com',
        'test',
        datetime('now'),
        'yes',
        'yes',
        'pending');
""")


# Check
print("User successfully inserted")

# Commit to db
conn.commit()

# Close db
conn.close()
