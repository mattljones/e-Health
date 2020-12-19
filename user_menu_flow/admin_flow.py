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

from classes import gp
from classes import patient


############################### INPUT MENU PAGES ###########################

###### MANAGE GP ACCOUNTS FUNCTIONS ######

def gp_account_section_menu(next_dict):
    '''
    Returns to the section menu.
    '''
    pass

def view_gp(next_dict):
    '''
    Select a list of GPs and allows choice for viewing.
    '''
    pass

def retrieve_gp_list(type):
    df = gp.select_list('all')
    print("\n----------------------------------------------------\n"
          "                ", "PLEASE SELECT A GP", "\n")
    print(df[1])
    choice = input('Select a GP: ')
    return df[choice]

def same_gp(next_dict):
    '''
    Allows viewing of the same GP from the final menu.
    '''

def add_gp(next_dict):
    '''
    Adds a new GP.
    '''
    pass

def deactivate_gp(next_dict):
    '''
    Deactivates a GP.
    '''
    pass

def delete_gp(next_dict):
    '''
    Deletes a GP.
    '''
    pass

###### MANAGE PATIENT ACCOUNTS FUNCTIONS ######

def patient_account_section_menu(next_dict):
    '''
    Returns to the section menu.
    '''
    pass

def choose_patient(next_dict):
    '''
    Choose patient account.
    '''

def view_patient(next_dict):
    '''
    View a Patient Account.
    '''
    pass

def confirm_patient(next_dict):
    '''
    Confirm pending patient registrations.
    '''
    pass

def delete_patient(next_dict):
    '''
    Delete a patient account
    '''
    pass

###### MANAGE GP-PATIENT PAIRINGS FUNCTIONS ######

def pairings_section_menu(next_dict):
    '''
    Returns to the section menu.
    '''
    pass

def pairing_gp(next_dict):
    '''
    Search for a patient and pair them up with a GP.
    '''
    pass

def pairing_patient(next_dict):
    '''
    Select a GP and pair patients to them if they are not full.
    '''
    pass

###### MANAGE GP SCHEDULES FUNCTIONS ######

def schedules_main(next_dict):
    '''
    Returns the numbered list of GPs to choose from
    '''
    pass

def schedules_section_menu(next_dict):
    '''
    Returns to the section menu.
    '''
    pass

def schedule_date(next_dict):
    '''
    Choice of schedule date period.
    '''
    pass

def view_schedule(next_dict):
    '''
    View a GP's current schedule.
    '''    
    pass

def manage_availability(next_dict):
    '''
    Manage the availability of GPs.
    '''
    pass

def modify_availability(next_dict):
    '''
    Change a GP's availability.
    '''
    pass

def manage_time_off(next_dict):
    '''
    Manage a GP's time off.
    '''
    pass

def view_time_off(next_dict):
    '''
    View a GP's current time off.
    '''
    pass

def add_time_off(next_dict):
    '''
    Add time off to a GP's schedule.
    '''
    pass

def remove_time_off(next_dict):
    '''
    Remove time off from a GP's schedule.
    '''
    pass

###### MANAGE UPCOMING APPOINTMENTS FUNCTIONS ######

def appointments_section_menu(next_dict):
    '''
    Returns to the section menu.
    '''
    pass

def add_appointment(next_dict):
    '''
    Schedule an appointment for a GP.
    '''
    pass

def view_appointment(next_dict):
    '''
    View a current list of appointments.
    '''
    pass

def appointment_by_patient(next_dict):
    '''
    Find a patient's upcoming appointments.
    '''
    pass

def appointment_check(next_dict):
    '''
    Check whether the appointment selected is available.
    '''
    pass

def appointment_by_gp(next_dict):
    '''
    Find a GP's upcoming appointments with date options.
    '''
    pass

def delete_appointment(next_dict):
    '''
    Allows deleting of appointments.
    '''
    pass


###### APPOINTMENT SUMMARIES FUNCTIONS ######

def summaries_section_menu(next_dict):
    '''
    Returns to the section menu.
    '''
    pass

def appointment_summary_date(next_dict):
    '''
    Returns the appointment summaries based on the user choice.
    '''
    pass

def appointment_summary_patient(next_dict):
    '''
    Allows for searching of appointment summaries by patient.
    '''
    pass

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
              

yes_no_flow = {
    "title": " ",
    "type": "sub",
    "1": ("Yes", empty_method, empty_dict),
    "2": ("No", empty_method, empty_dict),
}


###### MANAGE GP ACCOUNTS SUB-MENU ######


delete_gp_account_final_menu = {
    "title": "NEXT ACTIONS",
    "type": "sub",
    "1": ("Delete Another GP", delete_gp,),
    "2": ("Section Menu", gp_account_section_menu, empty_dict)
}

deactivate_gp_account_final_menu = {
    "title": "NEXT ACTIONS",
    "type": "sub",
    "1": ("Deactivate Another GP", deactivate_gp,),
    "2": ("Section Menu", gp_account_section_menu, empty_dict)
}

add_new_gp_account_final_menu = {
    "title": "NEXT ACTIONS",
    "type": "sub",
    "1": ("Add Another GP", add_gp, empty_dict),
    "2": ("Section Menu", gp_account_section_menu, empty_dict)
}

view_edit_gp_accounts_final_menu = {
    "title": "NEXT ACTIONS",
    "type": "sub",
    "1": ("View/Modify Same GP", same_gp, empty_dict),
    "2": ("GP List", retrieve_gp_list, empty_dict),
    "3": ("Section Menu", gp_account_section_menu, empty_dict)
}

manage_gp_accounts_flow = {
    "title": "MANAGE GP ACCOUNTS",
    "type": "sub",
    "1":("View/Edit GP Details", view_gp, view_edit_gp_accounts_final_menu),
    "2":("Add New GP Account", add_gp, add_new_gp_account_final_menu),
    "3":("Deactivate GP Account", deactivate_gp, deactivate_gp_account_final_menu),
    "4":("Delete GP Account", delete_gp, delete_gp_account_final_menu)
}

###### MANAGE PATIENT ACCOUNTS SUB-MENU ######

delete_patient_account_final_menu = {
    "title": "NEXT ACTIONS",
    "type": "sub",
    "1": ("Delete Another Patient", delete_patient, empty_dict),
    "2": ("Section Menu", patient_account_section_menu, empty_dict)
}

add_new_patient_account_final_menu = {
    "title": "NEXT ACTIONS",
    "type": "sub",
    "1": ("Add Another Patient", confirm_patient, empty_dict),
    "2": ("Section Menu", patient_account_section_menu, empty_dict)
}

view_edit_patient_accounts_final_menu = {
    "title": "NEXT ACTIONS",
    "type": "sub",
    "1": ("View/Modify Same Patient", view_patient, empty_dict),
    "2": ("Patient Search Page", choose_patient, empty_dict),
    "3": ("Section Menu", patient_account_section_menu, empty_dict)
}

manage_patient_accounts_flow = {
    "title": "MANAGE PATIENT ACCOUNTS",
    "type": "sub",
    "1":("View/Edit Patient Details", view_patient, view_edit_patient_accounts_final_menu),
    "2":("Add New Patient Account", confirm_patient, add_new_patient_account_final_menu),
    "3":("Delete Patient Account", delete_patient, delete_patient_account_final_menu)
}

###### MANAGE GP-PATIENT PAIRINGS SUB-MENU ######

gp_patient_pairing_final_menu = {
    "title": "NEXT ACTIONS",
    "type": "sub",
    "1": ("View/Edit More Pairings", pairings_section_menu, empty_dict),
}

gp_patient_pair_flow = {
    "title": "SEARCH FOR A GP OR PATIENT",
    "type": "sub",
    "1": ("Search By Patient", pairing_patient, gp_patient_pairing_final_menu),
    "2": ("Search By GP", pairing_gp, gp_patient_pairing_final_menu),
}

###### MANAGE GP SCHEDULES SUB-MENU ######

remove_time_off_final_actions = {
    "title": "NEXT ACTIONS",
    "type": "sub",
    "1": ("Remove More Time Off", remove_time_off, empty_dict),
    "2": ("Manage Upcoming Time Off", manage_time_off, empty_dict),
    "3": ("Manage GP Availability", manage_availability, empty_dict),
    "4": ("Choose a different GP", schedules_main, empty_dict),
    "5": ("Section Menu", schedules_section_menu, empty_dict
}

remove_time_off_flow = {
    "title": "SELECT TIME OFF LENGTH",
    "type": "sub",
    "1": ("All", empty_method, remove_time_off_final_actions),
    "2": ("Day", empty_method, remove_time_off_final_actions),
    "3": ("Week", empty_method, remove_time_off_final_actions),
    "4": ("Custom", empty_method, remove_time_off_final_actions)
}

appointment_conflict_final_actions = {
    "title": "NEXT ACTIONS",
    "type": "sub",
    "1": ("Try Adding Again", add_time_off, empty_dict),
    "2": ("Manage Upcoming Time Off", manage_time_off, empty_dict,
    "3": ("Manage GP Availability", manage_availability, empty_dict,
    "4": ("Choose a different GP", schedules_main, empty_dict),
    "5": ("Section Menu", schedules_section_menu, empty_dict)
}

add_time_off_final_actions = {
    "title": "NEXT ACTIONS",
    "type": "sub",
    "1": ("Add More Time Off", add_time_off, empty_dict),
    "2": ("Remove Time Off", remove_time_off, remove_time_off_flow),
    "3": ("Choose a different GP", schedules_main, empty_dict),
    "4": ("Section Menu", schedules_section_menu, empty_dict)
}

add_time_off_flow = {
    "title": "SELECT TIME OFF LENGTH",
    "type": "sub",
    "1": ("Day", empty_method, add_time_off_final_actions),
    "2": ("Week", empty_method, add_time_off_final_actions),
    "3": ("Custom", empty_method, add_time_off_final_actions),
}

view_time_off_final_actions = {
    "title": "NEXT ACTIONS",
    "type": "sub",
    "1": ("Add Time Off", add_time_off, add_time_off_flow),
    "2": ("Remove Time Off", remove_time_off, remove_time_off_flow),
    "3": ("Manage GP Availability", manage_availability, empty_dict),
    "4": ("Choose a different GP", schedules_main, empty_dict),
    "5": ("Section Menu", schedules_section_menu, empty_dict)
}

manage_time_off_flow = {
    "title": "MANAGE TIME OFF",
    "type": "sub",
    "1": ("View", view_time_off, view_time_off_final_actions),
    "2": ("Add", add_time_off, add_time_off_flow),
    "3": ("Remove", remove_time_off, remove_time_off_flow)
}

manage_availability_flow = {
    "title": "MANAGE AVIALABILITY",
    "type": "sub",
    "1": ("View/Cancel Upcoming Appointments", view_appointment, empty_dict),
    "2": ("Manage Upcoming Time Off", manage_time_off, manage_time_off_flow)
}

view_schedule_final_actions = {
    "title": "NEXT ACTIONS",
    "type": "sub",
    "1": ("Modify GP Availability", manage_availability, empty_dict),
    "2": ("View a Different Time Period", schedule_date, empty_dict,
    "3": ("Choose a different GP", schedules_main, empty_dict),
    "4": ("Section Menu", schedules_section_menu, empty_dict)
}

schedule_length_flow = {
    "title": "SELECT SCHEDULE LENGTH",
    "type": "sub",
    "1": ("Day", view_schedule, view_schedule_final_actions),
    "2": ("Week", view_schedule, view_schedule_final_actions),
    "3": ("Custom", view_schedule, view_schedule_final_actions)
}

view_schedule_flow = {
    "title": "VIEW AND MANAGE SCHEDULE",
    "type": "sub",
    "1": ("View GP Schedule", schedule_date, schedule_length_flow),
    "2": ("Manage GP Availability", manage_availability, manage_availability_flow)
}

###### MANAGE UPCOMING APPOINTMENTS SUB-MENU ######

appointment_deleted_gp_final_actions = {
    "title": "NEXT ACTIONS",
    "type": "sub",
    "1": ("View Other Appointments For This GP", appointment_by_gp, empty_dict),
    "2": ("View Another Patient's Appointments", appointment_by_patient, empty_dict),
    "3": ("Search by GP/Date", appointment_by_gp, empty_dict),
    "4": ("Section Menu", appointments_section_menu, empty_dict)
}

delete_gp_appointment_flow ={
    "title": "SELECT APPOINTMENT DATE",
    "type": "sub",
    "1": ("Day", delete_appointment, appointment_deleted_gp_final_actions),
    "2": ("Week", delete_appointment,appointment_deleted_gp_final_actions),
    "3": ("Custom", delete_appointment, appointment_deleted_gp_final_actions)
}

appointment_deleted_patient_final_actions = {
    "title": "NEXT ACTIONS",
    "type": "sub",
    "1": ("View Other Appointments For This Patient", appointment_by_patient, empty_dict),
    "2": ("View Another Patient's Appointments", view_appointment, empty_dict),
    "3": ("Search by GP/Date", appointment_by_gp, empty_dict),
    "4": ("Section Menu", appointments_section_menu, empty_dict)
}

view_cancel_appointment_flow = {
    "title": "VIEW OR CANCEL AN UPCOMING APPOINTMENT",
    "type": "sub",
    "1": ("Search By Patient", appointment_by_patient, appointment_deleted_patient_final_actions),
    "2": ("Search By GP", appointment_by_gp, delete_gp_appointment_flow)
}

gp_availability_error_final_actions = {
    "title": "NEXT ACTIONS",
    "type": "sub",
    "1": ("Try again", appointment_by_gp, empty_dict),
    "2": ("Add Another Appointment", add_appointment, empty_dict),
    "3": ("Section Menu", appointments_section_menu, empty_dict)
}

appointment_made_final_actions = {
    "title": "NEXT ACTIONS",
    "type": "sub",
    "1": ("Add Another Appointment For This Patient", add_appointment, empty_dict),
    "2": ("Add Another Appointment For Another Patient", add_appointment, empty_dict),
    "3": ("Section Menu", appointments_section_menu, empty_dict)
}

availability_error_flow = {
    "title": "NO PATIENT AVAILABILITY",
    "type": "sub",
    "1": ("Choose a Different Time", add_appointment, empty_dict),
    "2": ("View Slots Available With Any GP", appointment_by_gp, empty_dict)
}

add_new_appointment_flow = {
    "title": "SELECT APPOINTMENT DATE",
    "type": "sub",
    "1": ("Day", appointment_patient, empty_dict),
    "2": ("Week", appointment_by_patient, empty_dict),
    "3": ("Custom", appointment_by_patient,empty_dict)
}

manage_appointment_flow = {
    "title": "MANAGE APPOINTMENTS",
    "type": "sub",
    "1": ("Add a New Appointment", add_appointment, add_new_appointment_flow),
    "2": ("View/Cancel Upcoming Appointment", view_appointment, view_cancel_appointment_flow)
}

###### VIEW APPOINTMENT SUMMARIES SUB-MENU ######

appointment_summary_final_actions = {
    "title": "NEXT ACTIONS",
    "type": "sub",
    "1": ("View a Different Appointment", appointment_summary_date, empty_dict),
    "2": ("View a Different Patient", appointment_summary_patient, empty_dict),
}

appointment_summary_date_flow = {
    "title": "SELECT APPOINTMENT DATE",
    "type": "sub",
    "1": ("Day", appointment_summary_date, appointment_summary_final_actions),
    "2": ("Week", appointment_summary_date, appointment_summary_final_actions),
    "3": ("Custom", appointment_summary_date, appointment_summary_final_actions)
}

###### MAIN MENU ####

main_flow = {
    "title": "ADMIN MAIN MENU",
    "type":"main",
    "1":("Manage GP Accounts", empty_method, manage_gp_accounts_flow),
    "2":("Manage Patient Accounts", empty_method, manage_patient_accounts_flow ),
    "3":("Manage GP-Patient Pairings", empty_method, manage_pairings_flow),
    "4":("Manage GP Schedules", schedules_main, manage_schedules_flow),
    "5":("Manage Upcoming Appointments", empty_method, manage_appointments_flow),
    "6":("View Appointment Summaries", empty_method, view_summaries_flow)
}