# admin_flow.py

# library imports 
from datetime import datetime, timedelta, date
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


def view_edit_gp(next_dict):
    '''
    Select from a list of GPs and allows choice for viewing.
    '''

    profile = {
    1: 'first_name',
    2: 'last_name',
    3: 'gender',
    4: 'birth_date',
    5: 'email',
    6: 'working_days',
    7: 'department_id',
    8: 'specialisation_id',
    9: 'status'
    }

    # Check if gp id already selected previously for reuse
    if 'gp_id_choice' not in globals():
        choice = retrieve_gp('all')
    else:
        global gp_id_choice
        choice = gp_id_choice

    doctor_df = GP.select(choice)

    print("\n----------------------------------------------------\n"
          "                ",'GP DETAILS', "\n")
    print(doctor_df[2])
    key = int(input("Choose a value to edit. \n--> "))

    if key not in range(1,len(profile)+1):
        print("\n\U00002757 Input not valid.")
        key = int(input("Choose a value to edit. \n--> "))

    new_value = input("\nChoose a new value to input. \n--> ") 

    print("\n----------------------------------------------------\n"
          "                ",'CONFIRM?', "\n")
    print("Do you want to edit field [{}] with the new value '{}'?".format(key, new_value))
    print("[ 1 ] Yes")
    print("[ 2 ] No")

    y_n = int(input("\n--> "))

    while y_n not in (1,2):
        print("\n\U00002757 Input not valid.")
        y_n = int(input("\n--> "))
    
    if y_n == 1:
        # Get raw df to edit
        df = doctor_df[0]

        # Update the selected section to the new value 
        df.__dict__[profile[key]] = new_value

        # Update in the database
        df.update()
        print("\n\U00002705 GP profile successfully updated.")
        return utils.display(next_dict)
        
    elif y_n == 2:
        return utils.display(next_dict)


def retrieve_gp(type):
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



def view_same_gp(next_dict):
    '''
    Allows cycling back to the view_gp function for the same GP,
    stored in the global variable gp_choice.
    '''
    return view_edit_gp(view_edit_gp_accounts_final_menu)


def view_another_gp(next_dict):
    '''
    Allows cycling back to the view_gp function from final_menu,
    deleting the global variable so a different GP can be viewed.
    '''
    global gp_id_choice
    del gp_id_choice
    return view_edit_gp(view_edit_gp_accounts_final_menu)


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

    # TODO: List out Depts and Specializations and allow choice

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
    gp_id = retrieve_gp('active')

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
    Deletes a GP.
    '''
    # List and prompt admin for a gp id
    gp_id = retrieve_gp('all')

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
    

def retrieve_patient():
    print("\n----------------------------------------------------\n"
    "                ",'ENTER LAST NAME', "\n")
    valid = False

    while valid == False :
        last_name = input("\nPlease enter the patient's last name:\n--> ")
        
        choose_patient('matching', patient_last_name=last_name)

        # Select ID of the patient of interest 
        selected_patient_id = input('\nPlease choose a patient ID \nOr enter \'#\' to change the patient\'s last name \n--> ')

        if selected_patient_id == '#':
            valid = False

        elif selected_patient_id.isnumeric() and utils.validate(selected_patient_id) :
            valid = True

        else:
            print("\U00002757 Invalid entry, please try again and enter your choice.")

    return selected_patient_id


def view_edit_patient(next_dict):
    '''
    View a Patient Account.
    '''

    profile = {
    1: 'first_name',
    2: 'last_name',
    3: 'gender',
    4: 'birth_date',
    5: 'email',
    6: 'NHS_blood_donor',
    7: 'NHS_organ_donor',
    8: 'status'
    }

    if 'patient_id_choice' not in globals():
        choice = retrieve_patient()
    else:
        global patient_id_choice
        choice = patient_id_choice
        
    selected_patient = Patient.select(choice)
    print("\n----------------------------------------------------\n"
          "                ",'PATIENT DETAILS', "\n")
    print(selected_patient[2])
    print('\nYou are viewing the details of {} {} (ID: {}).'.format(selected_patient[0].first_name, selected_patient[0].last_name, choice))
    
    print("\n----------------------------------------------------\n"
    "                ",'EDIT THIS PATIENT?', "\n")
    print('[ 1 ] Yes')
    print('[ 2 ] Choose Another Patient')
    edit_choice = int(input('--> '))

    while edit_choice not in (1, 2):
        print("\n\U00002757 Invalid entry, please try again")
        edit_choice = int(input('\n--> '))

    if edit_choice == 2:

        del patient_id_choice
        return view_edit_patient(next_dict)

    else:
        key = int(input("Choose a value to edit. \n--> "))
        new_value = input("\nChoose a new value to input. \n--> ") 

        print("\n----------------------------------------------------\n"
          "                ",'CONFIRM?', "\n")
        print("Do you want to edit field [{}] with the new value '{}'?".format(key, new_value))
        print("[ 1 ] Yes")
        print("[ 2 ] No")
    
    y_n = int(input("\n--> "))
    
    while y_n not in (1,2):
        print("\n\U00002757 Input not valid.")
        y_n = int(input("\n--> "))

    if y_n == 1:
        # Get raw df to edit
        df = selected_patient[0]

        # Update the selected section to the new value 
        df.__dict__[profile[key]] = new_value

        # Update in the database
        df.update()
        print("\n\U00002705 Patient profile successfully updated.")
        return utils.display(next_dict)
        
    elif y_n == 2:
        return utils.display(next_dict)


def view_same_patient(next_dict):
    '''
    Allows cycling back to the view_edit_patient function from the final_menu
    for the same patient.
    '''
    return view_edit_patient(view_edit_patient_accounts_final_menu)


def view_another_patient(next_dict):
    '''
    Allows cycling back to the view_edit_patient function from the final_menu
    for another patient.
    '''
    global patient_id_choice
    del patient_id_choice
    return view_edit_patient(view_edit_patient_accounts_final_menu)


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
    return utils.display(view_appointment_by_gp)


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

# TODO: Schedule func update is causing error - Discuss with Manuel
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
            Schedule.delete_timeoff(gp_id_choice, 'custom', start_date, end_date)
        
        # Proceed with next section
        return utils.display(next_dict)

    else:
        # Return to main remove time off menu
        return remove_time_off(next_dict)


def remove_time_off_all(next_dict):
    '''
    Remove time off from future GP's schedule.
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


def add_appointment(next_dict):
    '''
    Choose the appointment from a day of available slots.
    '''
    if 'patient_id_choice' not in globals():
        choice = retrieve_patient()
    else:
        global patient_id_choice
        choice = patient_id_choice
    
    selected_patient = Patient.select(choice)
    patient_name = selected_patient[0].first_name + ' ' + selected_patient[0].last_name
    patient_id = selected_patient[0].id

    gp_id, gp_name = selected_patient[0].select_gp_details(choice)

    print('\nPatient {} (ID: {}) is registered with {} (ID: {})'.format(patient_name, choice, gp_name, gp_id))

    print("\n----------------------------------------------------\n"
    "                ","EDIT THIS PATIENT'S APPOINTMENTS?", "\n")
    print('[ 1 ] Yes')
    print('[ 2 ] Choose Another Patient')
    edit_choice = int(input('--> '))

    while edit_choice not in (1, 2):
        print("\n\U00002757 Invalid entry, please try again")
        edit_choice = int(input('\n--> '))

    if edit_choice == 2:
        patient_id_choice = ''
        del patient_id_choice
        return add_appointment(next_dict)

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
        print("\n\U00002757 Invalid entry, please try again and enter 1, 2 or #.")
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
        print("\n\U00002757 Invalid entry, please try again and enter 1, 2 or #.")
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
          "you want to display availability\n\n"
          "Enter 'T' to see availability from today")

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
            if date.fromisoformat(start_date) >= date.today():
                valid = True
            
            else:
                print("\n\U00002757 Appointment date must be in the future.")
        
        if valid == False:
            start_date = input("\n--> ")

    # Calling the Appointment class static method select_availability or select_other_availability to display desired availibility
    if personal_gp == True: 
        availability = Appointment.select_availability(view, gp_id, start_date)

    else: 
        availability = Appointment.select_other_availability(view, Patient.select_gp_details(patient_id)[0], start_date)
        boolean_available = availability[6]

        # if no availability amongst other GPs
        if boolean_available == False:
            print("\n\U00002757 No availability among other GPs for the dates selected, \nplease book with your personal GP or change dates.")
            return add_appointment(next_dict)

        # if availability, get displayed gp_ID and name
        else:
            gp_id = availability[4]
            gp_name = availability[5]

    # morning availability first with 3 user choices outside of booking indexes
    morning = True
    options = ('#','A','a')
    
    # Print morning availability
    print("\n\n--- Morning ---\n" + availability[2])

    print("\n[ ... ] Enter the index of the time slot to book")

    print("\n[ A ] Display afternoon availability")
    print("[ # ] Display other availabilities (different dates or GPs) ")

    # Require user choice of booking slot
    booking_index = input("\n--> ")

    # Formatting user input correctly
    if booking_index not in options :
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
        while len(selected_time_slot.index) != 1 and booking_index not in options:
            print("\n\U00002757 Invalid entry, please try again and enter a valid time slot index.")
            booking_index = input("\n--> ")

            # Formatting user input correctly
            if booking_index not in options :
                while len(booking_index) < 3:
                    booking_index = '0' + booking_index

            selected_time_slot = availability[0].where(availability[0]=="["+booking_index+"]").dropna(how='all').dropna(axis=1)

        # if user wants to display new availability, recursive call of the function itself
        if booking_index == "#":
            return add_appointment(next_dict)

        # if user wants to display afternoon availability
        elif booking_index in ("A","a"):
            # Updating Boolean and options
            morning = False
            options = ('#')
            # Print afternoon availability
            print("\n\n--- Afternoon ---\n" + availability[3])
            print("\n[ ... ] Enter the index of the time slot to book")
            print("[ # ] Display other availabilities (different dates or GPs) ")
            
            # Require user choice of booking slot
            booking_index = input("\n--> ")

            # Formatting user input correctly
            if booking_index not in options:
                while len(booking_index) < 3:
                    booking_index = '0' + booking_index

            selected_time_slot = availability[0].where(availability[0]=="["+booking_index+"]").dropna(how='all').dropna(axis=1)

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
                print("\n\U00002757 Invalid entry, please try again and enter 1 or 2.")
                user_confirmation = input("\n--> ")

            # If user confirms booking, exit loop
            if user_confirmation == '1': 
                confirmation = True

            # if user doesn't confirm --> initialised variables and loop again
            else: 
                confirmation = False

                # initialising variables
                print("\n[ ... ] Enter the index of the time slot to book")

                if morning == True:
                    print("\n[ A ] Display afternoon availability")
                
                print("[ # ] Display other availabilities (different dates or GPs) ")
                booking_index = input("\n--> ")

                # Formatting user input correctly
                if booking_index not in options:
                    while len(booking_index) < 3:
                        booking_index = '0' + booking_index

                selected_time_slot = availability[0].where(availability[0]=="["+booking_index+"]").dropna(how='all').dropna(axis=1)
    

    # Now that user has confirmed appointment, require appointment type (online or offline)  
    print("\nDo you want to add appointment in person or online ?")
    print("\n[ 1 ] Online")
    print("[ 2 ] In person")
    print("\n[ # ] Cancel appointment booking")

    # ask user choice
    i = input("\n--> ")
    
    # while invalid user input
    while i not in ("1","2","#"):
        print("\n\U00002757 Invalid entry, please try again and enter 1, 2 or #.")
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
    booking = Appointment(booking_start_time = str(booking_date) + " " + str(booking_time), booking_agenda = booking_agenda, booking_type = booking_type, patient_id = patient_id, gp_id = gp_id)

    # Book appointment on Database
    success, reason = booking.book()

    if success:
        print("\n\U00002705 Appointment successfully booked with " + gp_name + " at " + str(booking_time) + " on the " + str(booking_date) + ".")
        return utils.display(next_dict)

    else:
        print("\n\U00002757 " + reason)
        return add_appointment(next_dict)


def add_another_appointment_diff_patient(next_dict):
    '''
    Allows cycling back to the add_appointment function for a different patient choice.
    '''
    global patient_id_choice
    patient_id_choice = ''
    del patient_id_choice
    return add_appointment(appointment_made_final_actions)


def add_another_appointment_same_patient(next_dict):
    '''
    Allows cycling back to the add_appointment function for the same patient.
    '''
    return add_appointment(appointment_made_final_actions)


def view_appointment_by_patient(next_dict):
    '''
    Find a patient's upcoming appointments.
    '''
    # Create a shortlist by last name
    print("\n----------------------------------------------------\n"
          "                ",'SELECT PATIENT', "\n")

    valid = False

    while valid == False :
        last_name = input("\nPlease enter the patient's last name:\n--> ")
        
        choose_patient('matching', patient_last_name=last_name)

        # Select ID of the patient of interest 
        selected_patient_id = input('\nPlease choose a patient ID \nOr enter \'#\' to change the patient\'s last name \n--> ')

        if selected_patient_id == '#':
            valid = False

        elif selected_patient_id.isnumeric() and utils.validate(selected_patient_id) :
            valid = True

        else:
            print("\U00002757 Invalid entry, please try again and enter your choice.")
    
    # Select all upcoming appointments for this patient ID
    appts = Appointment.select_patient('upcoming', selected_patient_id)

    # Print the appointments information
    print(appts[1])

    return utils.display(next_dict)


def view_appointment_by_same_patient(next_dict):
    '''
    Allows cycling back to allow deletion of more appointments for the same patient.
    '''
    return view_appointment_by_patient(appointment_viewed_patient_final_actions)


def view_appointment_by_another_patient(next_dict):
    '''
    Allows cycling back to allow deletion of more appointments for another patient.
    '''
    return view_appointment_by_patient(appointment_viewed_patient_final_actions)
    

def view_appointment_by_gp(next_dict):
    '''
    Find a GP's appointments after a certain date and display them in day/week view.
    '''
    # Prompt user for GP
    df = GP.select_list('all')
    df_show = df[1]
    print("\n----------------------------------------------------\n"
          "                ",'GP LIST', "\n")
    print(df_show)
    
    valid = False

    while valid == False :
        global gp_id_choice
        gp_id_choice = input("\nPlease select a GP ID. \n--> ")

        if gp_id_choice.isnumeric() and utils.validate(gp_id_choice):
            valid = True
            gp_id_choice = int(gp_id_choice)

        else:
            print("\U00002757 Invalid entry, please try again and enter your choice.")

    
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


def delete_appointment_gp(next_dict):
    '''
    Allows deleting of appointments for a specific GP in a specified data range.
    '''

    if 'gp_id_choice' not in globals():
        gp_id = retrieve_gp('all')
    else:
        global gp_id_choice
        gp_id = gp_id_choice

    print("\n----------------------------------------------------\n"
          "                ",'INSERT DATE RANGE', "\n")
    print("Please insert date range for batch cancellation:")    
    print("[ 1 ] Day\n[ 2 ] Week\n[ 3 ] Custom")
    date_range = int(input('\n--> '))

    while date_range not in (1,2,3):
        print("\n\U00002757 Invalid entry, please try again")
        date_range = int(input('\n--> '))

    start = utils.get_start_date()

    # Day
    if date_range == 1:
        end = start

    # Week
    elif date_range == 2:
        s = datetime.strptime(start, "%Y-%m-%d")
        e = s + timedelta(weeks=1) 
        end = datetime.strftime(e, "%Y-%m-%d")   

    # Custom
    else:
        end = utils.get_end_date()

    print("\n----------------------------------------------------\n"
          "                ",'INSERT REASON', "\n")
   
    validate = False
    while validate == False:
        reason = input("Please insert reason for batch rejection: \n--> ")    

        if utils.validate(reason):
            validate = True

    print("\n----------------------------------------------------\n"
          "                ",'CONFIRM?', "\n")
    print("Do you want to reject all appointments from {} to {} for GP with ID {}?\n".format(start, end, gp_id))
    print("[ 1 ] Yes\n[ 2 ] No")
    y_n = int(input('\n--> '))

    while y_n not in (1, 2):
        print("\n\U00002757 Invalid entry, please try again")
        y_n = int(input('\n--> '))
        
    if y_n == 1:
         Appointment.change_status_batch_future(start, end, gp_id, "rejected", reason)
         print("\n\U00002705 Appointments deleted.")
         utils.display(next_dict)

    elif y_n == 2:
        utils.display(appointment_deleted_gp_final_actions)


def delete_appointment_patient(next_dict):
    '''
    Allows deleting of appointments for a specific Patient in a specified data range.
    '''

    if 'patient_id_choice' not in globals():
        patient_id = retrieve_patient()
    else:
        global patient_id_choice
        patient_id = patient_id_choice

    print("\n----------------------------------------------------\n"
          "                ",'INSERT DATE RANGE', "\n")
    print("Please insert date range for batch cancellation: ")    
    print("[ 1 ] Day\n[ 2 ] Week\n[ 3 ] Custom")
    date_range = int(input('\n--> '))

    while date_range not in (1,2,3):
        print("\n\U00002757 Invalid entry, please try again")
        date_range = int(input('\n--> '))

    start = utils.get_start_date()

    # Day
    if date_range == 1:
        end = start

    # Week
    elif date_range == 2:
        s = datetime.strptime(start, "%Y-%m-%d")
        e = s + timedelta(weeks=1) 
        end = datetime.strftime(e, "%Y-%m-%d")   

    # Custom
    else:
        end = utils.get_end_date()

    print("\n----------------------------------------------------\n"
          "                ",'INSERT REASON', "\n")
    
    validate = False
    while validate == False:
        reason = input("Please insert reason for batch rejection: \n--> ")    

        if utils.validate(reason):
            validate = True

    print("\n----------------------------------------------------\n"
          "                ",'CONFIRM?', "\n")
    print("Do you want to reject all appointments from {} to {} for Patient with ID {}?\n".format(start, end, patient_id))
    print("[ 1 ] Yes\n[ 2 ] No")
    y_n = int(input('\n--> '))

    while y_n not in (1, 2):
        print("\n\U00002757 Invalid entry, please try again")
        y_n = int(input('\n--> '))
        
    if y_n == 1:
         Appointment.change_status_batch_future_patient(start, end, patient_id, "rejected", reason)
         print("\n\U00002705 Appointments deleted.")
         utils.display(next_dict)

    elif y_n == 2:
        utils.display(appointment_deleted_gp_final_actions)


def delete_appointment_another_gp(next_dict):
    '''
    Allows cycling back to delete another appointment of the same GP.
    '''
    global gp_id_choice
    gp_id_choice = ''
    del gp_id_choice
    return delete_appointment_gp(next_dict)


def delete_appointment_another_patient(next_dict):
    '''
    Allows cycling back to delete another appointment of the same GP.
    '''
    global patient_id_choice
    patient_id_choice = ''
    del patient_id_choice
    return delete_appointment_patient(next_dict)


###### RECORDS FUNCTIONS ######

# This whole section has been simplified from the flow diagram, 
# with 'summaries' changed to 'records'. Now, only choice to be
# made is selecting the patient, which is done within the one function.


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


def another_record_same_patient(next_dict):
    '''
    Allows viewing of another record for the same patient.
    '''
    return records_main(records_final_menu)



def another_record_diff_patient(next_dict):
    '''
    Allows viewing of another record for the same patient.
    '''
    return records_main(records_final_menu)


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
    "1": ("View/Modify Same GP", view_same_gp, empty_dict),
    "2": ("View/Modify Another GP", view_another_gp, empty_dict),
    "3": ("Section Menu", gp_account_section_menu, empty_dict)
}

manage_gp_accounts_flow = {
    "title": "MANAGE GP ACCOUNTS",
    "type": "sub",
    "1":("View/Edit GP Details", view_edit_gp, view_edit_gp_accounts_final_menu),
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
    "1": ("View/Modify Same Patient", view_same_patient, empty_dict),
    "2": ("Patient Search Page", view_another_patient, empty_dict),
    "3": ("Section Menu", patient_account_section_menu, empty_dict)
}

manage_patient_accounts_flow = {
    "title": "MANAGE PATIENT ACCOUNTS",
    "type": "sub",
    "1":("View/Edit Patient Details", view_edit_patient, view_edit_patient_accounts_final_menu),
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
    "1": ("Delete Another GP's Appointments", delete_appointment_another_gp, empty_dict),
    "2": ("Search by Patient", view_appointment_by_patient, empty_dict),
    "3": ("Section Menu", appointments_section_menu, empty_dict)
}


appointment_deleted_patient_final_actions = {
    "title": "NEXT ACTIONS",
    "type": "sub",
    "1": ("Delete Another Patient's Appointments", delete_appointment_another_patient, empty_dict),
    "2": ("Search by GP", view_appointment_by_gp, empty_dict),
    "3": ("Section Menu", appointments_section_menu, empty_dict)
}

appointment_viewed_gp_final_actions = {
    "title": "NEXT ACTIONS",
    "type": "sub",
    "1": ("View Another GP's Appointments", view_appointment_by_gp, empty_dict),
    "2": ("Delete This GP's Appointments", delete_appointment_gp, empty_dict),
    "3": ("Search by Patient", view_appointment_by_patient, empty_dict),
    "4": ("Section Menu", appointments_section_menu, empty_dict)
}

appointment_viewed_patient_final_actions = {
    "title": "NEXT ACTIONS",
    "type": "sub",
    "1": ("View Another Patient's Appointments", view_appointment_by_patient, empty_dict),
    "2": ("Delete This Patient's Appointments", delete_appointment_patient, empty_dict),
    "3": ("Search by GP", view_appointment_by_gp, empty_dict),
    "4": ("Section Menu", appointments_section_menu, empty_dict)
}

delete_appointment_flow = {
    "title": "DELETE UPCOMING APPOINTMENTS",
    "type": "sub",
    "1": ("Patient", delete_appointment_patient, appointment_deleted_patient_final_actions),
    "2": ("GP", delete_appointment_gp, appointment_deleted_gp_final_actions)
}

view_appointment_flow = {
    "title": "VIEW UPCOMING APPOINTMENTS",
    "type": "sub",
    "1": ("Search By Patient", view_appointment_by_patient, appointment_viewed_patient_final_actions),
    "2": ("Search By GP", view_appointment_by_gp, appointment_viewed_gp_final_actions)
}

gp_availability_error_final_actions = {
    "title": "NEXT ACTIONS",
    "type": "sub",
    "1": ("Try Again For the Same Patient", add_another_appointment_same_patient, empty_dict),
    "2": ("Add Another Appointment for a Different Patient", add_another_appointment_diff_patient, empty_dict),
    "3": ("Section Menu", appointments_section_menu, empty_dict)
}

appointment_made_final_actions = {
    "title": "NEXT ACTIONS",
    "type": "sub",
    "1": ("Add Another Appointment For This Patient", add_another_appointment_same_patient, empty_dict),
    "2": ("Add Appointment For Another Patient", add_another_appointment_diff_patient, empty_dict),
    "3": ("Section Menu", appointments_section_menu, empty_dict)
}


manage_appointment_flow = {
    "title": "MANAGE APPOINTMENTS",
    "type": "sub",
    "1": ("View Appointments", empty_method, view_appointment_flow),
    "2": ("Add a New Appointment", add_appointment, appointment_made_final_actions),
    "3": ("Delete Upcoming Appointments", empty_method, delete_appointment_flow)
}

###### VIEW APPOINTMENT RECORDS SUB-MENU ######

records_final_menu = {
    "title": "NEXT ACTIONS",
    "type": "sub",
    "1": ("View a Different Appointment", another_record_same_patient, empty_dict),
    "2": ("View a Different Patient", another_record_diff_patient, empty_dict),
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
    "6":("View Appointment Summaries", records_main, records_final_menu)
}


############################# TESTING ###############################

if __name__ == '__main__':
    utils.display(main_flow_admin)
    pass
    