---
marp: true
paginate: true
---

<style>
h1 {color: #486BD3;
    text-align: center
}
</style>

# Background

- This document describes the different class methods in detail, including:
  - Name
  - Type
  - User flow & purpose
  - Parameters
  - Return objects
- It is a working document based on hypotheses about:
  - Structure of user flows
  - Best implementation method
- Add, modify or remove methods as appropriate

# `Appointment`

| Name | Type | User flow & purpose | Parameters | Returns |
| ---- | ---- | ------------------- | ---------- | ------- |
| book | instance | <li><b>Admin, Patient</b> <li>Booking an appointment from an instance (instance created in user flow) | - | - |
| update | instance | <li><b>Admin, GP</b> <li> Updating an appointment's details (technically overriding every DB attribute w/ instance values) | - | - |
| select | factory | <li><b>Admin, GP</b> <li> Generating an instance of an appointment to later update attributes based on user input | <li>booking_id | <li>Appointment instance <li>DF incl. indexing of all appointment attributes (not incl. prescription) |
| select_GP | static | <li><b>Admin, GP</b> <li> Getting a list of a GP's appointments in a given time period | <li>type = day/week <li>gp_id <li>[time parameters] | <li>DF of a specific GP's appointments for an upcoming day (detailed) or week (less detailed per day) |
| select_GP_pending | static | <li><b>GP</b> <li> Getting a list of a GP's pending (awaiting confirmation) appointments | <li>gp_id | <li>DF of a specific GP's pending appointments incl. all relevant attributes (sorted by booking_start_time ASC) |
| select_patient_previous | static | <i>Used in Record.select() method</i> | <li>patient_id | <li>DF of a specific patient's previous appointments (incl. ID and other relevant attributes) |
| select_patient_upcoming | static | <li><b>Admin, Patient</b> <li>Getting a list of a patient's upcoming appointments | <li>patient_id | <li>DF of a specific patient's upcoming appointments (incl. ID and other relevant attributes) |
| select_availability | static | <li><b>Admin, Patient</b> <li> Getting a specific GP's availability before booking an appointment | <li>type = day/week <li>gp_id <li>[time parameters] | <li>DF incl. indexing of a specific GP's availability for an upcoming day (detailed) or week (less detailed per day) <br><i>NB: in user flow, to 'check' for availability count rows in DF</i> |
| select_other_availability | static | <li><b>Admin, Patient</b> <li> Getting alternative GP availabilities when a patient's own GP has none before booking an appointment | <li>type = day/week <li>gp_id <li>[time parameters] | <li>DF incl. indexing w/ <b>all other GPs'</b> (i.e. with gp_id not equal to the gp_id parameter passed) availability for an upcoming day (detailed) or week (less detailed per day) <br><i>NB: in user flow, to 'check' for availability count rows in DF |
| change_status | static | <li><b>Admin, Patient, GP</b> <li> Changing status for different reasons e.g. cancelling, confirming, rejecting | <li>booking_id <li>new_status | - |
| confirm_all_GP_pending | static | <li><b>GP</b> <li> Confirming all pending appointments | <li>gp_id | - |
<br>

# `GP`

| Name | Type | User flow & purpose | Parameters | Returns |
| ---- | ---- | ------------------- | ---------- | ------- |
| insert | instance | <li><b>Admin</b> <li> Inserting a new GP from an instance populated by user input (GPs cannot register themselves; instance created in user flow) | - | - |
| update | instance | <li><b>Admin</b> <li> Updating a GP's details (technically overriding every DB attribute w/ instance values) | - | - |
| select | factory | <li><b>Admin</b> <li> Generating an instance of a GP to later update attributes based on user input | <li>gp_id | <li> GP instance <li> DF incl. indexing of all of a GP's attributes (except password) |
| select_list | static | <li><b>Admin</b> <li>List of GPs to choose from (used in multiple branches) | <li>type = all/not_full | <li>DF of all relevant GPs {gp_id, no. patients (if type = 'not_full'; sort column), name (Dr. + gp_last_name), gp_birth_date} |
| select_departments | static | <li><b>Admin</b> <li> List of GP departments for reference when updating | - | <li> DF of all GP departments |
| select_specialisations | static | <li><b>Admin</b> <li> List of GP specialisations for reference when updating | - | <li> DF of all GP specialisations |
| change_status | static | <li><b>Admin</b> <li> Changing a GP's status (to inactive/active) | <li>gp_id <li>new_status | <i>NB: if deactivating, this auto-reallocates the GP's patients and future appointments to other GPs. </i> |
| delete | static | <li><b>Admin</b> <li> Deleting a GP | <li>gp_id | <i>NB: this auto-reallocates the GP's patients and future appointments to other GPs. </i> |
| check_not_full | static | <li><b>Admin</b> <li> Checking a GP is not full before giving them an additional patient (since DB might have changed since GP.select_list(not_full) was called) | <li>gp_id | <li>BOOL True (not full) or False (full) |
<br>

# `Patient`

| Name | Type | User flow & purpose | Parameters | Returns |
| ---- | ---- | ------------------- | ---------- | ------- |
| update | instance | <li><b>Admin</b> <li> Updating a patient's details (technically overriding every DB attribute w/ instance values) | - | - |
| select | factory | <li><b>Admin</b> <li> Generating an instance of a patient to later update attributes based on user input <br> <i>Used in Record.select() method</i> | <li>patient_id | <li>Patient instance <li>DF incl. indexing of all of a patient's attributes (except password, and medical conditions neither as that's for GPs to edit) |
| select_list | static | <li><b>Admin</b> <li> List of patients to choose from (used in multiple branches) | <li>type = pending/matching <li>if matching, patient_last_name | <li>DF of all relevant patients {patient_id, patient_registration_date (if type = 'pending'; sort column), patient_first_name, patient_last_name, patient_birth_date, gp_id (if type = 'matching')} |
| confirm | static | <li><b>Admin</b> <li> Confirming patients (currently no direct method to change status to 'inactive', but allowed in DB) | <li>type = all/single  <li>if single, patient_id | <i>NB: patients were automatically given a GP during registration to avoid allowing nulls in the DB </i> |
| delete | static | <li><b>Admin</b> <li> Deleting a patient | <li>patient_id | - |
| change_GP | static | <li><b>Admin</b> <li> Changing a patient's default GP | <li>patient_id <li>new_gp_id | - |
<br>

# `Prescription`

| Name | Type | User flow & purpose | Parameters | Returns |
| ---- | ---- | ------------------- | ---------- | ------- |
| insert | instance | <li><b>GP</b> <li> Inserting a new prescription from an instance populated by user input (instance created in user flow) | - | - |
| select_patient | static | <i>Used in Record.select() method</i> | <li>patient_id | <li>DF of all of a given patient's prescriptions on record (incl. ID and other relevant attributes) |
| select_drug_list | static | <li><b>GP</b> <li> Getting a list of drugs to choose from (for a prescription) | - | <li>DF of all drugs in DB {drug_id, drug_name} |
<br>

# `Record`

| Name | Type | User flow & purpose | Parameters | Returns |
| ---- | ---- | ------------------- | ---------- | ------- |
| update | instance | <li><b>GP</b> <li>Updating a patient's medical record (technically overriding every DB attribute w/ instance values) | - | - |
| select | factory | <li><b>Admin, GP</b> <li> Generating an instance of a patient record to later update attributes based on user input (Admin can view only) | <li>patient_id | <i> Calls Appointment.select_patient_previous(), Patient.select() and Prescription.select_patient() </i> <li>Record instance <li>DF incl. indexing of all of a patient's 'medical' attributes <li> DF incl. indexing of patient's past appointments integrated with corresponding prescriptions |
<br>

# `Schedule`

| Name | Type | User flow & purpose | Parameters | Returns |
| ---- | ---- | ------------------- | ---------- | ------- |
| select | static | <li><b>Admin, GP</b> <li> Viewing a GP's schedule | <li>type = day/week <li>gp_id <li>[time parameters] | <li>DF of a specific GP's schedule for a given day (detailed) or week (less detailed per day) |
| select_upcoming_timeoff | static | <li><b>Admin</b> <li> Viewing a GP's upcoming timeoff (currently all future timeoff and sick leaves are shown) | <li>gp_id | <li>DF of a GP's upcoming time off {booking_id, booking_start_time, booking_status, booking_type, booking_status_change_time} |
| check_timeoff_conflict | static | <li><b>Admin, GP</b> <li> Checking proposed GP timeoff doesn't conflict with any appointments (not checking for working days) | <li>gp_id <li>date_start <li>date_end | <li> BOOLean: 'True' if there was a conflict, 'False' is there was no conflict  <li> old: DF of conflicting appointments {booking_id, booking_start_time, booking_status, booking_status_change_time, patient name (patient_first_name + patient_last_name)} <br><i>NB: in user flow, to 'check' for conflicts count rows in DF |
| insert_timeoff | static | <li><b>Admin, GP</b> <li> Inserting GP time off (only custom, as I believe that GPs are more interested to put in custom ranges rather than week or days because time offs are always planned and thereby pretty much defined at the time of insertion) | <li>gp_id <li>timeoff_type = time off/sick leave <li>start_date <li>end_date | <li> 'custom time_off insertion done' | 
| delete_upcoming_timeoff | static | <li><b>Admin, GP</b> <li> Deleting a GP's upcoming time off (e.g if no longer sick, holiday cancelled) (only in whole days for now) | <li>gp_id <li>type = all/day/week/custom <li>timeoff_type = time off/sick leave <li>start_date <li>end_date | <li>all: 'all upcoming timeoffs were deleted'<li>custom: 'all timeoffs for the customs date range were deleted' |
<br>

# `User`
- Currently no methods (shared GP/Patient instance attributes only)
<br>