# admin_flow.py

# library imports 
from datetime import datetime, timedelta
from pathlib import Path
import sys 

# Change python path for imports
p = Path(__file__).parents[1]
sys.path.insert(1, str(p))

# Importing utility methods from the 'system' package
from system import utils

# Importing class methods
from classes.gp import GP
from classes.record import Record
from classes.patient import Patient
from classes.schedule import Schedule
from classes.appointment import Appointment

############################### INPUT MENU PAGES ###########################

###### MANAGE GP ACCOUNTS FUNCTIONS ######

def gp_account_section_menu(next_dict):
    '''
    Returns to the section menu.
    '''
    return utils.display(manage_gp_accounts_flow)


def view_gp(next_dict):
    '''
    Select from a list of GPs and allows choice for viewing.
    '''

    # Check if gp id already selected previously for reuse
    if 'gp_id_choice' in globals():
        choice = gp_id_choice
    else:
        choice = retrieve_gp_list('all')

    doctor_df = GP.select(choice)

    print("\n----------------------------------------------------\n"
          "                ",'GP DETAILS', "\n")
    print(doctor_df[2])
    index_choice = int(input("Choose a value to edit. \n"
    "--> "))
    value_choice = input("\nChoose a new value to input. \n"
    "--> ") 

    print("\n----------------------------------------------------\n"
          "                ",'CONFIRM?', "\n")
    print("[ 1 ] Yes")
    print("[ 2 ] No")
    y_n = int(input("\n--> "))
    if y_n == 1:
        # TODO: UPDATE THE DATABASE WITH THE ENTERED VALUES

        return utils.display(next_dict)
        
    elif y_n == 2:
        return utils.display(next_dict)
    else:
        print("\n\U00002757 Input not valid.")
        return utils.display(next_dict)


def retrieve_gp_list(type):
    '''
    Shows the list of GPs and allows choice from that list.
    '''
    df = GP.select_list(type)
    df_show = df[1]
    print("\n----------------------------------------------------\n"
          "                ",'GP LIST', "\n")
    print(df_show)
    global gp_id_choice
    gp_id_choice = int(input("\nPlease select a GP ID. \n--> "))
    return gp_id_choice


def same_gp(next_dict):
    # NOTE: This functions serves no purpose. 
    '''
    Allows viewing/editing of the same GP.
    '''
    return utils.display(next_dict)


def view_another_gp(next_dict):
    '''
    Allows cycling back to the view_gp function from final_menu.
    '''
    return view_gp(view_edit_gp_accounts_final_menu)


def add_gp(next_dict):
    '''
    Adds a new GP.
    '''
    print("\n----------------------------------------------------\n"
          "                ",'ENTER GP DETAILS', "\n")

    # TODO: Input validation (see patient registration in register_login_flow)
    first_name = input('Please enter First Name: \n'
    '--> ')
    last_name = input('\nPlease enter Last Name: \n'
    '--> ')
    gender = input('\nPlease enter Gender: \n'
    '--> ')
    birth_date = input('\nPlease enter Birth Date: \n'
    '--> ')
    email = input('\nPlease enter Email: \n'
    '--> ')
    password_raw = input('\nPlease enter Password: \n'
    '--> ')
    working_days = input('\nPlease enter Working Days: \n'
    '--> ')

    # TODO: LIST OUT DEPARTMENTS AND SPECIALISATIONS AND GIVE CHOICE.

    # Default department and specialiations: 1
    department_id = 1
    specialisation_id = 1

    # Default status: active 
    status = 'active'

    new_gp = GP(id_ = None,
                first_name=first_name, 
                last_name=last_name, 
                gender=gender, 
                birth_date=birth_date, 
                email=email, 
                password_raw=password_raw, 
                working_days=working_days, 
                department_id=department_id, 
                specialisation_id=specialisation_id, 
                status=status)

    print("\n----------------------------------------------------\n"
          "                ",'CONFIRM?', "\n")
    print("[ 1 ] Yes")
    print("[ 2 ] No")

    y_n = int(input("\n--> "))
    
    if y_n == 1:
        # Insert new GP in db
        GP.insert(new_gp)
        print("\n\U00002705 Dr. {} has been registered.".format(last_name))
        return utils.display(next_dict)
        
    elif y_n == 2:
        print("\n\U00002757 GP not added.")
        return utils.display(next_dict)

    else:
        print("\n\U00002757 Input not valid.")
        return utils.display(next_dict)


def add_another_gp(next_dict):
    '''
    Allows cycling back to add_gp from final_menu.
    '''
    return add_gp(add_new_gp_account_final_menu)


def deactivate_gp(next_dict):
    '''
    Deactivates a GP.
    '''
    # List and prompt admin for a gp id
    gp_id = retrieve_gp_list('active')

    print("\n----------------------------------------------------\n"
          "                ",'CONFIRM?', "\n")
    print("Do you want to deactive GP with ID: {}?\n".format(gp_id))
    print("[ 1 ] Yes")
    print("[ 2 ] No")

    y_n = int(input("\n--> "))

    if y_n == 1:
        GP.change_status(gp_id, 'inactive')
        print("\n\U00002705 GP with ID [{}] has been deactivated.".format(gp_id))
        return utils.display(next_dict)

    elif y_n == 2:
        print("\n\U00002757 Deactivation cancelled.")
        return utils.display(next_dict)

    else:
        print(("\n\U00002757 Input not valid."))
        return utils.display(next_dict)



def deactivate_another_gp(next_dict):
    '''
    Allows cycling back to add_gp from final_menu.
    '''
    return deactivate_gp(deactivate_gp_account_final_menu)



def delete_gp(next_dict):
    '''
    # NOTE: Integrate docstrings with info from GP.delete()
    Deletes a GP.
    '''
    # List and prompt admin for a gp id
    gp_id = retrieve_gp_list('all')

    print("\n----------------------------------------------------\n"
          "                ",'CONFIRM?', "\n")
    print("Do you want to delete GP with ID: {}?\n".format(gp_id))
    print("[ 1 ] Yes")
    print("[ 2 ] No")

    y_n = int(input("\n--> "))

    while y_n not in (1, 2):
        print(("\n\U00002757 Input not valid."))
        y_n = int(input("\n--> "))

    if y_n == 1:
        # Patients and appointments reallocated
        if GP.delete(gp_id)[0]: 
            print("""\n\U00002705 GP with ID {} has been deleted.
\U00002705 Patients reallocated successfully.
\U00002705 Appointments reallocated successfully.""".format(gp_id))

        # Patients reallocated | Appointment *not* reallocated
        elif GP.delete(gp_id)[1] == 'apps':
            print("""\n\U00002705 GP with ID {} has been deleted. 
\U00002705 Patients reallocated successfully.
\U00002757 Appointments *NOT* reallocated due to conflict in the following appointments: {}"""
                    .format(gp_id, GP.delete(gp_id)[4]))

        # Appointments reallocated | Patients *not* reallocated
        elif GP.delete(gp_id)[1] == 'patients':
            print("""\n\U00002705 GP with ID {} has been deleted. 
\U00002705 Appointments reallocated successfully.
\U00002757 Patients *NOT* reallocated due to {} patients exceeding total hospital capacity."""
                    .format(gp_id, GP.delete(gp_id)[2]))

        # Patients and appointment *not* reallocated
        elif GP.delete(gp_id)[1] == 'both':
            print("""\n\U00002705 GP with ID {} has been deleted. 
\U00002757 Patients *NOT* reallocated due to {} patients exceeding total hospital capacity.
\U00002757 Appointments *NOT* reallocated due to conflict in the following appointments: {}"""
                    .format(gp_id, GP.delete(gp_id)[2], GP.delete(gp_id)[4]))

        return utils.display(next_dict)

    elif y_n == 2:
        print("\n\U00002757 Action cancelled.")
        return utils.display(next_dict)


def delete_another_gp(next_dict):
    '''
    Allows cycling back to delete_gp from final_menu.
    '''
    return delete_gp(delete_gp_account_final_menu)


###### MANAGE PATIENT ACCOUNTS FUNCTIONS ######


def patient_account_section_menu(next_dict):
    '''
    Returns to the section menu.
    '''
    return utils.display(manage_patient_accounts_flow)


def choose_patient(type, patient_last_name=None):
    '''
    Choose patient account.
    '''
    df = Patient.select_list(type,patient_last_name)
    print("\n----------------------------------------------------\n"
          "                ",'SELECT PATIENT', "\n")
    print(df[1])
    

def same_patient(next_dict):
    '''
    Allows editing of the same patient from the final_menu.
    '''
    #TODO: FIGURE OUT HOW TO DO THIS.
    #NOTE: SIMILAR TO same_gp FUNCTION.
    return utils.display(view_edit_patient_accounts_final_menu)


# NOTE: Rename this edit_patient?
def view_patient(next_dict):
    '''
    View a Patient Account.
    '''
    print("\n----------------------------------------------------\n"
          "                ",'ENTER LAST NAME', "\n")
    last_name = input("Please enter the patient's last name:\n"
    "--> ")
    choose_patient('matching', patient_last_name=last_name)
    choice = int(input('\nPlease choose a patient ID\n'
    '--> '))
    selected_patient = Patient.select(choice)
    print("\n----------------------------------------------------\n"
          "                ",'PATIENT DETAILS', "\n")
    print(selected_patient[2])
    index_choice = int(input("Choose an value to edit. \n"
    "--> "))
    value_choice = input("\nChoose a new value to input. \n"
    "--> ") 

    print("\n----------------------------------------------------\n"
          "                ",'CONFIRM?', "\n")
    print("[ 1 ] Yes")
    print("[ 2 ] No")
    y_n = int(input("\n--> "))
    if y_n == 1:

        # TODO: UPDATE THE DATABASE WITH THE ENTERED VALUES

        return utils.display(next_dict)
        
    elif y_n == 2:
        return utils.display(next_dict)


def view_another_patient(next_dict):
    '''
    Allows cycling back to the view_patient function from the final_menu.
    '''
    return view_patient(view_edit_patient_accounts_final_menu)


def confirm_patient(next_dict):
    '''
    Confirm pending patient registrations.
    '''
    choose_patient('pending')
    print("\n----------------------------------------------------\n"
          "                ",'CONFIRM ALL NEW PATIENTS?', "\n")
    print("[ 1 ] Yes")
    print("[ 2 ] Enter Individual ID(s)")
    choice = int(input('Please enter your choice:\n'
    '--> '))
    
    if choice == 1:

        print("\n----------------------------------------------------\n"
          "                ",'CONFIRM?', "\n")
        print("[ 1 ] Yes")
        print("[ 2 ] No")
        y_n = int(input("\n--> "))

        if y_n == 1:
            Patient.confirm('all')
            return utils.display(next_dict)
        
        elif y_n == 2:
            return utils.display(next_dict)
        
    elif choice == 2:

        print("\n----------------------------------------------------\n"
        "                ",'ENTER PATIENT ID(S) TO CONFIRM', "\n")
        ids = input('Please enter ID(s) here, comma-separated.\n'
        '--> ').split()

        print("\n----------------------------------------------------\n"
        "                ",'CONFIRM?', "\n")
        print("[ 1 ] Yes")
        print("[ 2 ] No")
        y_n = int(input("\n--> "))

        if y_n == 1:
            for id in ids:
                Patient.confirm('single', patient_id = int(id))

            return utils.display(next_dict)
        
        elif y_n == 2:
            return utils.display(next_dict)


def confirm_another_patient(next_dict):
    '''
    Allows cycling back to the confirm_patient function from the final_menu.
    '''
    return confirm_patient(add_new_patient_account_final_menu)


def delete_patient(next_dict):
    '''
    Delete a patient account
    '''
    print("\n----------------------------------------------------\n"
          "                ",'ENTER LAST NAME', "\n")

    last_name = input("Please enter the patient's last name:\n"
    "--> ")

    choose_patient('matching', patient_last_name=last_name)
    choice = input('''
Please input a patient ID or a list of IDs separated by commas (e.g. 42,66,82)\n'''
    '--> ')
    # Eliminating whitespace from string and splitting it into single IDs
    patient_ids = choice.replace(' ', '').split(',')


    print("\n----------------------------------------------------\n"
    "                ",'CONFIRM?', "\n")
    print("[ 1 ] Yes")
    print("[ 2 ] No")
    y_n = int(input("\n--> "))
    if y_n == 1:
        for id in patient_ids:
            Patient.delete(id)
            print("\n\U00002705 Patient with ID {} has been deleted.".format(id))
        return utils.display(next_dict)
        
    elif y_n == 2:
        print("\n\U00002757 Action cancelled.")
        return utils.display(next_dict)

    else:
        print("\n\U00002757 Input not valid.")
        return utils.display(next_dict)


def delete_another_patient(next_dict):
    '''
    Allows cycling back to the delete_patient function from the final_menu.
    '''
    return delete_patient(delete_patient_account_final_menu)


###### MANAGE GP-PATIENT PAIRINGS FUNCTIONS ######


def pairings_section_menu(next_dict):
    '''
    Returns to the section menu.
    '''
    return utils.display(gp_patient_pair_flow)


def pairing_patient(next_dict):
    '''
    Search for a patient and pair them up with a GP.
    '''

    # NOTE: Better way to reuse code from view_patient()

    print("\n----------------------------------------------------\n"
          "                ",'ENTER LAST NAME', "\n")
    last_name = input("Please enter the patient's last name:\n"
    "--> ")
    choose_patient('matching', patient_last_name=last_name)
    patient_id = int(input('\nPlease choose a patient ID\n'
    '--> '))
    selected_patient = Patient.select(patient_id)
    gp_id = selected_patient[0].gp_id
    gp_lastname = GP.select(gp_id)[0].last_name

    print('Patient {} is currently registered with Dr {}.'.format(patient_id, gp_lastname))
    print("\n----------------------------------------------------\n"
          "                ",'CHANGE DEFAULT GP', "\n")
    print('[ 1 ] Auto-Reallocate')
    print('[ 2 ] Select GP From List')
    choice = int(input('\n--> '))

    if choice == 1:
        new_gp = Patient.change_gp('auto', patient_id)

        if new_gp[0]:
            print("\n----------------------------------------------------\n"
            "                ",'CONFIRM?', "\n")
            print("[ 1 ] Yes")
            print("[ 2 ] No")
            y_n = int(input("\n--> "))

            if y_n == 1:
                print("\n\U00002705 Patient with ID {} has been allocated to Dr {}.".format(patient_id, new_gp[1]))
                return utils.display(next_dict)

            elif y_n == 2:
                print("\n\U00002757 Action cancelled.")
                return utils.display(next_dict)

            else:
                print("\n\U00002757 Input not valid.")
                return utils.display(next_dict)
        
        else:
            print("\n\U00002757 All GPs are full.")
            return utils.display(next_dict)


    elif choice == 2:
        gp_list = GP.select_list('not_full')
        print("\n----------------------------------------------------\n"
            "                ",'NON-FULL GP LIST', "\n")
        print(gp_list[1])
        new_gp_id = int(input('\nPlease choose a GP to allocate the patient to.\n'
        '--> '))
        new_gp = Patient.change_gp('specific', patient_id, new_gp_id=new_gp_id)

        if new_gp[0]:
            print("\n----------------------------------------------------\n"
            "                ",'CONFIRM?', "\n")
            print("[ 1 ] Yes")
            print("[ 2 ] No")
            y_n = int(input("\n--> "))

            if y_n == 1:
                print("\n\U00002705 Patient with ID {} has been allocated to Dr {}.".format(patient_id, new_gp[1]))
                return utils.display(next_dict)

            elif y_n == 2:
                print("\n\U00002757 Action cancelled.")
                return utils.display(next_dict)

            else:
                print("\n\U00002757 Input not valid.")
                return utils.display(next_dict)
        else:
            print("\n\U00002757 All GPs are full.")
            return utils.display(next_dict)
        
    
    else:
        print("\n\U00002757 Input not valid.")
        return utils.display(next_dict)
    

def pairing_gp(next_dict):
    '''
    Select a GP and pair patients to them if they are not full.
    '''
    gp_list = GP.select_list('not_full')
    print("\n----------------------------------------------------\n"
    "                ",'NON-FULL GP LIST', "\n")
    print(gp_list[1])
    new_gp_id = int(input('\nPlease choose a GP to allocate patients to.\n'
    '--> '))


    print("\n----------------------------------------------------\n"
    "                ",'ADD PATIENTS', "\n")
    print('[ 1 ] By IDs')
    print('[ 2 ] Search by last name')
    choice = int(input('\n--> '))

    if choice == 1:
        print("\n----------------------------------------------------\n"
        "                ",'ENTER IDS', "\n")
        id_choice = input('''
Please input a patient ID or a list of IDs separated by commas (e.g. 42,66,82)\n'''
        '--> ')
        patient_ids = id_choice.replace(' ', '').split(',')

        print("\n----------------------------------------------------\n"
        "                ",'CONFIRM?', "\n")
        print("[ 1 ] Yes")
        print("[ 2 ] No")
        y_n = int(input("\n--> "))

        if y_n == 1:

            for id in patient_ids:
                new_gp = Patient.change_gp('specific', id, new_gp_id=new_gp_id)

                if new_gp[0]:
                    print("\n\U00002705 Patient with ID {} has allocated to Dr {}.".format(id, new_gp[1]))
                    return utils.display(next_dict)

                else:
                    print("\n\U00002757 This GP is full.")
                    return utils.display(next_dict)
        
        elif y_n == 2:
            print("\n\U00002757 Action cancelled.")
            return utils.display(next_dict)

        else:
            print("\n\U00002757 Input not valid.")
            return utils.display(next_dict)
    
    elif choice == 2:

        print("\n----------------------------------------------------\n"
          "                ",'ENTER LAST NAME', "\n")
        last_name = input("Please enter the patient's last name:\n"
        "--> ")
        choose_patient('matching', patient_last_name=last_name)
        patient_id = int(input('\nPlease choose a patient ID\n'
        '--> '))
        selected_patient = Patient.select(patient_id)

        print("\n----------------------------------------------------\n"
        "                ",'CONFIRM?', "\n")
        print("[ 1 ] Yes")
        print("[ 2 ] No")
        y_n = int(input("\n--> "))

        if y_n == 1:
            new_gp = Patient.change_gp('specific', patient_id, new_gp_id=new_gp_id)

            if new_gp[0]:
                print("\n\U00002705 Patient with ID {} has been allocated to Dr {}.".format(patient_id, new_gp[1]))
                return utils.display(next_dict)

            else:
                print("\n\U00002757 This GP is full.")
                return utils.display(next_dict)
        
        elif y_n == 2:
            print("\n\U00002757 Action cancelled.")
            return utils.display(next_dict)

        else:
            print("\n\U00002757 Input not valid.")
            return utils.display(next_dict)

    else:
        print("\n\U00002757 Input not valid.")
        return utils.display(next_dict)


###### MANAGE GP SCHEDULES FUNCTIONS ######


def choose_gp(next_dict):
    # NOTE: This seems to be doing the same thing as retrieve_gp_list()
    # Using similar code for now, substitute function name in dict later if needed
    '''
    Returns the numbered list of GPs to choose from
    '''
    df = GP.select_list('all')
    df_show = df[1]
    print("\n----------------------------------------------------\n"
          "                ",'GP LIST', "\n")
    print(df_show)
    global gp_id_choice
    gp_id_choice = int(input("\nPlease select a GP ID. \n--> "))
    
    return utils.display(next_dict)


def schedules_section_menu(next_dict):
    '''
    Returns to the section menu.
    '''
    return utils.display(view_schedule_flow)


def view_schedule_day(next_dict):
    '''
    View a GP's current schedule for a day.
    '''    
    start_date = utils.get_start_date()
    sched = Schedule.select(gp_id_choice, 'day', start_date)
    print("\n----------------------------------------------------\n"
          "                ",'DAILY SCHEDULE', "\n")
    print(sched[1])
    return utils.display(next_dict)


def view_schedule_week(next_dict):
    '''
    View a GP's current schedule for a week.
    '''    
    start_date = utils.get_start_date()
    sched = Schedule.select(gp_id_choice, 'week', start_date)
    print("\n----------------------------------------------------\n"
          "                ",'WEEKLY SCHEDULE', "\n")
    print(sched[1])
    return utils.display(next_dict)



def view_another_schedule(next_dict):
    '''
    Allows cycling back to the schedule_length_flow from the final_menu.
    '''
    return utils.display(schedule_length_flow)



def choose_another_gp(next_dict):
    '''
    Allows choice to change the GP viewed from the final_menu.
    '''
    return choose_gp(view_schedule_flow)



def appointments_shortcut(next_dict):
    '''
    Allows the viewing of appointments (in sub-menu 5) from the manage_availability_flow
    (in sub-menu 4). 
    '''
    return utils.display(delete_gp_appointment_flow)



def view_time_off(next_dict):
    '''
    View a GP's current time off.
    '''
    print("\n----------------------------------------------------\n"
          "                ",'TIME OFF', "\n")

    off = Schedule.select_upcoming_timeoff(gp_id_choice)
    print(off[1])

    return utils.display(next_dict)



def manage_more_availability(next_dict):
    '''
    Allows cycling back to the manage_availability_flow menu from the final_menu.
    '''
    return utils.display(manage_availability_flow)



def manage_more_time_off(next_dict):
    '''
    Allows cycling back to the manage_time_off_flow menu from the final_menu.
    '''
    return utils.display(manage_time_off_flow)



def add_time_off(next_dict):
    '''
    Returns menu to add time off to a GP's schedule.
    '''
    return utils.display(add_time_off_flow)


def add_time_off_day(next_dict):
    '''
    Adds a day of time off to a GP's schedule.
    '''
    # NOTE: Minimize code repetition
    print("\n----------------------------------------------------\n"
          "                ",'ADD TIME OFF - DAY', "\n")

    # Prompt user for type of time off
    print("Please select the time off type: ")
    print("\n [ 1 ] Sick leave \n [ 2 ] General time off")
    timeoff_type_input = input('\n--> ')

    while timeoff_type_input not in ('1', '2'):
        print("\n\U00002757 Invalid entry, please try again")
        timeoff_type_input = input('\n--> ')
        
    if timeoff_type_input == '1':
        timeoff_type = 'sick leave'
    elif timeoff_type_input == '2':
        timeoff_type = 'time off'

    # Prompt user for start date only
    start_date = utils.get_start_date()

    # Add one day to start date
    s = datetime.strptime(start_date, "%Y-%m-%d")
    e = s + timedelta(days=1) 
    end_date = datetime.strftime(e, "%Y-%m-%d")  

    # Confirmation step
    print("\n----------------------------------------------------\n"
          "                ",'CONFIRM?', "\n")

    print('\nDo you want to add one day of {} on {}?\n'.format(timeoff_type, start_date))
    print("[ 1 ] Yes")
    print("[ 2 ] No")

    user_confirmation = input("\n--> ")

    while user_confirmation not in ('1','2'):
            print("\n\U00002757 Invalid entry, please try again")
            user_confirmation = input("\n--> ")

    if user_confirmation == '1':
        # Add timeoff to db
        Schedule.insert_timeoff(gp_id_choice, timeoff_type, start_date, end_date)
        print("\n\U00002705 Time off successfully added.")
        return utils.display(next_dict)
        
    else:
        # Return to main add time off menu
        return utils.display(add_time_off_flow)


def add_time_off_week(next_dict):
    '''
    Adds a week of time off to a GP's schedule.
    '''
    # NOTE: Minimize code repetition
    print("\n----------------------------------------------------\n"
          "                ",'ADD TIME OFF - WEEK', "\n")

    # Prompt user for type of time off
    print("Please select the time off type: ")
    print("\n [ 1 ] Sick leave \n [ 2 ] General time off")
    timeoff_type_input = input('\n--> ')

    while timeoff_type_input not in ('1', '2'):
        print("\n\U00002757 Invalid entry, please try again")
        timeoff_type_input = input('\n--> ')
        
    if timeoff_type_input == '1':
        timeoff_type = 'sick leave'
    elif timeoff_type_input == '2':
        timeoff_type = 'time off'

    # Prompt user for start date only
    start_date = utils.get_start_date()

    # Add one day to start date
    s = datetime.strptime(start_date, "%Y-%m-%d")
    e = s + timedelta(weeks=1) 
    end_date = datetime.strftime(e, "%Y-%m-%d")  

    # Confirmation step
    print("\n----------------------------------------------------\n"
          "                ",'CONFIRM?', "\n")

    print('\nDo you want to add one week of {} starting from {}?\n'.format(timeoff_type, start_date))
    print("[ 1 ] Yes")
    print("[ 2 ] No")

    user_confirmation = input("\n--> ")

    while user_confirmation not in ('1','2'):
            print("\n\U00002757 Invalid entry, please try again")
            user_confirmation = input("\n--> ")

    if user_confirmation == '1':
        # Add timeoff to db
        Schedule.insert_timeoff(gp_id_choice, timeoff_type, start_date, end_date)
        print("\n\U00002705 Time off successfully added.")
        return utils.display(next_dict)
        
    else:
        # Return to main add time off menu
        return add_time_off(next_dict)


def add_time_off_custom(next_dict):
    '''
    Adds a custom amount of time off to a GP's schedule.
    '''
    print("\n----------------------------------------------------\n"
          "                ",'ADD TIME OFF - CUSTOM', "\n")

    # Prompt user for type of time off
    print("Please select the time off type: ")
    print("\n [ 1 ] Sick leave \n [ 2 ] General time off")
    timeoff_type_input = input('\n--> ')

    while timeoff_type_input not in ('1', '2'):
        print("\n\U00002757 Invalid entry, please try again")
        timeoff_type_input = input('\n--> ')
        
    if timeoff_type_input == '1':
        timeoff_type = 'sick leave'
    elif timeoff_type_input == '2':
        timeoff_type = 'time off'

    # Prompt user for time off range
    start_date = utils.get_start_date()
    end_date = utils.get_end_date()

    # Confirmation step
    print("\n----------------------------------------------------\n"
          "                ",'CONFIRM?', "\n")

    print('\nDo you want to add {} from {} to {}?\n'.format(timeoff_type, start_date, end_date))
    print("[ 1 ] Yes")
    print("[ 2 ] No")

    user_confirmation = input("\n--> ")

    while user_confirmation not in ('1','2'):
            print("\n\U00002757 Invalid entry, please try again")
            user_confirmation = input("\n--> ")

    if user_confirmation == '1':
        # Add timeoff to db
        Schedule.insert_timeoff(gp_id_choice, timeoff_type, start_date, end_date)
        print("\n\U00002705 Time off successfully added.")
        return utils.display(next_dict)

    else:
        # Return to main add time off menu
        return add_time_off(next_dict)



def remove_time_off(next_dict):
    '''
    Returns menu to remove a custom amount of time off to a GP's schedule.
    '''
    return utils.display(remove_time_off_flow)



def remove_time_off_custom(next_dict):
    '''
    Remove a custom amount of time off to a GP's schedule.
    '''
    print("\n----------------------------------------------------\n"
          "                ",'REMOVE TIME OFF - CUSTOM', "\n")

    # Prompt user for type of time off
    print("Please select the time off type: ")
    print("\n [ 1 ] Sick leave \n [ 2 ] General time off \n [ 3 ] Both")
    timeoff_type_input = input('\n--> ')

    while timeoff_type_input not in ('1', '2', '3'):
        print("\n\U00002757 Invalid entry, please try again")
        timeoff_type_input = input('\n--> ')
        
    if timeoff_type_input == '1':
        timeoff_type = 'sick leave'
    elif timeoff_type_input == '2':
        timeoff_type = 'time off'
    elif timeoff_type_input == '3':
        timeoff_type = 'all time off'

    # Prompt user for time off range
    start_date = utils.get_start_date()
    end_date = utils.get_end_date()

    # Confirmation step
    print("\n----------------------------------------------------\n"
          "                ",'CONFIRM?', "\n")

    print('\nDo you want to remove {} from {} to {}?\n'.format(timeoff_type, start_date, end_date))
    print("[ 1 ] Yes")
    print("[ 2 ] No")

    user_confirmation = input("\n--> ")

    while user_confirmation not in ('1','2'):
            print("\n\U00002757 Invalid entry, please try again")
            user_confirmation = input("\n--> ")

    if user_confirmation == '1':
        # Remove timeoff of a specific type from db
        if timeoff_type_input in ('1', '2'):
            Schedule.delete_timeoff(gp_id_choice, 'custom', timeoff_type, start_date, end_date)
            print("\n\U00002705 Time off successfully removed.")

        # Remove timeoff of both types from db
        elif timeoff_type_input == '3':
            Schedule.delete_timeoff(gp_id_choice, 'custom', 'sick leave', start_date, end_date)
            Schedule.delete_timeoff(gp_id_choice, 'custom', 'time off', start_date, end_date)
        
        # Proceed with next section
        return utils.display(next_dict)

    else:
        # Return to main remove time off menu
        return remove_time_off(next_dict)


def remove_time_off_all(next_dict):
    '''
    Remove time off from a GP's schedule.
    '''
    print("\n----------------------------------------------------\n"
          "                ",'REMOVE TIME OFF - ALL', "\n")

    # Prompt user for type of time off
    print("Please select the time off type: ")
    print("\n [ 1 ] Sick leave \n [ 2 ] General time off \n [ 3 ] Both")
    timeoff_type_input = input('\n--> ')

    while timeoff_type_input not in ('1', '2', '3'):
        print("\n\U00002757 Invalid entry, please try again")
        timeoff_type_input = input('\n--> ')
        
    if timeoff_type_input == '1':
        timeoff_type = 'sick leave'
    elif timeoff_type_input == '2':
        timeoff_type = 'time off'
    elif timeoff_type_input == '3':
        timeoff_type = 'all time off'

    # Confirmation step
    print("\n----------------------------------------------------\n"
          "                ",'CONFIRM?', "\n")

    print('\nDo you want to remove {} from the schedule?\n'.format(timeoff_type))
    print("[ 1 ] Yes")
    print("[ 2 ] No")

    user_confirmation = input("\n--> ")

    while user_confirmation not in ('1','2'):
            print("\n\U00002757 Invalid entry, please try again")
            user_confirmation = input("\n--> ")

    if user_confirmation == '1':
        # Remove timeoff of a specific type from db
        if timeoff_type_input in ('1', '2'):
            Schedule.delete_timeoff(gp_id_choice, 'all', timeoff_type)
            print("\n\U00002705 Time off successfully removed.")

        # Remove timeoff of both types from db
        elif timeoff_type_input == '3':
            Schedule.delete_timeoff(gp_id_choice, 'all', 'sick leave')
            Schedule.delete_timeoff(gp_id_choice, 'all', 'time off')
        
        # Proceed with next section
        return utils.display(next_dict)

    else:
        # Return to main remove time off menu
        return remove_time_off(next_dict)



def remove_more_time_off(next_dict):
    '''
    Allows cycling back to the remove_time_off menu from the final_menu.
    '''
    return utils.display(remove_time_off_flow)



###### MANAGE UPCOMING APPOINTMENTS FUNCTIONS ######


def appointments_section_menu(next_dict):
    '''
    Returns to the section menu.
    '''
    return utils.display(manage_appointment_flow)


def view_appointment(next_dict):
    '''
    View all appointments for a specific GP after the current time.
    '''
    apps = Appointment.select_GP_appt(gp_id_choice)
    print(apps)

    return utils.display(next_dict)

#NOTE: INCOMPLETE
def add_appointment(next_dict):
    '''
    Schedule an appointment for a GP.
    '''
    #TODO: GET RID OF THIS AND CALL EMPTY_METHOD.
    return utils.display(next_dict)


#NOTE: INCOMPLETE
def choose_appointment_day(next_dict):
    '''
    Choose the appointment from a day of available slots.
    '''
    print("\n----------------------------------------------------\n"
          "                ",'ENTER DAY', "\n")
    start_date = utils.get_start_date()

    print("\n----------------------------------------------------\n"
          "                ",'ENTER LAST NAME', "\n")
    last_name = input("Please enter the patient's last name:\n"
    "--> ")
    choose_patient('matching', patient_last_name=last_name)
    patient_id = int(input('\nPlease choose a patient ID\n'
    '--> '))
    selected_patient = Patient.select(patient_id)

    gp_id = selected_patient[0].gp_id
    gp_lastname = GP.select(gp_id)[0].last_name
    
    appt_df = Appointment.select_availability('day', gp_id, start_date)

    print(appt_df[1])
    appt_selected = int(input('\nPlease choose the slot to book the appointment in:\n'
    '-->\n'))
    #TODO: BOOK THE APPOINTMENT IF VALID INPUT.
    #NOTE: LOTS OF SHARED CODE BETWEEN THIS AND CHOOSE APPOINTMENT WEEK.
    return utils.display(next_dict)


#NOTE: INCOMPLETE
def choose_appointment_week(next_dict):
    '''
    Choose the appointment from a week of available slots.
    '''
    print("\n----------------------------------------------------\n"
          "                ",'ENTER WEEK START DATE', "\n")
    start_date = utils.get_start_date()

    print("\n----------------------------------------------------\n"
          "                ",'ENTER LAST NAME', "\n")
    last_name = input("Please enter the patient's last name:\n"
    "--> ")
    choose_patient('matching', patient_last_name=last_name)
    patient_id = int(input('\nPlease choose a patient ID\n'
    '--> '))
    selected_patient = Patient.select(patient_id)

    gp_id = selected_patient[0].gp_id
    gp_lastname = GP.select(gp_id)[0].last_name
    
    appt_df = Appointment.select_availability('week', gp_id, start_date)

    print(appt_df[1])
    appt_selected = int(input('\nPlease choose the slot to book the appointment in:\n'
    '-->\n'))
    #TODO: BOOK THE APPOINTMENT IF VALID INPUT.
    #NOTE: LOTS OF SHARED CODE BETWEEN THIS AND CHOOSE APPOINTMENT DAY.
    return utils.display(next_dict)


def appointment_by_patient(next_dict):
    '''
    Find a patient's upcoming appointments.
    '''
    # NOTE: Reusing code from view_patient (which actually also handles updating)

    # Create a shortlist by last name
    print("\n----------------------------------------------------\n"
          "                ",'SELECT PATIENT', "\n")
    last_name = input("Please enter the patient's last name:\n"
    "--> ")
    choose_patient('matching', patient_last_name=last_name)

    # Select ID of the patient of interest 
    selected_patient_id = input('\nPlease choose a patient ID\n--> ')
    
    # Select all upcoming appointments for this patient ID
    appts = Appointment.select_patient('upcoming', selected_patient_id)

    # Print the appointments information
    print(appts[1])

    return utils.display(next_dict)


def appointment_check(next_dict):
    # NOTE to Tom: I don't see this being use anywhere else. Still useful?
    '''
    Check whether the appointment selected is available.
    '''
    return utils.display(next_dict)
    

def appointment_by_gp(next_dict):
    '''
    Find a GP's appointments after a certain date and display them in day/week view.
    '''
    # Prompt user for GP
    df = GP.select_list('all')
    df_show = df[1]
    print("\n----------------------------------------------------\n"
          "                ",'GP LIST', "\n")
    print(df_show)
    global gp_id_choice
    gp_id_choice = int(input("\nPlease select a GP ID. \n--> "))
    
    # Prompt user for starting date
    print("\n----------------------------------------------------\n"
      "                ",'SELECT DATE', "\n")

    start_date = utils.get_start_date()

    print("\n----------------------------------------------------\n"
      "                ",'SELECT VIEW', "\n")

    # Prompt user for type of view
    print("Please select the date view: ")
    print("\n [ 1 ] Day \n [ 2 ] Week")
    view_input = input('\n--> ')

    while view_input not in ('1', '2'):
        print("\n\U00002757 Invalid entry, please try again")
        view_input = input('\n--> ')
        
    if view_input == '1':
        view_type = 'day'
    elif view_input == '2':
        view_type = 'week'

    appts = Appointment.select_GP(view_type, gp_id_choice, start_date)
    print(appts[1])

    return utils.display(next_dict)

# NOTE: delete_appointment could be done with day / week / custom
# Appointment class method supports it already
def delete_appointment_day(next_dict):
    '''
    Allows deleting of all appointments for a specific GP in a specific day.
    '''

    start = utils.get_start_date()
    end = start

    print("\n----------------------------------------------------\n"
          "                ",'INSERT REASON', "\n")
    reason = input("Please insert reason for batch rejection: \n--> ")    

    print("\n----------------------------------------------------\n"
          "                ",'CONFIRM?', "\n")
    print("Do you want to reject all appointments on {} for GP with ID {}?\n".format(start, gp_id_choice))
    print("[ 1 ] Yes\n[ 2 ] No")
    y_n = input('\n--> ')

    while y_n not in ('1', '2'):
        print("\n\U00002757 Invalid entry, please try again")
        y_n = input('\n--> ')
        
    if y_n == '1':
         Appointment.change_status_batch_future(start, end, gp_id_choice, "rejected", reason)
         print("\U00002705 Appointments rejected.")
         utils.display(next_dict)

    elif y_n == '2':
        utils.display(delete_gp_appointment_flow)

def delete_appointment_week(next_dict):
    '''
    Allows deleting of all appointments for a specific GP in a specific week.
    '''
    
    start = utils.get_start_date()
    end = start + timedelta(weeks=1) 

    print("\n----------------------------------------------------\n"
          "                ",'INSERT REASON', "\n")
    reason = input("Please insert reason for batch rejection: \n--> ")    

    print("\n----------------------------------------------------\n"
          "                ",'CONFIRM?', "\n")
    print("Do you want to reject all appointments from {} to {} for GP with ID {}?\n"
    .format(start, end, gp_id_choice))

    print("[ 1 ] Yes\n[ 2 ] No")
    y_n = input('\n--> ')

    while y_n not in ('1', '2'):
        print("\n\U00002757 Invalid entry, please try again")
        y_n = input('\n--> ')
        
    if y_n == '1':
         Appointment.change_status_batch_future(start, end, gp_id_choice, "rejected", reason)
         print("\U00002705 Appointments rejected.")
         utils.display(next_dict)

    elif y_n == '2':
        utils.display(delete_gp_appointment_flow)


###### RECORDS FUNCTIONS ######

#NOTE: This whole section has been simplified from the flow diagram, 
#      with 'summaries' changed to 'records'. Now, only choice to be
#      made is selecting the patient, which is done within the one 
#      function.


def records_main(next_dict):
    '''
    Allows the selection of a patient's medical records. 
    '''
    print("\n----------------------------------------------------\n"
          "                ",'SELECT PATIENT', "\n")
    
    # Filter by last name
    last_name = input("Please enter the patient's last name:\n"
    "--> ")
    choose_patient('matching', patient_last_name=last_name)

    # Select the ID of the patient whose records we want to access    
    patient_id_input = input('\nPlease choose a patient ID \n--> ')

    # Retrieve patient records
    record = Record.select(patient_id_input)

    # Display patient records
    print(record[2])

    return utils.display(next_dict)


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
    "1": ("Delete Another GP", delete_another_gp, empty_dict),
    "2": ("Section Menu", gp_account_section_menu, empty_dict)
}

deactivate_gp_account_final_menu = {
    "title": "NEXT ACTIONS",
    "type": "sub",
    "1": ("Deactivate Another GP", deactivate_another_gp, empty_dict),
    "2": ("Section Menu", gp_account_section_menu, empty_dict)
}

add_new_gp_account_final_menu = {
    "title": "NEXT ACTIONS",
    "type": "sub",
    "1": ("Add Another GP", add_another_gp, empty_dict),
    "2": ("Section Menu", gp_account_section_menu, empty_dict)
}

view_edit_gp_accounts_final_menu = {
    "title": "NEXT ACTIONS",
    "type": "sub",
    "1": ("View/Modify Same GP", same_gp, empty_dict),
    "2": ("GP List", view_another_gp, empty_dict),
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
    "1": ("Delete Another Patient", delete_another_patient, empty_dict),
    "2": ("Section Menu", patient_account_section_menu, empty_dict)
}

add_new_patient_account_final_menu = {
    "title": "NEXT ACTIONS",
    "type": "sub",
    "1": ("Add Another Patient", confirm_another_patient, empty_dict),
    "2": ("Section Menu", patient_account_section_menu, empty_dict)
}

view_edit_patient_accounts_final_menu = {
    "title": "NEXT ACTIONS",
    "type": "sub",
    "1": ("View/Modify Same Patient", same_patient, empty_dict),
    "2": ("Patient Search Page", view_another_patient, empty_dict),
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
    "1": ("Remove More Time Off", remove_more_time_off, empty_dict),
    "2": ("Manage Upcoming Time Off", manage_more_time_off, empty_dict),
    "3": ("Manage GP Availability", manage_more_availability, empty_dict),
    "4": ("Choose a different GP", choose_another_gp, empty_dict),
    "5": ("Section Menu", schedules_section_menu, empty_dict)
}

remove_time_off_flow = {
    "title": "SELECT TIME OFF LENGTH",
    "type": "sub",
    "1": ("All", remove_time_off_all, remove_time_off_final_actions),
    "2": ("Custom", remove_time_off_custom, remove_time_off_final_actions)
}

appointment_conflict_final_actions = {
    "title": "NEXT ACTIONS",
    "type": "sub",
    "1": ("Try Adding Again", add_time_off, empty_dict),
    "2": ("Manage Upcoming Time Off", manage_more_time_off, empty_dict),
    "3": ("Manage GP Availability", manage_more_availability, empty_dict),
    "4": ("Choose a different GP", choose_another_gp, empty_dict),
    "5": ("Section Menu", schedules_section_menu, empty_dict)
}

add_time_off_final_actions = {
    "title": "NEXT ACTIONS",
    "type": "sub",
    "1": ("Add More Time Off", add_time_off, empty_dict),
    "2": ("Remove Time Off", remove_time_off, remove_time_off_flow),
    "3": ("Choose a different GP", choose_another_gp, empty_dict),
    "4": ("Section Menu", schedules_section_menu, empty_dict)
}

add_time_off_flow = {
    "title": "SELECT TIME OFF LENGTH",
    "type": "sub",
    "1": ("Day", add_time_off_day, add_time_off_final_actions),
    "2": ("Week", add_time_off_week, add_time_off_final_actions),
    "3": ("Custom", add_time_off_custom, add_time_off_final_actions),
}

view_time_off_final_actions = {
    "title": "NEXT ACTIONS",
    "type": "sub",
    "1": ("Add Time Off", add_time_off, add_time_off_flow),
    "2": ("Remove Time Off", remove_time_off, remove_time_off_flow),
    "3": ("Manage GP Availability", manage_more_availability, empty_dict),
    "4": ("Choose a different GP", choose_another_gp, empty_dict),
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
    "title": "VIEW AND MANAGE AVAILABILITY",
    "type": "sub",
    "1": ("View Upcoming Appointments", appointments_shortcut, empty_dict),
    "2": ("Manage Upcoming Time Off", empty_method, manage_time_off_flow)
}

view_schedule_final_actions = {
    "title": "NEXT ACTIONS",
    "type": "sub",
    "1": ("Modify GP Availability", empty_method, manage_availability_flow),
    "2": ("View a Different Time Period", view_another_schedule, empty_dict),
    "3": ("Choose a different GP", choose_another_gp, empty_dict),
    "4": ("Section Menu", schedules_section_menu, empty_dict)
}

schedule_length_flow = {
    "title": "SELECT SCHEDULE LENGTH",
    "type": "sub",
    "1": ("Day", view_schedule_day, view_schedule_final_actions),
    "2": ("Week", view_schedule_week, view_schedule_final_actions),
}

view_schedule_flow = {
    "title": "VIEW AND MANAGE SCHEDULE",
    "type": "sub",
    "1": ("View GP Schedule", empty_method, schedule_length_flow),
    "2": ("Manage GP Availability", empty_method, manage_availability_flow)
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
    "title": "DATE RANGE - APPOINTMENTS TO REJECT",
    "type": "sub",
    "1": ("Day", delete_appointment_day, appointment_deleted_gp_final_actions),
    "2": ("Week", delete_appointment_week, appointment_deleted_gp_final_actions)
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
    "1": ("Try again", empty_method, empty_dict),
    "2": ("Add Another Appointment", add_appointment, empty_dict),
    "3": ("Section Menu", appointments_section_menu, empty_dict)
}

appointment_made_final_actions = {
    "title": "NEXT ACTIONS",
    "type": "sub",
    "1": ("Add Another Appointment For This Patient", add_appointment, empty_dict),
    "2": ("Add Appointment For Another Patient", empty_method, empty_dict),
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
    "1": ("Day", choose_appointment_day, appointment_made_final_actions),
    "2": ("Week", choose_appointment_week, appointment_made_final_actions)
}

manage_appointment_flow = {
    "title": "MANAGE APPOINTMENTS",
    "type": "sub",
    "1": ("Add a New Appointment", add_appointment, add_new_appointment_flow),
    "2": ("Manage Upcoming Appointment", empty_method, view_cancel_appointment_flow)
}

###### VIEW APPOINTMENT SUMMARIES SUB-MENU ######

appointment_summary_final_actions = {
    "title": "NEXT ACTIONS",
    "type": "sub",
    "1": ("View a Different Appointment", empty_method, empty_dict),
    "2": ("View a Different Patient", records_main, empty_dict),
}

###### MAIN MENU ####

main_flow_admin = {
    "title": "ADMIN MAIN MENU",
    "type":"main",
    "1":("Manage GP Accounts", empty_method, manage_gp_accounts_flow),
    "2":("Manage Patient Accounts", empty_method, manage_patient_accounts_flow ),
    "3":("Manage GP-Patient Pairings", empty_method, gp_patient_pair_flow),
    "4":("Manage GP Schedules", choose_gp, view_schedule_flow),
    "5":("Manage Upcoming Appointments", empty_method, manage_appointment_flow),
    "6":("View Appointment Summaries", records_main, appointment_summary_final_actions)
}


############################# TESTING ###############################

if __name__ == '__main__':
    utils.display(main_flow_admin)
    pass
    