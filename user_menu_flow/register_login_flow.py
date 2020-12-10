# register_login_flow.py

# library imports 
from pathlib import Path
import sys 

# Change python path for imports
p = Path(__file__).parents[1]
sys.path.insert(1, str(p))

# Importing utility methods from the 'system' package
from system.utils import login, register, display

# Importing menu paths for each user from the 'user_menu_flow' package
from user_menu_flow import gp_flow, admin_flow, patient_flow

# import global variables from globals.py
from system import globals


################################ INPUT MENU PAGES ###########################

def login_page(next_dict):
    '''
    Function defining the user login page takes an empty 
    dictionary as argument for utils.display function consistency.
    '''
    print("\n---------------------------------------------------- \n"
          "                    LOGIN\n"
          "\nPlease, enter your credentials:"
          "\n(enter '#' to go back to main page)")

    email = input("\n--> Email address: ")

    if (email == '#'):
        return display(main_flow)

    password = input("\n--> Password: ")

    if (password == '#'):
        return display(main_flow)

    # Hardcoded for now
    #########################
    (success,usr_type,usr_id) = (True,"patient",3)
    ########################

    if (success == False):

        print("\nInvalid credentials, please try again.")
        return login_page(next_dict)
    
    else:
        print("\nSuccessful login !")

        if (usr_type == 'patient'):
            return display(patient_flow.main_flow)

        elif (usr_type == 'gp'):
            return display(gp_flow.main_flow)

        else:
            return display(admin_flow.main_flow)



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
            return display(main_flow)

        else:
            usr_input.append(single_input)
    
    # Hardcoded for now
    ###########################
    (success,usr_type,usr_id) = (True,"patient",3)
    ###########################

    if (success == False):

        print("\nInvalid entry, please try again.")
        return register_page(next_dict)

    else :
        print("\nSuccessfully registered !")
        return display(patient_flow.main_flow)



########################## MENU NAVIGATION DICTIONARY ######################

# No further menu after login and register, so store empty nested 
# dictionary for display function return parameter
empty_dict = {}


# login home page dictionary
main_flow = {"title":"WELCOME",
             "type":"main",
             "1":("Login",login_page,empty_dict),
             "2":("Register",register_page,empty_dict)}