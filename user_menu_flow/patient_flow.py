# patient_flow.py

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

# TODO: fill in the function corresponding to user choices (below)
############################### INPUT MENU PAGES ###########################

def book_personal_gp(next_dict):
    '''
    '''
    return utils.display(next_dict)


def book_other_gp(next_dict):
    '''
    '''
    return utils.display(next_dict)


############################ SEQUENTIAL STEPS MENUS ########################

def empty_method(next_dict):
    '''
    Empty method to be stored in the tuple of the dictionary of the user 
    choice doesn't require any specific steps and just redirects 
    '''
    return utils.display(next_dict)

def manage_appointment(next_dict):
    '''
    '''
    # SQL query qhether the patient has an appointment booked
    # Hardcoded for now
    ##################
    has_appointment = False
    had_appointment = True
    #################

    if has_appointment:
        return utils.display(next_dict["has"])

    elif had_appointment:
        return utils.display(next_dict["had"])

    else:
        return utils.display(next_dict["has_not"])

def change_GP_pair(next_dict):
    '''
    '''
    return utils.display(next_dict)

def read_messages(next_dict):
    '''
    '''
    return utils.display(next_dict)

def cancel_appointment(next_dict):
    '''
    '''
    return utils.display(next_dict)

def download_prescription(next_dict):
    '''
    '''
    return utils.display(next_dict)


######################### MENU NAVIGATION DICTIONARIES ######################

# Empty nested dictionary to store in tuple for last menu
# before going back to main page (for display function return parameter).
empty_dict = {"title": "CHANGES SAVED",
              "type":"sub"}


# "Book with registered GP ???" page dictionary
flow_11 =  {"title": "BOOK WITH REGISTERED GP ?",
            "type":"sub",
            "1":("Yes",book_personal_gp,empty_dict),
            "2":("No, book with another GP",book_other_gp,empty_dict)}


# "Manage/Book appointment" page dictionary
flow_1  = {"has_not":
                {"title": "BOOK APPOINTMENT ?",
                "type":"sub",
                "1":("Yes",empty_method,flow_11)},
          "has":
                {"title": "MANAGE APPOINTMENT",
                "type":"sub",
                "1":("Cancel appointment",cancel_appointment,empty_dict)},
          "had":
                {"title": "PAST APPOINTMENT",
                "type":"sub",
                "1":("Download prescription",download_prescription,empty_dict),
                "2":("Book new appointment",empty_method,flow_11)}}


# "Change GP pair" page dictionary
flow_2 = {"title": "CHANGE REGISTERED GP ?",
            "type":"sub",
            "1":("Yes - You will be assigned to another GP but you cannot choose it.",change_GP_pair, empty_dict)}


# patient main page dictionary
main_flow_patient = {"title": "PATIENT MAIN MENU",
                     "type":"main",
                     "1":("Book & Manage Appointments",manage_appointment,flow_1),
                     "2":("Change default GP",empty_method, flow_2)}
