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
- It is a working document based on assumptions about:
  - Structure of user flows
  - Best implementation method
- Add, modify or remove methods as appropriate

# `appointment`

| Name | Type | User flow & purpose | Parameters | Returns |
| ---- | ---- | ------------------- | ---------- | ------- |
| book | instance | <li>xxx | <li>N/A | <li>- |
| update | instance | <li>xxx | <li>N/A | <li>- |
| select_GP_upcoming | static | <li>xxx | <li>type = day/week/custom <li>gp_id <li>[time parameters] | <li>DF(s) incl. indexing w/ specific GP's appointments for an upcoming day (detailed, 1), week (less detailed, 1) or custom (1+) <br><i> If: custom is 1 day >> return day DF; <= 7 days >> return week DF format; > 7 days >> return multiple week DFs |
| select_patient_previous | static | <li>xxx | <li>patient_id | <li>DF incl. indexing of a specific patient's previous appointments (incl. ID and other relevant attributes) |
| select_patient_upcoming | static | <li>xxx | <li>patient_id | <li>DF incl. indexing of a specifi cpatient's upcoming appointments (incl. ID and other relevant attributes) |
| select_availability | static | <li>xxx | <li>type = day/week/custom <li>gp_id <li>[time parameters] | <li>DF(s) incl. indexing w/ specific GP's availability for an upcoming day (detailed, 1), week (less detailed, 1) or custom (1+) <br><i> If: custom is 1 day >> return day DF; <= 7 days >> return week DF format; > 7 days >> return multiple week DFs |
| select_other_availability | static | <li>xxx | <li>type = day/week/custom <li>gp_id <li>[time parameters] | <li>DF(s) incl. indexing w/ <b>all other GPs</b> (i.e. with gp_id not equal to the gp_id parameter passed) availability for an upcoming day (detailed, 1), week (less detailed, 1) or custom (1+) <br><i> If: custom is 1 day >> return day DF; <= 7 days >> return week DF format; > 7 days >> return multiple week DFs |
| cancel | static | <li>xxx | <li>booking_id | <li>- |

# `gp`

| Name | Type | User flow & purpose | Parameters | Returns |
| ---- | ---- | ------------------- | ---------- | ------- |
| insert | instance | <li>xxx | <li>N/A | <li>xxx |
| update | instance | <li>xxx | <li>N/A | <li>xxx |
| select | factory | <li>xxx | <li>gp_id | <li>xxx |
| select_list | static | <li> | <li>type = all/not_full | <li>xxx |
| change_status | static | <li>xxx | <li>gp_id <li>new_status | <li>xxx |
| delete | static | <li>xxx | <li>gp_id | <li>xxx |
| check_full | static | <li>xxx | <li>gp_id | <li>xxx |

# `patient`

| Name | Type | User flow & purpose | Parameters | Returns |
| ---- | ---- | ------------------- | ---------- | ------- |
| update | instance | <li>xxx | <li>N/A | <li>xxx |
| select | factory | <li>xxx | <li>gp_id | <li>xxx |
| select_list | static | <li>xxx | <li>type = pending/matching <li>if matching, DOB + letter_1_family_name | <li>xxx |
| confirm | static | <li>xxx | <li>type = all/single  <li>if single, patient_id | <li>xxx |
| delete | static | <li>xxx | <li>patient_id | <li>xxx |
| change_GP | static | <li>xxx | <li>patient_id <li>new_gp_id | <li>xxx |

# `prescription`

| Name | Type | User flow & purpose | Parameters | Returns |
| ---- | ---- | ------------------- | ---------- | ------- |
| insert | instance | <li>xxx | <li>N/A | <li>- |
| select_patient | static | <li>xxx | <li>patient_id | <li>DF of all of a given patient's prescriptions on record (incl. ID and other relevant attributes) |
| select_drug_list | static | <li>xxx | <li>- | <li>DF incl. indexing of all drugs in DB w/ ID and name |

# `record`

| Name | Type | User flow & purpose | Parameters | Returns |
| ---- | ---- | ------------------- | ---------- | ------- |
| update | instance | <li>xxx | <li>N/A | <li>xxx |
| select | factory | <li>xxx | <li>patient_id | <li>xxx |

# `schedule`

| Name | Type | User flow & purpose | Parameters | Returns |
| ---- | ---- | ------------------- | ---------- | ------- |
| select | static | <li>xxx | <li>type = day/week/custom <li>gp_id <li>[time parameters] | <li>DF(s) w/ specific GP's schedule for a day (detailed, 1), week (less detailed, 1) or custom (1+) <br><i> If: custom is 1 day >> return day DF; <= 7 days >> return week DF format; > 7 days >> return multiple week DFs |
| select_upcoming_timeoff | static | <li>xxx | <li>gp_id | <li>DF with GP's upcoming time off grouped by day (time off currently done only in whole days) |
| check_timeoff_conflict | static | <li>xxx | <li>gp_id <li>date_start <li>date_end | <li>BOOL True (no conflict w/ booked/confirmed appointments) or False (conflicts) |
| insert_timeoff | static | <li>xxx | <li>type = day/week/custom <li>gp_id <li>reason = time off/sick leave <li>[time parameters] | <li>- |
| delete_upcoming_timeoff | static | <li>xxx | <li>type = all/day/week/custom <li>gp_id <li>[time parameters] | <li>- |

# `user`
- Currently no methods (shared GP/patient instance attributes only)