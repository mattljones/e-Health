# admin_flow.py

# library imports 
from pathlib import Path
import sys 

# Change python path for imports
p = Path(__file__).parents[1]
sys.path.insert(1, str(p))

# Importing utility methods from the 'system' package
from system import utils

# import global variables from globals.py
from system import globals


############################### INPUT MENU PAGES ###########################


############################ SEQUENTIAL STEPS MENUS ########################

def empty_method(next_dict):
    '''
    Empty method to be stored in the tuple of the dictionary of the user 
    choice doesn't require any specific steps and just redirects 
    '''
    return utils.display(next_dict)

########################## MENU NAVIGATION DICTIONARIES ######################

# Empty nested dictionary to store in tuple for last menu
# before going back to main page (for display function return parameter).
empty_dict = {"title": "CHANGES SAVED",
              "type":"sub"}
              



###### MANAGE GP ACCOUNTS SUB-MENU ######


delete_gp_account_final_menu = {
    "title": "NEXT ACTIONS",
    "type": "sub",
    "1": ("Delete Another GP", ,),
    "2": ("Section Menu", , manage_gp_accounts_flow)
}

deactivate_gp_account_final_menu = {
    "title": "NEXT ACTIONS",
    "type": "sub",
    "1": ("Deactivate Another GP", ,),
    "2": ("Section Menu", , manage_gp_accounts_flow)
}

add_new_gp_account_final_menu = {
    "title": "NEXT ACTIONS",
    "type": "sub",
    "1": ("Add Another GP", ,),
    "2": ("Section Menu", , manage_gp_accounts_flow)
}

#View/Edit GP Accounts Sub-menu
view_edit_gp_accounts_final_menu = {
    "title": "NEXT ACTIONS",
    "type": "sub",
    "1": ("View/Modify Same GP", ,),
    "2": ("GP List", ,),
    "3": ("Section Menu", , manage_gp_accounts_flow)
}

#
manage_gp_accounts_flow = {
    "title": "MANAGE GP ACCOUNTS",
    "type": "sub",
    "1":("View/Edit GP Details", ,),
    "2":("Add New GP Account", ,),
    "3":("Deactivate GP Account", ,),
    "4":("Delete GP Account", ,)
}

###### MANAGE PATIENT ACCOUNTS SUB-MENU ######

delete_patient_account_final_menu = {
    "title": "NEXT ACTIONS",
    "type": "sub",
    "1": ("Delete Another Patient", ,),
    "2": ("Section Menu", , manage_patient_accounts_flow)
}

add_new_patient_account_final_menu = {
    "title": "NEXT ACTIONS",
    "type": "sub",
    "1": ("Add Another Patient", ,),
    "2": ("Section Menu", , manage_patient_accounts_flow)
}

view_edit_patient_accounts_final_menu = {
    "title": "NEXT ACTIONS",
    "type": "sub",
    "1": ("View/Modify Same Patient", ,),
    "2": ("Patient Search Page", ,),
    "3": ("Section Menu", , manage_patient_accounts_flow)
}

manage_patient_accounts_flow = {
    "title": "MANAGE PATIENT ACCOUNTS",
    "type": "sub",
    "1":("View/Edit Patient Details", ,),
    "2":("Add New Patient Account", ,),
    "3":("Delete Patient Account", ,)
}

###### MANAGE GP-PATIENT PAIRINGS SUB-MENU ######

gp_patient_pairing_final_menu = {
    "title": "NEXT ACTIONS",
    "type": "sub",
    "1": ("View/Edit More Pairings", ,),
    "2": ("Section Menu", , gp_patient_pair_flow)
}

gp_patient_pair_flow = {
    "title": "SEARCH FOR A GP OR PATIENT",
    "type": "sub",
    "1": ("Search By Patient", ,),
    "2": ("Search By GP", ,),
}

###### MANAGE GP SCHEDULES SUB-MENU ######

remove_time_off_final_actions = {
    "title": "NEXT ACTIONS",
    "type": "sub",
    "1": ("Remove More Time Off", , remove_time_off_flow),
    "2": ("Manage Upcoming Time Off", , manage_time_off_flow),
    "3": ("Manage GP Availability", , manage_availability_flow),
    "4": ("Choose a different GP", , ),
    "5": ("Section Menu", , view_schedule_flow)
}

remove_time_off_flow = {
    "title": "SELECT TIME OFF LENGTH",
    "type": "sub",
    "1": ("All", ,)
    "2": ("Day", ,),
    "3": ("Week", ,),
    "4": ("Custom", , )
}

appointment_conflict_final_actions = {
    "title": "NEXT ACTIONS",
    "type": "sub",
    "1": ("Try Adding Again", , add_time_off_flow),
    "2": ("Manage Upcoming Time Off", , manage_time_off_flow),
    "3": ("Manage GP Availability", , manage_availability_flow),
    "4": ("Choose a different GP", , ),
    "5": ("Section Menu", , view_schedule_flow)
}

add_time_off_final_actions = {
    "title": "NEXT ACTIONS",
    "type": "sub",
    "1": ("Add More Time Off", , add_time_off_flow),
    "2": ("Remove Time Off", , remove_time_off_flow),
    "3": ("Choose a different GP", , ),
    "4": ("Section Menu", , view_schedule_flow)
}

add_time_off_flow = {
    "title": "SELECT TIME OFF LENGTH",
    "type": "sub",
    "1": ("Day", ,),
    "2": ("Week", ,),
    "3": ("Custom", , ),
}

view_time_off_final_actions = {
    "title": "NEXT ACTIONS",
    "type": "sub",
    "1": ("Add Time Off", , add_time_off_flow),
    "2": ("Remove Time Off", , remove_time_off_flow),
    "3": ("Manage GP Availability", , manage_availability_flow),
    "4": ("Choose a different GP", , ),
    "5": ("Section Menu", , view_schedule_flow)
}

manage_time_off_flow = {
    "title": "MANAGE TIME OFF",
    "type": "sub",
    "1": ("View", ,),
    "2": ("Add", ,),
    "3": ("Remove", ,)
}

manage_availability_flow = {
    "title": "MANAGE AVIALABILITY",
    "type": "sub",
    "1": ("View/Cancel Upcoming Appointments", ,),
    "2": ("Manage Upcoming Time Off", ,)
}

view_schedule_final_actions = {
    "title": "NEXT ACTIONS",
    "type": "sub",
    "1": ("Modify GP Availability", , manage_availability_flow),
    "2": ("View a Different Time Period", , schedule_length_flow),
    "3": ("Choose a different GP", , ),
    "4": ("Section Menu", , view_schedule_flow),
}

schedule_length_flow = {
    "title": "SELECT SCHEDULE LENGTH",
    "type": "sub",
    "1": ("Day", ,),
    "2": ("Week", ,),
    "3": ("Custom", , )
}

view_schedule_flow = {
    "title": "VIEW AND MANAGE SCHEDULE",
    "type": "sub",
    "1": ("View GP Schedule", ,),
    "2": ("Manage GP Availability", ,)
}

###### MANAGE UPCOMING APPOINTMENTS SUB-MENU ######


delete_gp_appointment_flow ={
    "title": "SELECT APPOINTMENT DATE",
    "type": "sub",
    "1": ("Day", ,),
    "2": ("Week", ,),
    "3": ("Custom", ,)
}

appointment_deleted_patient_final_actions = {
    "title": "NEXT ACTIONS",
    "type": "sub",
    "1": ("View Other Appointments For This Patient", , ),
    "2": ("View Another Patient's Appointments", ,),
    "3": ("search by GP/Date", ,view_cancel_appointment_flow ),
    "4": ("Section Menu", , manage_appointment_flow)
}

view_cancel_appointment_flow = {
    "title": "VIEW OR CANCEL AN UPCOMING APPOINTMENT",
    "type": "sub",
    "1": ("Search By Patient", , ),
    "2": ("Search By GP", ,)
}

gp_availability_error_final_actions = {
    "title": "NEXT ACTIONS",
    "type": "sub",
    "1": ("Try again", , add_new_appointment_flow),
    "2": ("Add Another Appointment", ,add_new_appointment_flow),
    "3": ("Section Menu", , manage_appointment_flow)
}

appointment_made_final_actions = {
    "title": "NEXT ACTIONS",
    "type": "sub",
    "1": ("Add Another Appointment For This Patient", , add_new_appointment_flow),
    "2": ("Add Another Appointment For Another Patient", ,),
    "3": ("Section Menu", , manage_appointment_flow)
}

availability_error_flow = {
    "title": "NO PATIENT AVAILABILITY",
    "type": "sub",
    "1": ("Choose a Different Time", , add_new_appointment_flow),
    "2": ("View Slots Available With Any GP", ,)
}

add_new_appointment_flow = {
    "title": "SELECT APPOINTMENT DATE",
    "type": "sub",
    "1": ("Day", ,),
    "2": ("Week", ,),
    "3": ("Custom", ,)
}

manage_appointment_flow = {
    "title": "MANAGE APPOINTMENTS",
    "type": "sub",
    "1": ("Add a New Appointment", ,),
    "2": ("View/Cancel Upcoming Appointment", ,)
}

###### VIEW APPOINTMENT SUMMARIES SUB-MENU ######
appointment_summary_final_actions = {
    "title": "NEXT ACTIONS",
    "type": "sub",
    "1": ("View a Different Appointment", , appointment_summary_date_flow),
    "2": ("View a Different Patient", , ),
}

appointment_summary_date_flow = {
    "title": "SELECT APPOINTMENT DATE",
    "type": "sub",
    "1": ("Day", ,),
    "2": ("Week", ,),
    "3": ("Custom", ,)
}

###### MAIN MENU ####

main_flow = {
    "title": "ADMIN MAIN MENU",
    "type":"main",
    "1":("Manage GP Accounts", , manage_gp_accounts_flow),
    "2":("Manage Patient Accounts", ,manage_patient_accounts_flow ),
    "3":("Manage GP-Patient Pairings", , manage_pairings_flow),
    "4":("Manage GP Schedules", , manage_schedules_flow),
    "5":("Manage Upcoming Appointments", , manage_appointments_flow),
    "6":("View Appointment Summaries", , view_summaries_flow)
}