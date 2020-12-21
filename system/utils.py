# Utility functions

from pathlib import Path
import os
import sys
import sqlite3
import hashlib
import pandas as pd
import datetime as dt
from system import asciiart

# Change python path for imports
p = Path(__file__).parents[1]
sys.path.insert(1, str(p))

# import register, patient, gp & admin main dictionaries
from user_menu_flow.patient_flow import main_flow_patient
from user_menu_flow.gp_flow import main_flow_gp
from user_menu_flow.admin_flow import main_flow_admin
from user_menu_flow.register_login_flow import main_flow_register

# import method to automatically allocate patient to gp with fewest patients
from classes.patient import Patient

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


class InvalidCharacterError(Error):
    """Raised when user inputs "'" or '"' to avoid SQL injections."""
    pass


class EmailFormatError(Error):
    """Raised when incorrectly formatted email address."""
    pass

class DuplicateEmailError(Error):
    """Raised when email has already been used in an account."""
    pass

class DateFormatError(Error):
    """Raised when date (YYYY-MM-DD) is not correctly formatted."""
    pass


# User is logged in if it has both type and id
def logged():
    """Check whether user is logged in or not."""
    return True if globals.usr_type in ("patient", "gp", "admin") else False


def logout():
    """Logout user and return to main page."""
    globals.usr_type = ""
    globals.usr_id = ""
    print("\n\U00002705 Succesfully logged out.")


# Display function for menu
def display(my_dict):
    '''
    Display function called to display menu and run the 
    functions corresponding to the user's choice.
    '''
    line = '-' * 52
    # TODO: use - * n  
    print("\n" + line + "\n"
          "                ", my_dict["title"], "\n")

    # automatically direct to next flow
    if my_dict["type"] == "auto":
        return my_dict["next"][0](my_dict["next"][1])

    # Print user choices
    for key in my_dict:
        if key not in ("title", "type"):
            print("[", key, "] " + my_dict[key][0])

    # Print "return main page" option if not on a main page
    if my_dict["type"] != "main":
        print("[ # ] Go back to main page")

    # Print "logout" option if logged in
    if logged():
        print("[ X ] Logout")

    else:
        # print "exit" option
        print("[ E ] Exit the system")

    # User input 
    usr_choice = input("\n--> ")

    # If "go back to main page"
    if usr_choice == '#':

        if globals.usr_type == "patient":
            return display(main_flow_patient)

        elif globals.usr_type == "gp":
            return display(main_flow_gp)

        elif globals.usr_type == "admin":
            return display(main_flow_admin)

        else:
            return display(main_flow_register)

    # If "Logout"
    elif usr_choice in ('X', 'x'):
        logout()
        return display(main_flow_register)

    # If user selected one of the options
    elif usr_choice in my_dict:
        return my_dict[usr_choice][1](my_dict[usr_choice][2])

    elif usr_choice in ('E', 'e'):
        print(
            # TODO: use - * n 
            "\n" + line + "\n" + "\n\U0001F51A Thanks for using e-health. Goodbye!")
        print(asciiart.exit_art)
        sys.exit()

    # TODO: add help function
    elif usr_choice in ('H', 'h'):
        pass

    # If invalid entry
    else:
        print("\n\U00002757 Invalid entry, please try again")
        return display(my_dict)


def hash_salt(password):
    """
    Hash and salt passwords.
    """

    salt = os.urandom(32) 

    hash_key = hashlib.pbkdf2_hmac(
        'sha256', 
        password.encode('utf-8'), 
        salt, 
        100000
    )

    hash_salt = (salt + hash_key).hex()

    return hash_salt


def validate(user_input):
    """
    Validate user input.  
    
    Custom errors:
        - Empty field
        - Input too long (> 50 chars) 
        - Does not contain "'" or '"' to avoid SQL injections
    """
    # NOTE: This func could be used as decorator
    try:
        if user_input == '':
            raise EmptyError
        elif len(user_input) > 50:
            raise LenghtError
        elif ('"' in user_input) or ("'" in user_input):
            raise InvalidCharacterError
    except InvalidCharacterError:
        print("\U00002757 Invalid character: ' and \" are not accepted.")
        return False
    except EmptyError:
        print("\U00002757 You need to input a value.")
        return False
    except LenghtError:
        print("\U00002757 Input is too long.")
        return False
    return True


def validate_email(user_input):
    """
    Validate user input for email address.  
    
    Custom errors:
        - Not empty field
        - Must contain '@' symbol
        - Not unique email address
        - Does not contain "'" or '"' to avoid SQL injections
    """
    # NOTE: This func could be used as decorator
    email_query = 'SELECT patient_email FROM patient'
    emails = db_read_query(email_query)   

    try:
        if user_input == '':
            raise EmptyError
        elif '@' not in user_input:
            raise EmailFormatError
        #elif emails['patient_email'].str.contains(user_input).any():
        #    raise DuplicateEmailError
        elif ('"' in user_input) or ("'" in user_input):
            raise InvalidCharacterError
    except InvalidCharacterError:
        print("\U00002757 Invalid character: ' and \" are not accepted.")
        return False
    except EmptyError:
        print("\U00002757 You need to input a value.")
        return False
    except DuplicateEmailError:
        print("\U00002757 Email address already in use.")
        return False
    except EmailFormatError:
        print("\U00002757 Incorrectly formatted email address.")
        return False
    return True


def validate_password(user_input):
    """
    Validate user input for password.  

    Custom errors:
        - Empty field
        - Input too short (< 8 chars)
        - Does not contain "'" or '"' to avoid SQL injections
    """
    # NOTE: This func could be used as decorator
    try:
        if user_input == '':
            raise EmptyError
        elif len(user_input) < 8:
            raise LenghtError
        elif ('"' in user_input) or ("'" in user_input):
            raise InvalidCharacterError
    except InvalidCharacterError:
        print("\U00002757 Invalid character: ' and \" are not accepted.")
        return False
    except EmptyError:
        print("\U00002757 You need to input a value.")
        return False
    except LenghtError:
        print("\U00002757 Input is too short, password must be 8 characters long minimum.")
        return False
    return True


def validate_date(user_input):
    """
    Validate user input for date such as DOB.  
    
    Custom errors:
        - Empty field
        - Does not contain "'" or '"' to avoid SQL injections
        - Date must be in format YYYY-MM-DD
    """
    # NOTE: This func could be used as decorator
    try:
        if user_input == '':
            raise EmptyError
        elif ('"' in user_input) or ("'" in user_input):
            raise InvalidCharacterError
        elif ((len(user_input) != 10) or
              (user_input[4] != '-') or
              (user_input[7] != '-')):
            raise DateFormatError

        int(user_input[:4])
        int(user_input[5:7])
        int(user_input[8:])

        # NOTE: is there a built-in func for data validation?
        if int(user_input[5:7]) > 12 or int(user_input[8:]) > 31:
            raise DateFormatError

    except InvalidCharacterError:
        print("\U00002757 Invalid character: ' and \" are not accepted.")
        return False
    except EmptyError:
        print("\U00002757 You need to input a value.")
        return False
    except DateFormatError:
        print("\U00002757 Incorrectly formatted date, must be in format YYYY-MM-DD.")
        return False
    except ValueError:
        print("\U00002757 Incorrectly formatted date, must be in format YYYY-MM-DD.")
        return False

    return True

def get_start_date():
    print("Please enter the date (YYYY-MM-DD) from which\n" 
          "you want to diplay availibility\n\n"
          "Enter 'T' to see availibility from today")
    start_date = input("\n--> ")
    valid = False
    while valid == False:
        if start_date in ("T","t"): 
            valid = True
            start_date = dt.date.today().isoformat()
            return start_date
        elif validate_date(start_date):
            if dt.date.fromisoformat(start_date) > dt.date.today():
                valid = True
                return start_date
            else:
                print("\n\U00002757 Schedule date cannot be earlier than today.")
        else:
            print("\n\U00002757 Invalid entry, please try again")
        if valid == False:
            start_date = input("\n--> ")


def login(user_email, password, usr_type):
    """Check login credentials."""

    # u = (user_email,)
    conn = sqlite3.connect("database/db_comp0066.db")
    c = conn.cursor()

    sql_hash_salt = 'SELECT ' + usr_type + '_password FROM ' + usr_type + ' WHERE ' + usr_type + '_email=' + "'" + user_email + "'"
    c.execute(sql_hash_salt)

    # Get the full hash + salt from db
    # [0] is necessary or we will have a tuple instead of a string
    hash_salt = c.fetchone()[0]

    # Split hash and salt | len(salt) = 64 since hex byte is used
    salt = hash_salt[:64]
    hash_key = hash_salt[64:]

    # Hash and salt password to check (using same parameters)
    hash_key_to_check = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'), 
        bytes.fromhex(salt),
        100000
    ).hex()

    # Get new key 
    # hash_key_to_check = hash_salt_to_check[32:]

    ########################## DEBUG ##########################
    # print('input_password: ', password)                     #
    # print("hash_salt: ", hash_salt)                         #
    # print('salt: ', salt)                                   #
    # print('salt hex bytes: ', bytes.fromhex(salt))          #
    # print('hash_key_in_datab: ', hash_key)                  #
    # print('hash_key_to_check: ',      hash_key_to_check)    # 
    ########################## DEBUG ##########################

    # Check if new key matches our stored key
    if hash_key_to_check == hash_key:
        sql_id = 'SELECT ' + usr_type + '_id FROM ' + usr_type + ' WHERE ' + usr_type + '_email=' + "'" + user_email + "'"
        c.execute(sql_id)
        usr_id = c.fetchone()[0]
        globals.usr_type = usr_type
        globals.usr_id = usr_id
        conn.close()
        return True
        # else:
        #     conn.close()
        #     return False
    else:
        conn.close()
        return False


def register(first_name, last_name, gender, birth_date, 
            email, password, blood_donor, organ_donor):        
    """
    Register a new user by inserting user inputs / default values in database.
    
    Assumes inputs already validated and sanitized.  

    Values inserted: 
        - GP ID                     [Default: GP with fewest patients]
        - First name                
        - Last name                 
        - Gender                    
        - Birth date                
        - Email address
        - Password                  
        - Registration date         [Default: now]
        - Blood donor status
        - Organ donor status 
        - Patient status            [Default: pending]
    
    """

    gp_id_default = '0'
    reg_date = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    default_status = 'pending'
    hash_salt_pw = hash_salt(password)

    # Insert into patient table
    query = """INSERT INTO patient
            VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"""
    conn = sqlite3.connect('database/db_comp0066.db')
    c = conn.cursor()
    c.execute(query, 
                    (gp_id_default,
                    first_name,
                    last_name,
                    gender,
                    birth_date,
                    email,
                    hash_salt_pw,
                    reg_date,
                    blood_donor,
                    organ_donor,
                    default_status))

    # Assign GP using newly created patient_id
    patient_id = c.lastrowid 
    conn.commit()
    conn.close()

    print(patient_id)
    Patient.change_gp('auto', patient_id)    

    print("OK.")

    # Return boolean to use in user flow 
    return True


def user_type(user_id):
    """Print user type of a specified user."""
    u = (user_id,)

    conn = sqlite3.connect("database/db_comp0066.db")
    c = conn.cursor()
    c.execute('SELECT type FROM users WHERE user_id=?;', u)

    print(c.fetchone())

    conn.close()


def help():
    """ Help user understand and navigate the program."""
    # pass
    pass


def export():
    """ Export content of the page in .csv """
    # NOTE: advanced feature
    pass


def day_empty_df(date, gp_id):
    times = pd.date_range(start='08:00', periods=54, freq='10Min').strftime('%H:%M')
    date = pd.date_range(start=date, periods=1, freq='D')
    day_df = pd.DataFrame(index=times, columns=date.date)

    # Handling lunch time
    if (gp_id % 2) == 0:
        day_df.loc['12:00':'12:50'] = 'LUNCH'
    else:
        day_df.loc['13:00':'13:50'] = 'LUNCH'

    # Handling Working Days
    working_day_query = """SELECT gp_working_days FROM gp where gp_id == {};""".format(gp_id)
    working_day = db_read_query(working_day_query).loc[
        0, 'gp_working_days']  # will need a query to pull the first working day for a specific GP

    # This part of the code works out when the GP has weekends and populates those days with status "Weekend"
    weekend_day_range = [(working_day + 5) % 7, (working_day + 6) % 7]

    if day_df.columns[0].weekday() in weekend_day_range:
        day_df[day_df.columns[0]] = 'WEEKEND'

    # Make df pretty
    day_df.columns.values[0] = "Status"
    day_df = day_df.fillna("")

    return day_df


def week_empty_df(start_date, gp_id):
    days = pd.date_range(start=start_date, periods=7, freq='D')
    times = pd.date_range(start='08:00:00', periods=54, freq='10Min')  # .to_frame(name='Working Hours',index=False)
    week_df = pd.DataFrame(index=times.strftime('%H:%M'), columns=days.date)

    working_day_query = """SELECT gp_working_days FROM gp where gp_id == {};""".format(gp_id)
    working_day = db_read_query(working_day_query).loc[
        0, 'gp_working_days']  # will need a query to pull the first working day for a specific GP

    # This part of the code works out when the GP has weekends and populates those days with status "Weekend"
    weekend_day_range = [(working_day + 5) % 7, (working_day + 6) % 7]

    # Inserting 'Lunch Time'
    if (gp_id % 2) == 0:
        week_df.loc['12:00':'12:50'] = 'LUNCH'
    else:
        week_df.loc['13:00':'13:50'] = 'LUNCH'

    # Inserting 'Weekend'
    for i in range(7):
        if week_df.columns[i].weekday() in weekend_day_range:
            week_df[week_df.columns[i]] = 'WEEKEND'

    week_df = week_df.fillna(" ")

    return week_df

# This function accepts an SQL query as an input and then commits the changes into the DB
def db_execute(query):
    conn = sqlite3.connect('database/db_comp0066.db')
    c = conn.cursor()
    c.execute(query)
    conn.commit()
    conn.close()


# This function accepts an SQL query as an input and then returns the DF produced by the DB
def db_read_query(query):
    conn = sqlite3.connect("database/db_comp0066.db")
    result = pd.read_sql_query(query, conn)
    conn.close()
    return result