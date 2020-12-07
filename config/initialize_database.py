## COMP0066 Coursework Group 7
# This script initializes the sqlite database

import sqlite3

# Create a database
conn = sqlite3.connect('database/db_comp0066.db')

# Create cursor
c = conn.cursor()

## Creating the database tables.
# For user_gender ISO/IEC 5218 is used.

# Creating the admin table.
c.execute("""
    CREATE TABLE IF NOT EXISTS admin (
    admin_id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
    admin_first_name TEXT NOT NULL,
    admin_last_name TEXT NOT NULL,
    admin_gender NOT NULL CHECK(
        admin_gender = "not known" or
        admin_gender = "male" or
        admin_gender = "female" or
        admin_gender = "not applicable"),
    admin_brith_date DATE NOT NULL,
    admin_email TEXT NOT NULL,
    admin_password TEXT NOT NULL,
    admin_registration_date DATETIME NOT NULL);
""")

# Creating the gp table.
c.execute("""
    CREATE TABLE IF NOT EXISTS gp (
    gp_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
    gp_first_name TEXT NOT NULL,
    gp_last_name TEXT NOT NULL,
    gp_gender NOT NULL CHECK(
        gp_gender = "not known" or
        gp_gender = "male" or
        gp_gender = "female" or
        gp_gender = "not applicable"),
    gp_birth_date DATE NOT NULL,
    gp_email TEXT NOT NULL,
    gp_password TEXT NOT NULL,
    gp_registration_date DATETIME NOT NULL,
    gp_working_days INT NOT NULL,
    gp_department_id INTEGER NOT NULL,
    gp_specialisation_id INTEGER NOT NULL);
""")

# Creating the patient table.
c.execute("""
    CREATE TABLE IF NOT EXISTS patient (
    patient_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
    patient_first_name TEXT NOT NULL,
    patient_last_name TEXT NOT NULL,
    patient_gender NOT NULL CHECK(
        patient_gender = "not known" or
        patient_gender = "male" or
        patient_gender = "female" or
        patient_gender = "not applicable"),
    patient_birth_date DATE NOT NULL,
    patient_email TEXT NOT NULL,
    patient_password TEXT NOT NULL,
    patient_registration_date DATETIME NOT NULL,
    patient_NHS_blood_donor TEXT NOT NULL CHECK(
        patient_NHS_blood_donor = "yes" or
        patient_status = "no"), 
    patient_NHS_organ_donor TEXT NOT NULL CHECK(
        patient_NHS_organ_donor = "yes" or
        patient_NHS_organ_donor = "no"), 
    patient_status TEXT NOT NULL CHECK(
        patient_status = "inactive" or
        patient_status = "active"));
""")

# Creating the patient_medical_condition_type table.
c.execute("""
    CREATE TABLE IF NOT EXISTS patient_medical_condition_type (
    patient_medical_condition_type_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
    patient_medical_condition_type_name TEXT NOT NULL UNIQUE);
""")

# Creating the patient_medical_condition table.
c.execute("""
    CREATE TABLE IF NOT EXISTS patient_medical_condition (
    patient_id INTEGER REFERENCES patient (patient_id) ON DELETE CASCADE ON UPDATE CASCADE NOT NULL,
    patient_medical_condition_type_id TEXT REFERENCES patient_medical_condition_type (patient_medical_condition_type_id) ON DELETE CASCADE ON UPDATE CASCADE NOT NULL,
    PRIMARY KEY (patient_id, patient_medical_condition_type_id));
""")


# Creating the gp_specialisation table.
c.execute("""
    CREATE TABLE IF NOT EXISTS gp_specialisation (
    gp_specialisation_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
    gp_specialisation_name TEXT NOT NULL UNIQUE);
""")

# Creating the gp_department table.
c.execute("""
    CREATE TABLE IF NOT EXISTS gp_department (
    gp_department_id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
    gp_department TEXT UNIQUE NOT NULL);
""")

# Creating the availability table.
# TODO: we might need to add a separate table for the availability_status later on.
c.execute("""
    CREATE TABLE IF NOT EXISTS availability (
    availability_id INTEGER  PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
    availability_status TEXT NOT NULL CHECK(
        availability_status = "booked" or
        availability_status = "confirmed" or
        availability_status = "rejected" or
        availability_status = "cancelled" or
        availability_status = "time off" or
        availability_status = "sick leave"),
    availability_status_change_time DATETIME NOT NULL,
    availability_agenda TEXT,
    availability_start_time DATETIME NOT NULL,
    availability_type TEXT NOT NULL CHECK(
        availability_type = 'online' or
        availability_type = 'offline'),
    availability_notes TEXT NOT NULL,
    gp_id INTEGER  REFERENCES gp (gp_id) ON DELETE CASCADE ON UPDATE CASCADE NOT NULL,
    patient_id INTEGER  REFERENCES patient (gp_id) ON DELETE CASCADE ON UPDATE CASCADE);
""")

# Creating the prescription table.
c.execute("""
    CREATE TABLE IF NOT EXISTS prescription (
    prescription_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
    prescription_timestamp DATETIME NOT NULL,
    prescription_expiry_date DATETIME NOT NULL,
    drug_id NOT NULL, availability_id REFERENCES availability (availability_status) ON DELETE CASCADE ON UPDATE CASCADE NOT NULL);
""")

# Creating the drug table.
c.execute("""
    CREATE TABLE IF NOT EXISTS drug (
    drug_id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
    drug_name TEXT NOT NULL,
    drug_dosage TEXT NOT NULL,
    drug_frequency_dosage TEXT NOT NULL);
""")

# Inserting an admin in user table.
c.execute("""
    INSERT INTO
        admin (
        admin_first_name,
        admin_last_name,
        admin_gender,
        admin_brith_date,
        admin_email,
        admin_password,
        admin_registration_date)
    VALUES
        ('Admin',
        'Admin',
        'not known',
        '2020-01-01',
        'admin@email.com',
        'admin',
        datetime('now'));
""")

# Outputting outcome to user
print("DB successfully created")

# Commit to db
conn.commit()

# Close db
conn.close()
