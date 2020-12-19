# patient_flow.py

# library imports 
from pathlib import Path
from datetime import date
import sys

# Change python path for imports
package_dir = Path(__file__).parents[1]
sys.path.insert(0, str(package_dir))

# Importing utility methods from the 'system' package
from system import utils
from classes.appointment import Appointment
from classes.record import Record
from classes.patient import Patient

# import global variables from globals.py
from system import globals


############################### INPUT MENU PAGES ###########################

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
    for j in range(1,len(choices)):
        print("[ " + choices[j] + " ] Cancel row " + choices[j] + " of the table")
        
    print("\n[ # ] Do not cancel any appointment")

    i = input("\n--> ")

    # If user entry is invalid, ask for input again
    while i not in choices:
        print("\n\U00002757 Invalid entry, please try again")
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


def book_personal_gp(next_dict):
    '''
    Mehtod for patients to book an appointment with his personal GP.
    '''
    print("\n----------------------------------------------------\n"
            "              AVAILABILITY \n")

    # Display user availibility view options
    print("[ 1 ] Day view")
    print("[ 2 ] Week view")
    print("\n[ # ] Cancel appointment booking")

    # Require user choice
    i = input("\n--> ")

    # If invalid entry, ask for input again
    while i not in ("1","2","#"):
        print("\n\U00002757 Invalid entry, please try again")
        i = input("\n--> ")
    
    # If user want to stop apppointment booking process
    if i == "#": return utils.display(next_dict)

    # Availability day view
    elif i == "1": day_view = True

    # Availability week view
    else: day_view = False

    print("\n----------------------------------------------------\n"
            "              AVAILABILITY VIEW\n"
            "                 START DATE\n")

    print("Please enter the date (YYYY-MM-DD) from which\n" 
          "you want to diplay availibility\n\n"
          "Enter 'T' to see availibility from today")

    # Boolean for input validation
    valid = False

    # Require user choice
    i = input("\n--> ")

    # While invalid input, require input again
    while valid == False:
        
        if i in ("T","t"): valid = True
        
        elif utils.validate_date(i):
            if date.fromisoformat(i) > date.today():
                valid = True
            
            else:
                print("\n\U00002757 Appointment date must be in the future.")
        
        else:
            print("\n\U00002757 Invalid entry, please try again")

            
        if valid == False:
            i = input("\n--> ")

    # Calling the Appointment class static method select_availability to display availibility
    if day_view == True and i in ("T","t"):
        availibility = Appointment.select_availability('day', Patient.select_gp_details(globals.usr_id)[0], date.today().isoformat())
    elif day_view == True and i not in ("T","t"):
        availibility = Appointment.select_availability('day', Patient.select_gp_details(globals.usr_id)[0], i)
    elif day_view == False and i in ("T","t"):
        availibility = Appointment.select_availability('week', Patient.select_gp_details(globals.usr_id)[0], date.today().isoformat())
    else:
        availibility = Appointment.select_availability('week', Patient.select_gp_details(globals.usr_id)[0], i)

    print("\n" + availibility[1])

    # TODO: ask user input for which appointment to book & book appointment 

    return utils.display(next_dict)
        

def book_other_gp(next_dict):
    '''
    Mehtod for patients to book an appointment with 
    other GPs than hiw personal GP.
    '''
    print("\n----------------------------------------------------\n"
            "              AVAILABILITY \n")

    # Display user availibility view options
    print("[ 1 ] Day view")
    print("[ 2 ] Week view")
    print("\n[ # ] Cancel appointment booking")

    # Require user choice
    i = input("\n--> ")

    # If invalid entry, ask for input again
    while i not in ("1","2","#"):
        print("\n\U00002757 Invalid entry, please try again")
        i = input("\n--> ")
    
    # If user want to stop apppointment booking process
    if i == "#": return utils.display(next_dict)

    # Availability day view
    elif i == "1": day_view = True

    # Availability week view
    else: day_view = False

    print("\n----------------------------------------------------\n"
            "              AVAILABILITY VIEW\n"
            "                 START DATE\n")

    print("Please enter the date (YYYY-MM-DD) from\n" 
          "which you want to diplay availibility:\n\n"
          "Enter 'T' to see availibility from today.")

    # Boolean for input validation
    valid = False

    # Require user choice
    i = input("\n--> ")

    # While invalid input, require input again
    while valid == False:
        
        if i in ("T","t"): valid = True
        
        elif utils.validate_date(i):
            if date.fromisoformat(i) > date.today():
                valid = True
            
            else:
                print("\n\U00002757 Appointment date must be in the future.")
        
        else:
            print("\n\U00002757 Invalid entry, please try again")

            
        if valid == False:
            i = input("\n--> ")

    # Calling the Appointment class static method select_other_availability to display availibility
    if day_view == True and i in ("T","t"):
        availibility = Appointment.select_other_availability('day', Patient.select_gp_details(globals.usr_id)[0], date.today().isoformat())
    elif day_view == True and i not in ("T","t"):
        availibility = Appointment.select_other_availability('day', Patient.select_gp_details(globals.usr_id)[0], i)
    elif day_view == False and i in ("T","t"):
        availibility = Appointment.select_other_availability('week', Patient.select_gp_details(globals.usr_id)[0], date.today().isoformat())
    else:
        availibility = Appointment.select_other_availability('week', Patient.select_gp_details(globals.usr_id)[0], i)

    print("\n" + availibility[1])

    # TODO: ask user input for which appointment to book & book appointment 

    return utils.display(next_dict)


############################ SEQUENTIAL STEPS MENUS ########################

def empty_method(next_dict):
    '''
    Empty method to be stored in the tuple of the dictionary of the user 
    choice doesn't require any specific steps and just redirects.
    '''
    return utils.display(next_dict)


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


def access_prescription(next_dict):
    '''
    Method corresponding to user choice of accessing his prescription.
    from previous appointment.
    '''
    print("\n----------------------------------------------------\n"
            "       PAST APPOINTMENTS & PRESCIPTIONS \n")

    # Print table of past appointments and their prescription
    records = Record.select(globals.usr_id)
    print(records[4])
    
    return utils.display(next_dict)


def display_default_GP(next_dict):
    '''
    Displaying default GP name before asking user whether he wants to 
    change default GP or not
    '''
    print("\n----------------------------------------------------\n"
            "                REGISTERED GP \n")

    print("Your are registered with " + Patient.select_gp_details(globals.usr_id)[1] + ".\n")
    return utils.display(next_dict)


def change_GP_pair(next_dict):
    '''
    Change patient's assigned GP and register patient with most available GP.
    '''

    # Change default GP and get new GP name
    success, new_GP_name = Patient.change_gp('auto',globals.usr_id)

    # if successful change
    if success:
        print("\n\U00002705 Default GP successfully changed !"
              "\nYou are now registered with " + new_GP_name + ".\n")

    # if unsuccessful change
    else:
        print("\n\U00002757 Unknown error encountered while changing registered GP."
              "\nPlease try again later.")

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
                "1":("Access previous prescriptions",access_prescription,empty_dict),
                "2":("Book new appointment",empty_method,flow_1_new)},
          "both":
                {"title": "MANAGE WHICH APPOINTMENTS ?",
                "type":"sub",
                "1":("Access previous prescriptions",access_prescription,empty_dict),
                "2":("Cancel upcoming appointments",cancel_appointment,empty_dict),
                "3":("Book new appointment",empty_method,flow_1_new)}}


# "Change GP pair" page dictionary
flow_2 = {"title": "CHANGE REGISTERED GP ?",
            "type":"sub",
            "1":("Yes - You will be assigned to another GP but you cannot choose it.",change_GP_pair, empty_dict)}


# patient main page dictionary
main_flow_patient = {"title": "PATIENT MAIN MENU",
                     "type":"main",
                     "1":("Book & Manage Appointments", manage_appointment,flow_1),
                     "2":("Display & Change default GP", display_default_GP, flow_2)}
