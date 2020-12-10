# Utility functions

from pathlib import Path
import sys 
import sqlite3
import datetime

# Change python path for imports
p = Path(__file__).parents[1]
sys.path.insert(1, str(p))

# Import global variables from globals.py
from system import globals

# Custom errors
class Error(Exception):
    pass

class EmptyError(Error):
    """Raised when input is empty."""
    pass

class LenghtError(Error):
    """Raised when input is too long."""
    pass

# Display function for menu
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


# User is logged in if it has both type and id
def logged():
    """Check whether user is logged in or not.""" 
    return True if globals.usr_type in ("patient","gp","admin") else False 

def validate(user_input):
    """
    Validate user input.  
    
    Custom errors:
        - Empty field
        - Input too long (> 15 chars)
    """
    # NOTE: This func could be used as decorator
    try:
        if user_input == '':
            raise EmptyError
        elif len(user_input) > 15:
            raise LenghtError
    except EmptyError:
        print("You need to input a value.")
    except LenghtError:
        print("Input is too long.")

def login(username, password):
    """Check login credentials."""
    # query db for username and pw 
    # assign username to global var 
    pass

def logout():
    """Logout user and return to main page."""
    globals.usr_type = ""
    globals.usr_id = ""
    return display(register_login_flow.main_flow)

def register(first_name, last_name, gender, birth_date, email, pw, type):
    # TODO: update using real args + patient_id / gp_id
    """
    Register a new user by inserting user inputs in database.
    
    Assumes inputs already validated and sanitized.  

    Arguments included 
        - First name                
        - Last name                 
        - Gender                    
        - Birth date                
        - Email address
        - Password (TODO: hash)
        - Registration date         [default: now]
        - User type 
    
    """
    # Create connection to db
    conn = sqlite3.connect('config/db_comp0066.db')

    # Create cursor
    c = conn.cursor()

    # Insert into user
    c.execute("""
        INSERT INTO
            users (
            user_first_name,
            user_last_name,
            user_gender,
            user_birth_date,
            user_email,
            user_password,
            user_registration_date,
            user_type)
        VALUES
            (first_name,
            last_name,
            gender,
            birth_date,
            email,
            pw,
            datetime('now'),
            type);
    """)

    # Commit to db
    conn.commit()

    # Output message
    print("""Successfully registered. 
        You can login using your email %s and password.""" % email )

    # Close db
    conn.close()

def user_type(user_id):
    """Print user type of a specified user."""
    t = (user_id, )

    conn = sqlite3.connect("config/db_comp0066.db")
    c = conn.cursor()
    c.execute('SELECT type FROM users WHERE user_id=?;', t)

    print(c.fetchone())

    conn.close()

def select():
    """ Select options from menu."""
    pass

def help():
    """ Help user understand and navigate the program."""
    # pass
    pass

def update():
    """ Update specified values. """
    # pass
    pass

def export():
    """ Export content of the page in .csv """
    # NOTE: advanced feature
    pass

def sqlhelper():
    # NOTE: in separate file?
    pass