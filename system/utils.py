# Utility functions

from pathlib import Path
import sys
import sqlite3
import pandas as pd
import datetime

# Change python path for imports
p = Path(__file__).parents[1]
sys.path.insert(1, str(p))

# import register, patient, gp & admin main dictionaries
from user_menu_flow.patient_flow import main_flow_patient
from user_menu_flow.gp_flow import main_flow_gp
from user_menu_flow.admin_flow import main_flow_admin
from user_menu_flow.register_login_flow import main_flow_register

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


# User is logged in if it has both type and id
def logged():
    """Check whether user is logged in or not."""
    return True if globals.usr_type in ("patient", "gp", "admin") else False


def logout():
    """Logout user and return to main page."""
    globals.usr_type = ""
    globals.usr_id = ""


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
        if key not in ("title", "type"):
            print("[", key, "] " + dict[key][0])

    # Print "return main page" option if not on a main page
    if dict["type"] != "main":
        print("[ # ] Go back to main page")

    # Print "logout" option if logged in
    if logged():
        print("[ X ] Logout")

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
    elif usr_choice in dict:
        return dict[usr_choice][1](dict[usr_choice][2])

    elif usr_choice in ('E', 'e'):
        print("\U0001F51A Thanks for using e-health. Goodbye! ")
        sys.exit()
    
    # TODO: guidance option

    # If invalid entry
    else:
        print("\n \U00002757 Invalid entry, please try again")
        return display(dict)


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


def login(user_id, password):
    # TODO: generalize to all user types
    """Check login credentials."""

    u = (user_id,)

    conn = sqlite3.connect("config/db_comp0066.db")
    c = conn.cursor()
    c.execute('SELECT pw_hash FROM users WHERE user_id=?;', u)

    pw_hash = c.fetchone()

    conn.close()

    # TODO: apply hashing - assign usr_type - go to next page in menu flow
    if pw_hash == password:
        print("Login successful.")
        globals.usr_id = user_id
        return True
    else:
        print("Login failed.")
        return False


def register(first_name, last_name, gender, birth_date, email, pw, type):
    # TODO: update using real args - patient_id / gp_id - next page
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
        You can now login using your email %s and password.""" % email)

    # Close db
    conn.close()


def user_type(user_id):
    """Print user type of a specified user."""
    u = (user_id,)

    conn = sqlite3.connect("config/db_comp0066.db")
    c = conn.cursor()
    c.execute('SELECT type FROM users WHERE user_id=?;', u)

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


def day_empty_df(date, gp_id):
    times = pd.date_range(start='08:00', periods=54, freq='10Min').strftime('%H:%M')
    date = pd.date_range(start=date, periods=1, freq='D')
    day_df = pd.DataFrame(index=times, columns=date.date)

    # Handling Working Days
    working_day_query = """SELECT gp_working_days FROM gp where gp_id == {};""".format(gp_id)
    working_day = db_read_query(working_day_query).loc[
        0, 'gp_working_days']  # will need a query to pull the first working day for a specific GP

    # This part of the code works out when the GP has weekends and populates those days with status "Weekend"
    weekend_day_range = [(working_day + 5) % 7, (working_day + 6) % 7]

    if day_df.columns[0].weekday() in weekend_day_range:
        day_df[day_df.columns[0]] = 'Weekend'

    # Handling lunch time
    # even gp_id 12:00 to 13:00, odd gp_id 13:00 to 14:00
    if (gp_id % 2) == 0 and day_df[date.date].isnull().values.any() == True:
        day_df.loc['12:00':'12:50'] = 'Lunch Time'
    elif (gp_id % 2) != 0 and day_df[date.date].isnull().values.any() == True:
        day_df.loc['13:00':'13:50'] = 'Lunch Time'

    return day_df.fillna(" ")

def week_empty_df(start_date, gp_id):
    days = pd.date_range(start=start_date, periods=7, freq='D')
    times = pd.date_range(start='08:00:00', periods=54, freq='10Min')  # .to_frame(name='Working Hours',index=False)
    week_df = pd.DataFrame(index=times.strftime('%H:%M'), columns=days.date)

    working_day_query = """SELECT gp_working_days FROM gp where gp_id == {};""".format(gp_id)
    working_day = db_read_query(working_day_query).loc[
        0, 'gp_working_days']  # will need a query to pull the first working day for a specific GP

    # This part of the code works out when the GP has weekends and populates those days with status "Weekend"
    weekend_day_range = [(working_day + 5) % 7, (working_day + 6) % 7]

    for i in range(7):
        if week_df.columns[i].weekday() in weekend_day_range:
            week_df[week_df.columns[i]] = 'Weekend'

    # Handling lunch time
    if (gp_id % 2) == 0:
        week_df.loc[dt.datetime.strptime('12:00','%H:%M').strftime('%H:%M')
                    :dt.datetime.strptime('12:50','%H:%M').strftime('%H:%M')] = 'Lunch Time'
    elif (gp_id % 2) != 0:
        week_df.loc[dt.datetime.strptime('13:00', '%H:%M').strftime('%H:%M')
                    :dt.datetime.strptime('13:50', '%H:%M').strftime('%H:%M')] = 'Lunch Time'

    return week_df.fillna(" ")


# This function accepts an SQL query as an input and then commits the changes into the DB
def db_execute(query):
    conn = sqlite3.connect('database/db_comp0066.db')
    c = conn.cursor()
    c.execute(query)
    # Commit to db
    conn.commit()
    # print("Info successfully committed")
    # Close db
    conn.close()


# This function accepts an SQL query as an input and then returns the DF produced by the DB
def db_read_query(query):
    conn = sqlite3.connect("database/db_comp0066.db")
    result = pd.read_sql_query(query, conn)
    conn.close()
    return result
