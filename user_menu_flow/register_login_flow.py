# register_login_flow.py

# library imports 
from pathlib import Path
import sys 

# Change python path for imports
p = Path(__file__).parents[1]
sys.path.insert(1, str(p))

# Importing utility methods from the 'system' package
from system import utils

# Importing menu paths for each user from the 'user_menu_flow' package
from user_menu_flow import gp_flow, patient_flow

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

# TODO: Error handling, input validation and call corresponding register() function instead of hardcoding
def login_page(login_as):
    '''
    Function defining the user login page takes an empty 
    dictionary as argument for utils.display function consistency.
    '''
    print("\n---------------------------------------------------- \n"
          "                    LOGIN\n"
          "\nPlease, enter your credentials:"
          "\n  - enter '#' to go back to main page")


    login_credentials = ["Email address", "Password"]
    usr_input = ["",""]

    for i in (0,1):
        usr_input[i] = input("\n--> ", login_credentials[i]  ,": ")
        
        if (usr_input[i] == '#'):
            return utils.display(main_flow_register)

        utils.validate(usr_input[i])

    # Hardcoded for now
    #########################
    success = True
    ########################

    if (success == False):

        print("\nInvalid credentials, please try again.")
        return login_page(login_as)
    
    else:
        print("\nSuccessful login !")
        
        # Hardcoded for now
        #########################
        globals.usr_type,globals.usr_id = login_as, 3
        #########################

        if (globals.usr_type == 'patient'):
            return utils.display(patient_flow.main_flow_patient)

        elif (globals.usr_type == 'gp'):
            return utils.display(gp_flow.main_flow_gp)

        else:
            return utils.display(admin_flow.main_flow_admin)


# TODO: Error handling, input validation and call corresponding register() function instead of hardcoding
def register_page(next_dict):
    '''
    Function defining the user register page, takes an empty 
    dictionary as argument for utils.display function consistency.
    '''
    print("\n---------------------------------------------------- \n"
        "                   REGISTER\n"
        "\nPlease, fill in the following form:"
        "\n(enter '#' to go back to main page)")

    usr_details=["First name","Last name", "Email address"]
    usr_input=[]

    for i in usr_details:
        single_input = input("\n--> " + i + ": ")

        if single_input == "#" :
            return utils.display(main_flow_register)

        else:
            usr_input.append(single_input)
    
    # Hardcoded for now
    ###########################
    success = False
    ###########################

    if (success == True):
        print("\nInvalid entry, please try again.")
        return register_page(next_dict)

    else :
        print("\nYour registration must now be approved. \nYou will have to wait for a moment before being able to login.")
        return utils.display(main_flow_register)


########################## MENU NAVIGATION DICTIONARY ######################

# Empty nested dictionary to store in tuple for last menu
# before going back to main page (for display function return parameter).
empty_dict = {"title": "CHANGES SAVED",
              "type":"sub"}


# "Login as ?"" page dictionary
flow_1 = {"title":"LOGIN AS ?",
          "type":"sub",
          "1":("Patient",login_page,"patient"),
          "2":("GP",login_page,"gp"),
          "3":("Admin",login_page,"admin")}


# login home page dictionary
main_flow_register = {"title":"\N{hospital} WELCOME to e-health!",
                      "type":"main",
                      "1":("Login",empty_method,flow_1),
                      "2":("Register",register_page,empty_dict)}