# COMP0066 Coursework Group 2
# This script initializes the sqlite database

import sqlite3
import csv

# Create a database
conn = sqlite3.connect('database/db_comp0066.db')

# Create cursor
c = conn.cursor()


# CREATING DATABASE TABLES
# For user_gender ISO/IEC 5218 is used.

# Creating the admin table.
c.execute("""
    CREATE TABLE IF NOT EXISTS admin (
    admin_id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
    admin_first_name TEXT NOT NULL,
    admin_last_name TEXT NOT NULL,
    admin_gender TEXT NOT NULL CHECK(
        admin_gender = 'not known' or
        admin_gender = 'male' or
        admin_gender = 'female' or
        admin_gender = 'non binary' or
        admin_gender = 'prefer not to say'),
    admin_birth_date DATE NOT NULL,
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
    gp_gender TEXT NOT NULL CHECK(
        gp_gender = 'not known' or
        gp_gender = 'male' or
        gp_gender = 'female' or
        gp_gender = 'non binary' or
        gp_gender = 'prefer not to say'),
    gp_birth_date DATE NOT NULL,
    gp_email TEXT NOT NULL,
    gp_password TEXT NOT NULL,
    gp_registration_date DATETIME NOT NULL,
    gp_working_days INTEGER NOT NULL CHECK(
        gp_working_days = '0' or  -- Monday to Friday
        gp_working_days = '1' or  -- Tuesday to Saturday
        gp_working_days = '2' or  -- Wednesday to Sunday
        gp_working_days = '3' or  -- Thursday to Monday
        gp_working_days = '4' or  -- Friday to Tuesday
        gp_working_days = '5' or  -- Saturday to Wednesday
        gp_working_days = '6'),   -- Sunday to Thursday
    -- Number corresponds to first day of 5 consecutive days in working week e.g. 2 = Tuesday to Saturday
    gp_department_id INTEGER REFERENCES gp_department (gp_department_id) NOT NULL,
    -- We are not updating/deleting gp_department (gp_department_id) in the user flow so no special action on update/delete needed
    gp_specialisation_id INTEGER REFERENCES gp_specialisation (gp_specialisation_id) NOT NULL,
    -- We are not updating/deleting gp_specialisation (gp_specialisation_id) in the user flow so no special action on update/delete needed
    gp_status TEXT NOT NULL CHECK(
        gp_status = 'inactive' or
        gp_status = 'active'));
""")

# Creating the patient table.
c.execute("""
    CREATE TABLE IF NOT EXISTS patient (
    patient_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
    gp_id INTEGER REFERENCES gp (gp_id) NOT NULL,
    -- If a GP is deleted, this situation is handled in the Admin user flow (patients re-allocated). ID update is not included in the user flow. 
    patient_first_name TEXT NOT NULL,
    patient_last_name TEXT NOT NULL,
    patient_gender TEXT NOT NULL CHECK(
        patient_gender = 'not known' or
        patient_gender = 'male' or
        patient_gender = 'female' or
        patient_gender = 'non binary' or
        patient_gender = 'prefer not to say'),
    patient_birth_date DATE NOT NULL,
    patient_email TEXT NOT NULL,
    patient_password TEXT NOT NULL,
    patient_registration_date DATETIME NOT NULL,
    patient_NHS_blood_donor TEXT NOT NULL CHECK(
        patient_NHS_blood_donor = 'yes' or
        patient_NHS_blood_donor = 'no'), 
    patient_NHS_organ_donor TEXT NOT NULL CHECK(
        patient_NHS_organ_donor = 'yes' or
        patient_NHS_organ_donor = 'no'), 
    patient_status TEXT NOT NULL CHECK(
        patient_status = 'inactive' or
        patient_status = 'pending' or
        patient_status = 'confirmed'));
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
    -- If a patient is deleted, their medical records are no longer needed in the DB (assume archived/transferred to their new healthcare provider)
    patient_medical_condition_type_id TEXT REFERENCES patient_medical_condition_type (patient_medical_condition_type_id)
    ON DELETE CASCADE ON UPDATE CASCADE NOT NULL,
    -- We are not updating/deleting patient_medical_condition_type (patient_medical_condition_type_id) in the user flow so no special action on update/delete needed
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
    booking_id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
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
    -- For future appointments, Admin will update the associated GP before deletion, so no special action needed
    -- For past appointments, the old GP ID and name will remain in the booking table after the GP gets deleted;
    gp_last_name TEXT NOT NULL,
    patient_id INTEGER REFERENCES patient (gp_id) ON DELETE CASCADE ON UPDATE CASCADE);
    -- If a patient is deleted, their medical records are no longer needed in the DB (assume archived/transferred to their new healthcare provider)
""")

# Creating the prescription table.
c.execute("""
    CREATE TABLE IF NOT EXISTS prescription (
    prescription_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
    prescription_timestamp DATETIME NOT NULL,
    prescription_expiry_date DATETIME NOT NULL,
    drug_id INTEGER REFERENCES drug (drug_id),
    -- We are not updating/deleting drug (drug_id) in the user flow so no special action on update/delete needed
    drug_dosage TEXT NOT NULL,
    drug_frequency_dosage TEXT NOT NULL,
    booking_id INTEGER REFERENCES booking (booking_id) ON DELETE CASCADE ON UPDATE CASCADE NOT NULL);
    -- If an appointment is deleted, that means the corresponding patient has been deleted, so corresponding prescription(s) are no longer needed
""")

# Creating the drug table.
c.execute("""
    CREATE TABLE IF NOT EXISTS drug (
    drug_id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
    drug_name TEXT NOT NULL);
""")


# DUMMY DATA 
# Important: the autoincrement Primary Keys have to be unique and Not Null in the dummydata.csv file
# Otherwise, the import would not work. Meaning one can only import the dummydata.csv once, and then
# would need to change the dummydata.csv primary key value or take the database down.

# admin table dummy data
# 1 admin user. The system can support multiple admin users, but this is not essential. 
admin_csv = open("config/dummy_data/admin_dummydata.csv")
admin_rows = csv.reader(admin_csv)
c.executemany("INSERT INTO admin VALUES (?, ?, ?, ?, ?, ?, ?, ?)", admin_rows)

# booking table dummy data
# 50 bookings (appointments only as time-off/sick-leave require block-booking lots of slots) before 2020-12-25
booking_csv = open("config/dummy_data/booking_dummydata.csv")
booking_rows = csv.reader(booking_csv)
c.executemany("INSERT INTO booking VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", booking_rows)

# drug table dummy data
# 20 example drugs based on those most commonly presribed by NHS GPs.
drug_csv = open("config/dummy_data/drug_dummydata.csv")
drug_rows = csv.reader(drug_csv)
c.executemany("INSERT INTO drug VALUES (?, ?)", drug_rows)

# gp_department table dummy data
# 20 of the most important departments in NHS hospitals.
gp_department_csv = open("config/dummy_data/gp_department_dummydata.csv")
gp_department_rows = csv.reader(gp_department_csv)
c.executemany("INSERT INTO gp_department VALUES (?, ?)", gp_department_rows)

# gp table dummy data
# 10 example GPs (estimated average per GP practice in the UK) and 5 specialists (in other hospital departments)
gp_csv = open("config/dummy_data/gp_dummydata.csv")
gp_rows = csv.reader(gp_csv)
c.executemany("INSERT INTO gp VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", gp_rows)

# gp_specialisation table dummy data
# 15 of the most important specialisations for NHS doctors.
gp_specialisation_csv = open("config/dummy_data/gp_specialisation_dummydata.csv")
gp_specialisation_rows = csv.reader(gp_specialisation_csv)
c.executemany("INSERT INTO gp_specialisation VALUES (?, ?)", gp_specialisation_rows)

# patient table dummy data
# 50 example patients for conciseness (in reality, GPs have an average of c. 2,000 patients each!)
patient_csv = open("config/dummy_data/patient_dummydata.csv")
patient_rows = csv.reader(patient_csv)
c.executemany("INSERT INTO patient VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", patient_rows)

# patient_medical_condition table dummy data
# 30 medical condition relationships (some patients have none, some multiple).
patient_medical_condition_csv = open("config/dummy_data/patient_medical_condition_dummydata.csv")
patient_medical_condition_rows = csv.reader(patient_medical_condition_csv)
c.executemany("INSERT INTO patient_medical_condition VALUES (?, ?)", patient_medical_condition_rows)

# patient_medical_condition_type table dummy data
# 20 of the most common (primarily chronic) medical conditions in the UK.
patient_medical_condition_type_csv = open("config/dummy_data/patient_medical_condition_type_dummydata.csv")
patient_medical_condition_type_rows = csv.reader(patient_medical_condition_type_csv)
c.executemany("INSERT INTO patient_medical_condition_Type VALUES (?, ?)", patient_medical_condition_type_rows)

# prescription table dummy data
# 30 example prescriptions
prescription_csv = open("config/dummy_data/prescription_dummydata.csv")
prescription_rows = csv.reader(prescription_csv)
c.executemany("INSERT INTO prescription VALUES (?, ?, ?, ?, ?, ?, ?)", prescription_rows)


# DB CREATION COMPLETION

# Commit to db
conn.commit()

# Outputting outcome to user
print("DB successfully created")

# Close db
conn.close()
