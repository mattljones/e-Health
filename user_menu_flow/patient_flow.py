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
            print("\n-- Past Appointments -- \n" + previous[1])
        
        # If at least one appointment has been booked in the future
        if len(upcoming[0].index) > 0:
            has_appointment = True
            print("\n-- Future Appointments -- \n" + upcoming[1])


        # If patient has past appointments and upcoming appointemnts 
        if had_appointment and has_appointment:

            i = ""
            while i not in ("1","2"):

                print("\n----------------------------------------------------\n"
                    "            MANAGE WHICH APPOINTMENTS ? \n")

                print('[ 1 ] Previous appointments')
                print('[ 2 ] Upcoming appointments')

                i = input("\n--> ")

                if i == "1":
                    return utils.display(next_dict["had"])
                
                elif i == "2":
                    return utils.display(next_dict["has"])

                else:
                    print("\n\U00002757 Invalid entry, please try again")

        # If patient has upcoming appointemnts only
        elif has_appointment :
            return utils.display(next_dict["has"])

        # If patient has past appointemnts only
        elif had_appointment:
            return utils.display(next_dict["had"])

    # If patient has not booked appointments yet
    else:
        return utils.display(next_dict["has_not"])


def cancel_appointment(next_dict):
    '''
    Method corresponding to user choice of cancelling upcoming appointment.
    '''

    print("\n----------------------------------------------------\n"
            "            CANCEL WHICH APPOINTMENT ? \n")

    # Print a reminder of upcoming appointments
    upcoming = Appointment.select_patient('upcoming', globals.usr_id)
    print(upcoming[1])

    print("\n[ 1 ] Cancel 1st row of the table"
          "\n[ 2 ] Cancel 2nd row of the table"
          "\n  ... "
          "\n[ # ] ")


    return utils.display(next_dict)

def download_prescription(next_dict):
    '''
    Method corresponding to user choice of downloading prescription.
    from previous appointment.
    '''
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
                {"title": "UPCOMING APPOINTMENTS",
                "type":"sub",
                "1":("Cancel upcoming appointment",cancel_appointment,empty_dict),
                "2":("Book new appointment",empty_method,flow_11)},
          "had":
                {"title": "PREVIOUS APPOINTMENTS",
                "type":"sub",
                "1":("Download past appointment prescription",download_prescription,empty_dict),
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
