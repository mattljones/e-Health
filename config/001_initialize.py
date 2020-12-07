## COMP0066 Coursework Group 7
# This script initializes the sqlite database

import sqlite3

# Create a database
conn = sqlite3.connect('config/db_comp0066.db')

# Create cursor
c = conn.cursor()

# Creating the users table.
# For user_gender ISO/IEC 5218 is used.
c.execute("""
    CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
    user_first_name TEXT NOT NULL,
    user_last_name TEXT NOT NULL,
    user_gender NOT NULL CHECK(
        user_gender = "not known" or
        user_gender = "male" or
        user_gender = "female" or
        user_gender = "not applicable"),
    user_brith_date DATE NOT NULL,
    user_email TEXT NOT NULL,
    user_password TEXT NOT NULL,
    user_registration_date DATETIME NOT NULL,
    user_type TEXT NOT NULL CHECK(
        user_type = "admin" or
        user_type = "gp" or
        user_type = "patient"));
""")

# Creating the gp table.
c.execute("""
    CREATE TABLE IF NOT EXISTS gp (
    gp_id INT PRIMARY KEY NOT NULL UNIQUE REFERENCES users (user_id) ON DELETE CASCADE ON UPDATE CASCADE,
    gp_working_days INT NOT NULL,
    gp_department_id INTEGER NOT NULL,
    gp_specialisation_id INTEGER NOT NULL);
""")

# Creating the patient table.
c.execute("""
    CREATE TABLE IF NOT EXISTS patient (
    patient_id INTEGER PRIMARY KEY NOT NULL UNIQUE REFERENCES users (user_id) ON DELETE CASCADE ON UPDATE CASCADE, 
    gp_id INTEGER REFERENCES gp (gp_id) ON DELETE CASCADE ON UPDATE CASCADE NOT NULL UNIQUE, 
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
        availability_status = "available" or
        availability_status = "booked" or
        availability_status = "confirmed" or
        availability_status = "rejected" or
        availability_status = "cancelled" or
        availability_status = "time off" or
        availability_status = "sick leave"),
    availability_date DATE NOT NULL,
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
        users (
        user_first_name,
        user_last_name,
        user_gender,
        user_brith_date,
        user_email,
        user_password,
        user_registration_date,
        user_type)
    VALUES
        ('Admin',
        'Admin',
        'not known',
        '2020-01-01',
        'admin@email.com',
        'admin',
        datetime('now'),
        'admin');
""")

# Outputting outcome to user
print("DB successfully created")

# Commit to db
conn.commit()

# Close db
conn.close()
