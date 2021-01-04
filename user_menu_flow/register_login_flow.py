# register_login_flow.py

# library imports 
from pathlib import Path
from datetime import date
import sys 

# Change python path for imports
p = Path(__file__).parents[1]
sys.path.insert(1, str(p))

# Importing utility methods from the 'system' package
from system import utils
from system import asciiart

# Importing menu paths for each user from the 'user_menu_flow' package
from user_menu_flow import gp_flow, patient_flow, admin_flow

# import global variables from globals.py
from system import globals


############################ SEQUENTIAL STEPS MENUS ########################

def empty_method(next_dict):
    '''
    Empty method to be stored in the tuple of the dictionary of the user 
    choice doesn't require any specific steps and just redirects 
    '''
    return utils.display(next_dict)

################################ INPUT MENU PAGES ###########################

def reset_password(login_as):
    '''
    Method defining the 'Reset Password' page, called from login_page(), for users that have forgotten their password.

    Parameter:
        - login_as: user type the user is trying to login as selected on previous menu page.
    '''

    print("\n---------------------------------------------------- \n"
          "                    RESET PASSWORD\n"
          "\nPlease, enter your email address"
          "\nor '#' to go back to main page")
    
    # user input for email address
    user_email = input("\n--> Email address: ")

    # while user input has not been validated
    validate = False
    while validate != True:

        # If user want to go back to main menu
        if user_email == '#':
            return utils.display(main_flow_register)

        # if user input for email is validated
        elif utils.validate(user_email):
            validate = True

            # generate a random string 
            random_string_password_reset = utils.random_string(8)

            email_sent, message = utils.send_code_to_registered_user(login_as, user_email, random_string_password_reset)

            if email_sent == False:
                print("\n\U00002757 " + message)
                validate = False
                user_email = input("\n--> Email address: ")

            else:
                print("\n\U00002705 " + message)

        # if invalid entry
        else:
             user_email = input("\n--> Email address: ")
    
    print(utils.change_password(login_as, user_email, random_string_password_reset)[1])
    
    return utils.display(main_flow_register)

def login_page(login_as):
    '''
    Function defining the user login page.

    Parameter:
        - login_as: user type the user is trying to login as selected on previous menu page.
    '''
    print("\n---------------------------------------------------- \n"
          "                    LOGIN\n"
          "\nPlease, enter your credentials"
          "\n\nEnter '#' to go back to main page"
          "\nEnter 'R' to reset your password")

    # Login details
    login_credentials = ["Email address", "Password"]
    usr_input = []

    # Login input entries
    i = 0
    while i < len(login_credentials):
        single_input = input("\n--> " + login_credentials[i] + ": ")
        
        # Go back to main registration page
        if single_input == '#':
            return utils.display(main_flow_register)

        # If user want to reset his password
        elif single_input in ('R','r'):
            reset_password(login_as)

        # Input validation for email
        elif (login_credentials[i] == "Email address") and (utils.validate(single_input)):
            usr_input.append(single_input)
        # Input validation for password
        elif (login_credentials[i] == "Password") and (utils.validate(single_input)):
            usr_input.append(single_input)

        # If invalid input
        else :
            i -= 1
        
        i += 1

    # Calling the login() method to check user input against database
    # Returns boolean variable (True = valid credentials; False = invalid credentials)
    success, status = utils.login(usr_input[0],usr_input[1],login_as)
    
    # Invalid login credentials
    if success == False:
        print("\n\U00002757 Invalid email or password, please try again.")
        return login_page(login_as)
    
    elif status != "confirmed":
        print("\n\U00002757 Please wait for your account to be confirmed before login.")
        return login_page(login_as)
    
    # Valid login credentials
    else:
        print("\n\U00002705 Successful login !")

        # Redirects to patient main page 
        if (globals.usr_type == 'patient'):
            return utils.display(patient_flow.main_flow_patient)

        # Redirects to gp main page 
        elif (globals.usr_type == 'gp'):
            return utils.display(gp_flow.main_flow_gp)

        # Redirects to admin main page 
        else:
            return utils.display(admin_flow.main_flow_admin)


def register_page(next_dict):
    '''
    Function defining the user register page, takes an empty 
    dictionary as argument for utils.display function consistency.
    '''
    print("\n---------------------------------------------------- \n"
        "                   REGISTER\n"
        "\nPlease, fill in the following form"
        "\nor enter '#' to go back to main page")

    # register gender dictionary
    gender = {"title": "Gender",
              "1":"male",
              "2":"female",
              "3":"non binary",
              "4":"prefer not to say"}
    
    # register NHS blood donor dictionary
    blood_donor = {"title": "NHS Blood donor",
                   "1":"yes",
                   "2":"no"}

    # register NHS blood donor dictionary
    organ_donor = {"title": "NHS Organ donor",
                   "1":"yes",
                   "2":"no"}

    # Registration details
    usr_details=["First name", "Last name", "Birth date (YYYY-MM-DD)", 
                "Email address", "Password (8 characters min)", "Gender", 
                "NHS blood donor", "NHS organ donor"]

    MCQ_details_dict = [gender,blood_donor,organ_donor]
    
    # First name, last name, birth date, email, password, gender, blood, organs 
    usr_input=[]
    
    # Registration String entries
    i = 0
    while i < len(usr_details) - 3:
        single_input = input("\n--> " + usr_details[i] + ": ")
        
        # Go back to mian registration page 
        if (single_input == '#'):
            return utils.display(main_flow_register)

        # Input validation for name
        elif (usr_details[i] in ("First name", "Last name")) and utils.validate_name(single_input):
            usr_input.append(single_input)

        # Input validation for email
        elif (usr_details[i] == "Email address") and utils.validate_email(single_input):
            usr_input.append(single_input)

        # Input validation for password 
        elif (usr_details[i] == "Birth date (YYYY-MM-DD)") and utils.validate_date(single_input):

            if date.fromisoformat(single_input) < date.today():
                usr_input.append(single_input)

            else:
                print("\U00002757 Birth date must be in the past.")
                i -= 1

        # Input validation for the other registration details
        elif (usr_details[i] not in ("First name", "Last name", "Email address", "Password (8 characters min)", "Birth date (YYYY-MM-DD)")) and utils.validate(single_input):
            usr_input.append(single_input)

        # Input validation for password 
        elif (usr_details[i] == "Password (8 characters min)") and utils.validate_password(single_input):
            
            password_confirmation = input("\n--> Confirm password: ")
            
            if single_input == password_confirmation:
                usr_input.append(single_input)

            else:
                print("\n\U00002757 Passwords do not match, please enter password again")
                i -= 1

        # If invalid input
        else :
            i -= 1
        
        i += 1

    # Registration MCQ entries
    i = 0
    while i < len(MCQ_details_dict):
        print("\n------------------")
        print(MCQ_details_dict[i]["title"])

        # Print user options and corresponding keys
        for key in MCQ_details_dict[i]:
            if key != "title":
                print("  [", key, "] " + MCQ_details_dict[i][key])

        # User input 
        usr_choice = input("\n--> ") 

        # If valid input, store in usr_input
        if usr_choice in MCQ_details_dict[i]:
            usr_input.append(MCQ_details_dict[i][usr_choice])

        # If invalid input
        else:
            print("\n\U00002757 Invalid entry, please try again")
            i -= 1
        
        i += 1
    
    # Updating DB with new patient account
    success = utils.register(usr_input[0], usr_input[1], usr_input[5], usr_input[2], 
                             usr_input[3], usr_input[4], usr_input[6], usr_input[7])

    # If problem with registration
    if (success == False):
        print("\n\U00002757 Your registration could not be completed due to an unknown issue.")
        return register_page(next_dict)

    # If registration successful
    else :
        print("\n\U00002705 Your registration must now be approved. \nYou will have to wait for a moment before being able to login.")
        return utils.display(main_flow_register)


########################## MENU NAVIGATION DICTIONARY ######################

# Empty nested dictionary to store in tuple for last menu
# before going back to main page (for display function return parameter).
empty_dict = {"title": "CONTINUE E-HEALTH OR LOGOUT ?",
              "type":"sub"}


# "Login as ?"" page dictionary
flow_1 = {"title":"LOGIN AS ?",
          "type":"sub",
          "1":("Patient",login_page,"patient"),
          "2":("GP",login_page,"gp"),
          "3":("Admin",login_page,"admin")}


# login home page dictionary
main_flow_register = {"title":"{}\n                     \U0001F3E5 WELCOME TO E-HEALTH! \n\n\U00002757 Open your terminal in full screen for a better user experience \U00002757".format(asciiart.launch_art),
                      "type":"main",
                      "1":("Login",empty_method,flow_1),
                      "2":("Register as a patient",register_page,empty_dict)}