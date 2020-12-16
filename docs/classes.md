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

## Outline

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

## Return Variables
Optional:
- Instance for factory methods
- Boolean for check functions such as check_timeoff_conflict() returned before 1. and 2.  

Always:
1. df_object (raw dataframe, for manipulation (e.g. deducing meaning of user input))  
2. df_print (to_markdown formatted dataframe, for printing)

Consult the code itself to see the objects returned. 

## User flow
- The corresponding user flows/purposes are outlined, but the exact 'place' for each method to be used is not defined (hopefully it's clear)
- Where user input selection is required based on a DF, the DF includes either an ID variable (e.g. booking_id) or a '[X]' index where the number/ordering don't change (e.g user attributes)
<br><br>

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
| select | factory | <li><b>Admin</b> <li> Generating an instance of a GP to later update attributes based on user input | <li>gp_id | <li> GP instance <br><br> Generally: DF incl. indexing of all of a GP's attributes (except password) <li> df_object <li> df_print |
| select_list | static | <li><b>Admin</b> <li>List of GPs to choose from (used in multiple branches) | <li>type = all/active/not_full | Generally: DF of all relevant GPs {gp_id, name (Dr. + gp_last_name), gp_birth_date, no. patients (if type = 'not_full'; sort column)} <li> df_object <li> df_print |
| select_table | static | <li><b>Admin</b> <li> List of GP departments/specialisations for reference when updating | <li>type = department/specialisation | Generally: DF of relevant DB table <li> df_object <li> df_print |
| change_status | static | <li><b>Admin</b> <li> Changing a GP's status (to inactive/active) | <li>gp_id <li>new_status | <i>NB: if deactivating, this auto-reallocates the GP's patients and future appointments to other GPs. </i> |
| delete | static | <li><b>Admin</b> <li> Deleting a GP | <li>gp_id | <i>NB: this auto-reallocates the GP's patients and future appointments to other GPs. </i> |
| check_not_full | static | <i>Used in Patient.change_gp() method</i> | <li>gp_id | <li>BOOL True (not full) or False (full) |
<br>

# `Patient`

| Name | Type | User flow & purpose | Parameters | Returns |
| ---- | ---- | ------------------- | ---------- | ------- |
| update | instance | <li><b>Admin</b> <li> Updating a patient's details (technically overriding every DB attribute w/ instance values) | - | - |
| select | factory | <li><b>Admin</b> <li> Generating an instance of a patient to later update attributes based on user input | <li>patient_id | <li>Patient instance <br><br> Generally: DF incl. indexing of all of a patient's attributes (except password, and medical conditions neither as that's for GPs to edit) <li> df_object <li> df_print |
| select_list | static | <li><b>Admin</b> <li> List of patients to choose from (used in multiple branches) | <li>type = pending/matching <li>if matching, patient_last_name | Generally: DF of all relevant patients {patient_id, default GP (if type = 'matching'), patient_first_name, patient_last_name, patient_birth_date, patient_registration_date (if type = 'pending'; sort column)} <li> df_object <li> df_print |
| confirm | static | <li><b>Admin</b> <li> Confirming patients (currently no direct method to change status to 'inactive', but allowed in DB) | <li>type = all/single  <li>if single, patient_id | <i>NB: patients were automatically given a GP during registration to avoid allowing nulls in the DB </i> |
| delete | static | <li><b>Admin</b> <li> Deleting a patient | <li>patient_id | - |
| change_GP | static | <li><b>Admin</b> <li> Changing a patient's default GP (checks GP not full first) | <li>patient_id <li>new_gp_id | <li>BOOL True (successful) or False (unsuccessful) |
<br>

# `Prescription`

| Name | Type | User flow & purpose | Parameters | Returns |
| ---- | ---- | ------------------- | ---------- | ------- |
| insert | instance | <li><b>GP</b> <li> Inserting a new prescription from an instance populated by user input (instance created in user flow) | - | - |
| select_patient | static | <i>Used in Record.select() method</i> | <li>patient_id | Generally: DF with details of a patient's prescriptions {drug_name, drug_dosage, drug_frequency_dosage, prescription_expiry_date (YYYY-MM-DD), booking_id} <li> df_object <li> df_print  |
| select_drug_list | static | <li><b>GP</b> <li> Getting a list of drugs to choose from (for a prescription) | - | Generally: DF with all drugs {drug_id, drug_name} <li> df_object <li> df_print |
<br>

# `Record`

| Name | Type | User flow & purpose | Parameters | Returns |
| ---- | ---- | ------------------- | ---------- | ------- |
| update | instance | <li><b>GP</b> <li>Updating a patient's medical record (technically overriding every DB attribute w/ instance values) | - | - |
| select | factory | <li><b>Admin, GP</b> <li> Generating an instance of a patient record to later update attributes based on user input. <li> Whilst lots of patient information is displayed, only 'conditions' and 'appointment notes' are editable (assume prescriptions are non-editable/revokable) | <li>patient_id | <li>Record instance <br><br> Generally: <b>2 DFs</b> incl. indexing of all of a patient's 'medical'-related details: 1) attributes & medical conditions 2) previous appointments & corresponding prescriptions <li> df_patient_object <li> df_patient_print <li> df_apps_object <li> df_apps_print |
| select_conditions | static | <li><b>GP</b> <li>List of possible medical conditions for reference when updating patient record | - | Generally: DF of all possible medical conditions <li> df_object <li> df_print |
<br>

# `Schedule`

| Name | Type | User flow & purpose | Parameters | Returns |
| ---- | ---- | ------------------- | ---------- | ------- |
| select | static | <li><b>Admin, GP</b> <li> Viewing a GP's schedule | <li>gp_id <li>type = day/week <li>start_date (YYYY-MM-DD) | Generally: DF of a specific GP's schedule for a given day (detailed) or week (less detailed per day) <li> df_object <li> df_print  |
| select_upcoming_timeoff | static | <li><b>Admin</b> <li> Viewing a GP's upcoming timeoff | <li>gp_id | Generally: DF of a GP's upcoming time off {booking_start_time (YYYY-MM-DD), booking_stats, booking_status_change_time} <li> df_object <li> df_print |
| check_timeoff_conflict | static | <li><b>Admin, GP</b> <li> Checking proposed GP timeoff doesn't conflict with any appointments | <li>gp_id <li>date_start (YYYY-MM-DD) <li>date_end (YYYY-MM-DD) | <li> BOOLean: 'True' if there was a conflict, 'False' is there was no conflict  DF of conflicting appointments {booking_id, booking_start_time, booking_status, booking_status_change_time} <li> df_object <li> df_print |
| insert_timeoff | static | <li><b>Admin, GP</b> <li> Inserting GP time off (only whole days possible) | <li>gp_id <li> timeoff_type = time off/sick leave <li>start_date (YYYY-MM-DD) <li>end_date (YYYY-MM-DD) | <li> 'time off was inserted' | 
| delete_upcoming_timeoff | static | <li><b>Admin, GP</b> <li> Deleting a GP's upcoming time off (e.g if no longer sick, holiday cancelled) (only whole days possible) | <li>gp_id <li>type = all/custom <li>timeoff_type = time off/sick leave <li>start_date (YYYY-MM-DD, None for type = all) <li>end_date (YYYY-MM-DD, None for type = all) | <li>all: 'all upcoming timeoffs were deleted' <li> custom: 'timeoffs were deleted for your indicated time period' |
<br>

# `User`
- Currently no methods (shared GP/Patient instance attributes only)
<br>