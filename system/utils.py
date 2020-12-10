# Notes for util funcs

# imports
from pathlib import Path
import sys 

# Change python path for imports
p = Path(__file__).parents[1]
sys.path.insert(1, str(p))

# import global variables from globals.py
from system import globals


def display(dict):
    '''
    Display function called to display menu and run the 
    functions corresponding to the user's choice.
    '''

    print("\n----------------------------------------------------\n"
            "                ", dict["title"], "\n")

    # Print user choices
    for key in dict:
        if key not in ("title","type"):
            print("[",key,"] " + dict[key][0])
    
    # Print "return main page" option if not on a main page
    if dict["type"] != "main":
        print("[ # ] Go back to main page")

    # Print "logout" option if logged in
    if globals.usr_type in ("patient","gp","admin"):
        print("[ X ] Logout")

    # User input 
    usr_choice = input("\n--> ")

    # If "go back to main page"
    if usr_choice == '#':
        
        if globals.usr_type == "patient": 
            return display(patient_flow.main_flow)
            
        elif globals.usr_type == "gp" :
            return display(gp_flow.main_flow)

        elif globals.usr_type == "admin":
            return display(admin_flow.main_flow)

        else:
            return display(register_login_flow.main_flow)

    # If "Logout"
    elif usr_choice in ('X','x'):
        globals.usr_type = ""
        globals.usr_id = ""
        return display(register_login_flow.main_flow)

    # If user selected one of the options
    elif usr_choice in dict:
        return dict[usr_choice][1](dict[usr_choice][2])

    # If invalid entry
    else:
        print("\nInvalid entry, please try again.")
        return display(dict)


def logged():
    """Check whether user is logged in or not.""" 
    # Z: decorator
    pass

def validate():
    # decorator
    """Validate user input."""
    pass

def login(username, password):
    """Check login credentials."""
    # exception for empty > prompt
    # if not empty, query db for pw 
    # if match, login | else, message > prompt
    # assign username to global var 
    pass

def logout(username):
    """Logout user."""
    # empty global username var
    # reset user_status
    pass

def register():
    """Register a new user."""
    # pass
    pass

def check():
    """Check user type."""
    pass

def select():
    """ Select options from menu."""
    pass

def help():
    """ Help user understand and navigate the program."""
    # pass
    pass

def update():
    # pass
    pass

def export():
    # pass
    pass

def sqlhelper():
    # pass
    pass