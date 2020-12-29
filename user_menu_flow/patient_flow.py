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

    print("Enter ID of appointment to cancel \nor '#' to not cancel any of them")

    # Require user choice
    booking_id = input("\n--> ")
    
    # If user entry is invalid, ask for input again
    while booking_id not in str(upcoming[0]['Apt. ID'].tolist()) and booking_id != '#':
        print("\n\U00002757 Invalid entry, please try again")
        booking_id = input("\n--> ")

    # If do not want to cancel appointment, redirects to empty dictionary
    if booking_id == "#" :
        return utils.display(next_dict)

    # If want to cancel appointment, work out apt ID, delete it and
    # redicrect to empty dictionary
    else:
        Appointment.change_status(booking_id, "cancelled")
        print("\n\U00002705 Appointment successfully cancelled !")
        return utils.display(next_dict)


def book_appointment(next_dict):
    '''
    Mehtod for patients to book an appointment with his personal GP.
    '''

    print("\n----------------------------------------------------\n"
            "             BOOK WITH REGISTERED GP ? \n")

    # Display user availibility view options
    print("[ 1 ] Yes")
    print("[ 2 ] No, book with another GP")
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
    elif i == "1": personal_gp = True

    # Availability week view
    else: personal_gp = False

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
    elif i == "1": view = 'day'

    # Availability week view
    else: view = 'week'

    print("\n----------------------------------------------------\n"
            "              AVAILABILITY VIEW\n"
            "                 START DATE\n")

    print("Please enter the date (YYYY-MM-DD) from which\n" 
          "you want to diplay availibility\n\n"
          "Enter 'T' to see availibility from today")

    # Boolean for input validation
    valid = False

    # Require user choice
    start_date = input("\n--> ")

    # While invalid input, require input again
    while valid == False:
        
        if start_date in ("T","t"): 
            valid = True
            start_date = date.today().isoformat()
        
        elif utils.validate_date(start_date):
            if date.fromisoformat(start_date) > date.today():
                valid = True
            
            else:
                print("\n\U00002757 Appointment date must be in the future.")
        
        else:
            print("\n\U00002757 Invalid entry, please try again")

        if valid == False:
            start_date = input("\n--> ")

    # Calling the Appointment class static method select_availability or select_other_availability to display desired availibility
    if personal_gp == True: 
        availability = Appointment.select_availability(view, Patient.select_gp_details(globals.usr_id)[0], start_date)
        gp_id = Patient.select_gp_details(globals.usr_id)[0]
        gp_name = Patient.select_gp_details(globals.usr_id)[1]

    else: 
        availability = Appointment.select_other_availability(view, Patient.select_gp_details(globals.usr_id)[0], start_date)
        boolean_available = availability[4]

        # if no availability amongst other GPs
        if boolean_available == False:
            print("\nNo availability among other GPs for the dates selected, \nplease book with your personal GP or change dates.")
            return book_appointment(next_dict)

        # if availability, get displayed gp_ID and name
        else:
            gp_id = availability[2]
            gp_name = availability[3]


    print("\n" + availability[1])

    print("\nEnter the index of the time slot to book \nor '#' to display other availabilitites (different dates or GPs)")

    # Require user choice of booking slot
    booking_index = input("\n--> ")

    # Formatting user input correctly
    if booking_index != '#':
        while len(booking_index) < 3:
            booking_index = '0' + booking_index

    # Build dataframe with only the cell of timeslot selected by user
    # Will return an empty dataframe (nb rows = 0) for '#' and invalid entry
    selected_time_slot = availability[0].where(availability[0]=="["+booking_index+"]").dropna(how='all').dropna(axis=1)

    # user confirm time slot selection
    confirmation = False

    # while user hasn't confirmed his selection
    while confirmation == False:

        # While user entry is invalid
        while len(selected_time_slot.index) != 1 and booking_index != '#':
            print("\n\U00002757 Invalid entry, please try again")
            booking_index = input("\n--> ")

            # Formatting user input correctly
            if booking_index != '#':
                while len(booking_index) < 3:
                    booking_index = '0' + booking_index

            selected_time_slot = availability[0].where(availability[0]=="["+booking_index+"]").dropna(how='all').dropna(axis=1)

        # if user wants to display new availability, recursive call of the function itself
        if booking_index == "#":
             return book_appointment(next_dict)

        # Confirm time slot selection
        else :

            # work out booking date and time
            booking_date = list(selected_time_slot.columns)[0]
            booking_time = list(selected_time_slot.index)[0]

            # confirmation message
            print("\nBook a medical appointment at " + str(booking_time) + " on the " + str(booking_date) + " ?")
            print("\n[ 1 ] Yes")
            print("[ 2 ] No")

            # user confirmation choice 
            user_confirmation = input("\n--> ")

            # while invalid user input
            while user_confirmation not in ("1","2"):
                print("\n\U00002757 Invalid entry, please try again")
                user_confirmation = input("\n--> ")

            # If user confirms booking, exit loop
            if user_confirmation == '1': 
                confirmation = True

            # if user doesn't confirm --> initialised variables and loop again
            else: 
                confirmation = False

                # initialising variables
                print("\nEnter the index of the time slot to book \nor '#' to display other availabilitites (different dates or GPs)")
                booking_index = input("\n--> ")
                selected_time_slot = availability[0].where(availability[0]=="["+booking_index+"]").dropna(how='all').dropna(axis=1)
    

    # Now that user has confirmed appointment, require appointment type (online or offline)  
    print("\nDo you want to attend appointment in person or online ?")
    print("\n[ 1 ] Online")
    print("[ 2 ] In person")
    print("\n[ # ] Cancel appointment booking")

    # ask user choice
    i = input("\n--> ")
    
    # while invalid user input
    while i not in ("1","2","#"):
        print("\n\U00002757 Invalid entry, please try again")
        i = input("\n--> ")

    # cancel appointment booking
    if i == "#":
        return utils.display(next_dict)

    # online appointment
    elif i == "1":
        booking_type = "online"

    # offline appointment
    else:
        booking_type = "offline"
        

    # Require appointment agenda
    print("\nEnter short appointment agenda to inform GP of \nthe reason for the appointment.")
    booking_agenda = input("\n--> ")

    # While input is invalid, enter again
    while utils.validate(booking_agenda) == False:
        booking_agenda = input("\n--> ")
        
    # create appointement class instance to book appointment
    booking = Appointment(booking_start_time = str(booking_date) + " " + str(booking_time), booking_agenda = booking_agenda, booking_type = booking_type, patient_id = globals.usr_id, gp_id = gp_id)

    # Book appointment on Database
    success, reason = booking.book()

    if success:
        print("\n\U00002705 Appointment successfuly booked with " + gp_name + " at " + str(booking_time) + " on the " + str(booking_date) + ".")
        return utils.display(next_dict)

    else:
        print("\n\U00002757 " + reason)
        return book_appointment(next_dict)


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


# "Manage/Book appointment" page dictionary
flow_1 = {"neither":
                {"title": "BOOK NEW APPOINTMENT ?",
                "type":"sub",
                "1":("Yes",book_appointment,empty_dict)},
          "has":
                {"title": "MANAGE WHICH APPOINTMENTS ?",
                "type":"sub",
                "1":("Cancel upcoming appointments",cancel_appointment,empty_dict),
                "2":("Book new appointment",book_appointment,empty_dict)},
          "had":
                {"title": "MANAGE WHICH APPOINTMENTS ?",
                "type":"sub",
                "1":("Access previous prescriptions",access_prescription,empty_dict),
                "2":("Book new appointment",book_appointment,empty_dict)},
          "both":
                {"title": "MANAGE WHICH APPOINTMENTS ?",
                "type":"sub",
                "1":("Access previous prescriptions",access_prescription,empty_dict),
                "2":("Cancel upcoming appointments",cancel_appointment,empty_dict),
                "3":("Book new appointment",book_appointment,empty_dict)}}


# "Change GP pair" page dictionary
flow_2 = {"title": "CHANGE REGISTERED GP ?",
            "type":"sub",
            "1":("Yes - You will be assigned to another GP but you cannot choose it.",change_GP_pair, empty_dict)}


# patient main page dictionary
main_flow_patient = {"title": "PATIENT MAIN MENU",
                     "type":"main",
                     "1":("Book & Manage Appointments", manage_appointment,flow_1),
                     "2":("Display & Change default GP", display_default_GP, flow_2)}
