# COMP0066 Coursework Group 7
# This script initializes the sqlite database

import sqlite3
import csv

# Create a database
conn = sqlite3.connect('database/db_comp0066.db')

# Create cursor
c = conn.cursor()

# Creating the database tables.
# For user_gender ISO/IEC 5218 is used.

# Creating the admin table.
c.execute("""
    CREATE TABLE IF NOT EXISTS admin (
    admin_id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
    admin_first_name TEXT NOT NULL,
    admin_last_name TEXT NOT NULL,
    admin_gender NOT NULL CHECK(
        admin_gender = 'not known' or
        admin_gender = 'male' or
        admin_gender = 'female' or
        admin_gender = 'not applicable'),
    admin_birth_date DATE NOT NULL,
    admin_email TEXT NOT NULL,
    admin_password TEXT NOT NULL,
    admin_registration_date DATETIME NOT NULL);
""")

# Creating the gp table.
c.execute("""
    CREATE TABLE IF NOT EXISTS gp (
    gp_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
    gp_status NOT NULL CHECK(
        gp_status = 'active' or
        gp_gender = 'male'),
    gp_first_name TEXT NOT NULL,
    gp_last_name TEXT NOT NULL,
    gp_gender NOT NULL CHECK(
        gp_gender = 'not known' or
        gp_gender = 'male' or
        gp_gender = 'female' or
        gp_gender = 'not applicable'),
    gp_birth_date DATE NOT NULL,
    gp_email TEXT NOT NULL,
    gp_password TEXT NOT NULL,
    gp_registration_date DATETIME NOT NULL,
    gp_working_days INT NOT NULL,
    gp_department_id INTEGER REFERENCES gp_department (gp_department_id) NOT NULL,
    -- We are not including gp_department_id in the user flow
    gp_specialisation_id INTEGER REFERENCES gp_specialisation (gp_specialisation_id) NOT NULL);
    -- We are not including gp_specialisation_id in the user flow
""")

# Creating the patient table.
c.execute("""
    CREATE TABLE IF NOT EXISTS patient (
    patient_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
    gp_id INTEGER REFERENCES gp (gp_id) NOT NULL,
    -- If GP gets deleted, this situation is handled in the Admin user flow 
    patient_first_name TEXT NOT NULL,
    patient_last_name TEXT NOT NULL,
    patient_gender NOT NULL CHECK(
        patient_gender = 'not known' or
        patient_gender = 'male' or
        patient_gender = 'female' or
        patient_gender = 'not applicable'),
    patient_birth_date DATE NOT NULL,
    patient_email TEXT NOT NULL,
    patient_password TEXT NOT NULL,
    patient_registration_date DATETIME NOT NULL,
    patient_NHS_blood_donor TEXT NOT NULL CHECK(
        patient_NHS_blood_donor = 'yes' or
        patient_status = 'no'), 
    patient_NHS_organ_donor TEXT NOT NULL CHECK(
        patient_NHS_organ_donor = 'yes' or
        patient_NHS_organ_donor = 'no'), 
    patient_status TEXT NOT NULL CHECK(
        patient_status = 'inactive' or
        patient_status = 'active'));
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
    patient_medical_condition_type_id TEXT REFERENCES patient_medical_condition_type (patient_medical_condition_type_id)
    ON DELETE CASCADE ON UPDATE CASCADE NOT NULL,
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

# Creating the booking table.
# TODO: we might need to add a separate table for the booking_status later on.
# I have deleted booking_date as we can extract this from booking_start_time
c.execute("""
    CREATE TABLE IF NOT EXISTS booking (
    booking_id INTEGER  PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
    booking_start_time DATETIME NOT NULL,
    booking_status TEXT NOT NULL CHECK(
        booking_status = 'booked' or
        booking_status = 'confirmed' or
        booking_status = 'rejected' or
        booking_status = 'cancelled' or
        booking_status = 'time off' or
        booking_status = 'sick leave'),
    booking_status_change_time DATETIME NOT NULL,
    booking_agenda TEXT,
    booking_type TEXT CHECK(
        booking_type = 'online' or
        booking_type = 'offline'),
    booking_notes TEXT,
    gp_id INTEGER REFERENCES gp (gp_id) NOT NULL,
    -- For the future appointments, Admin will update the GP
    -- For the appointments in the past, the GP id will remain in the booking table after the GP gets deleted,
    -- assuming that the hospital keeps an archive of GPs 
    patient_id INTEGER  REFERENCES patient (gp_id) ON DELETE CASCADE ON UPDATE CASCADE);
""")

# Creating the prescription table.
c.execute("""
    CREATE TABLE IF NOT EXISTS prescription (
    prescription_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
    prescription_timestamp DATETIME NOT NULL,
    prescription_expiry_date DATETIME NOT NULL,
    drug_id INTEGER REFERENCES drug (drug_id),
    -- We are not including gp_specialisation_id in the user flow
    drug_dosage TEXT NOT NULL,
    drug_frequency_dosage TEXT NOT NULL,
    booking_id REFERENCES booking (booking_id) ON DELETE CASCADE ON UPDATE CASCADE NOT NULL);
""")

# Creating the drug table.
c.execute("""
    CREATE TABLE IF NOT EXISTS drug (
    drug_id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
    drug_name TEXT NOT NULL);
""")

# Inserting an admin in admin table.
admin_csv = open("config/admin_dummydata.csv")
admin_rows = csv.reader(admin_csv)
c.executemany("INSERT INTO admin VALUES (?, ?, ?, ?, ?, ?, ?, ?)", admin_rows)

# inserting drugs from config/drug_dummydata.csv
# Important: the autoincrement Primary Keys have to be unique and Not Null in the dummydata.csv file
# Otherwise, the import would not work. Meaning one can only import the dummydata.csv once, and then
# would need to change the dummydata.csv primary key value or take the database down.
drug_csv = open("config/drug_dummydata.csv")
drug_rows = csv.reader(drug_csv)
c.executemany("INSERT INTO drug VALUES (?, ?)", drug_rows)

# Outputting outcome to user
print("DB successfully created")

# Commit to db
conn.commit()

# Close db
conn.close()
