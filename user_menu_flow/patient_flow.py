# patient_flow.py

# library imports 
from pathlib import Path
import sys

# Change python path for imports
package_dir = Path(__file__).parents[1]
sys.path.insert(0, str(package_dir))

# Importing utility methods from the 'system' package
from system import utils
from classes.appointment import Appointment

# import global variables from globals.py
from system import globals

# TODO: fill in the function corresponding to user choices (below)
############################### INPUT MENU PAGES ###########################

def manage_appointment(next_dict):
    '''
    This method works out whether the logged in patient has an upcoming appointment, 
    had an appointment or neither of those.
    '''

    # To start with, we assume the user has no appointments booked
    has_appointment = False
    had_appointment = False

    # Fetching data frames containing future and past appointments of patient 
    previous = Appointment.select_patient('previous', globals.usr_id)
    upcoming = Appointment.select_patient('upcoming', globals.usr_id)

    # Display summary of appointents if patient has book at least one appointment (future or past)
    if len(previous[0].index) > 0 or len(upcoming[0].index) > 0:

        print ('\n----------------------------------------------------\n'
              '              APPOINTMENT SUMMARY')

        # If at least one appointment has been booked in the past
        if len(previous[0].index) > 0:
            had_appointment = True
            print("\n-- Previous Appointments -- \n" + previous[1])
        
        # If at least one appointment has been booked in the future
        if len(upcoming[0].index) > 0:
            has_appointment = True
            print("\n-- Upcoming Appointments -- \n" + upcoming[1])

    # If patient has past appointments and upcoming appointemnts 
    if had_appointment and has_appointment:
        return utils.display(next_dict["both"])

    # If patient has upcoming appointemnts only
    elif has_appointment :
        return utils.display(next_dict["has"])

    # If patient has past appointemnts only
    elif had_appointment:
        return utils.display(next_dict["had"])

    # If patient has not booked appointments yet
    else:
        return utils.display(next_dict["neither"])


def cancel_appointment(next_dict):
    '''
    Method corresponding to user choice of cancelling upcoming appointment.
    '''

    print("\n----------------------------------------------------\n"
            "            CANCEL WHICH APPOINTMENT ? \n")

    # Print a reminder of upcoming appointments
    upcoming = Appointment.select_patient('upcoming', globals.usr_id)
    print(upcoming[1] + "\n")

    # Generate a list of the user choices 
    choices = ["#"]
    for j in range (1, len(upcoming[0].index) + 1):
        choices.append(str(j))

    # Display patient choices and require input on apppointment to cancel
    i = 0
    while i not in choices:
        
        for i in range(1,len(choices)):
            print("[ " + choices[i] + " ] Cancel row " + choices[i] + " of the table")
        
        print("\n[ # ] Do not cancel any appointment")

        i = input("\n--> ")

    # If do not want to cancel appointment, redirects to empty dictionary
    if i == "#" :
        return utils.display(next_dict)

    # If want to cancel appointment, work out apt ID, delete it and
    # redicrect to empty dictionary
    else:
        booking_id = upcoming[0].iloc[int(i)-1]['Apt. ID']
        Appointment.change_status(booking_id, "cancelled")
        print("\n\U00002705 Appointment successfully cancelled !")
        return utils.display(next_dict)
        

def access_prescription(next_dict):
    '''
    Method corresponding to user choice of accessing his prescription.
    from previous appointment.
    '''
    print("\n----------------------------------------------------\n"
            "       PRESCRIPTION FOR WHICH APPOINTMENT ? \n")

    # Print a reminder of upcoming appointments
    previous = Appointment.select_patient('previous', globals.usr_id)
    print(previous[1])

    # Generate a list of the user choices 
    choices = ["#"]
    for j in range (1, len(previous[0].index) + 1):
        choices.append(str(j))

    # Display patient choices and require input on apppointment to cancel
    i = 0
    while i not in choices:

        for i in range(1,len(choices)):
            print("[ " + choices[i] + " ] Access prescription for appointment in row " + choices[i] + " of the table")
        
        print("\n[ # ] Do not access any prescription")

        i = input("\n--> ")

    # If do not want to cancel appointment, redirects to empty dictionary
    if i == "#" :
        return utils.display(next_dict)

    # If want to cancel appointment, work out apt ID, delete it and
    # redicrect to empty dictionary
    else:
        booking_id = previous[0].iloc[i-1]['Apt. ID']
        
        # TODO: Retrieve prescription using apt_ID and display it

        return utils.display(next_dict)


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
    choice doesn't require any specific steps and just redirects.
    '''
    return utils.display(next_dict)

def change_GP_pair(next_dict):
    '''
    '''
    return utils.display(next_dict)

######################### MENU NAVIGATION DICTIONARIES ######################

# Empty nested dictionary to store in tuple for last menu
# before going back to main page (for display function return parameter).
empty_dict = {"title": "CONTINUE E-HEALTH OR LOGOUT ?",
              "type":"sub"}


# "Book new appointement" page dictionary
flow_1_new =  {"title": "BOOK WITH REGISTERED GP ?",
            "type":"sub",
            "1":("Yes",book_personal_gp,empty_dict),
            "2":("No, book with another GP",book_other_gp,empty_dict)}


# "Manage/Book appointment" page dictionary
flow_1 = {"neither":
                {"title": "BOOK NEW APPOINTMENT ?",
                "type":"sub",
                "1":("Yes",empty_method,flow_1_new)},
          "has":
                {"title": "MANAGE WHICH APPOINTMENTS ?",
                "type":"sub",
                "1":("Cancel upcoming appointments",cancel_appointment,empty_dict),
                "2":("Book new appointment",empty_method,flow_1_new)},
          "had":
                {"title": "MANAGE WHICH APPOINTMENTS ?",
                "type":"sub",
                "1":("Access previous appointement prescription",access_prescription,empty_dict),
                "2":("Book new appointment",empty_method,flow_1_new)},
          "both":
                {"title": "MANAGE WHICH APPOINTMENTS ?",
                "type":"sub",
                "1":("Access previous appointement prescription",access_prescription,empty_dict),
                "2":("Cancel upcoming appointments",cancel_appointment,empty_dict),
                "3":("Book new appointment",empty_method,flow_1_new)}}


# "Change GP pair" page dictionary
flow_2 = {"title": "CHANGE REGISTERED GP ?",
            "type":"sub",
            "1":("Yes - You will be assigned to another GP but you cannot choose it.",change_GP_pair, empty_dict)}


# patient main page dictionary
main_flow_patient = {"title": "PATIENT MAIN MENU",
                     "type":"main",
                     "1":("Book & Manage Appointments",manage_appointment,flow_1),
                     "2":("Change default GP",empty_method, flow_2)}
