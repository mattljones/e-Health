# Utility functions

from pathlib import Path
import sys
import sqlite3
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
    elif usr_choice in dict:
        return dict[usr_choice][1](dict[usr_choice][2])

    elif usr_choice in ('E', 'e'):
        print(
            "\n----------------------------------------------------\n" + "\n\U0001F51A Thanks for using e-health. Goodbye!")
        print(asciiart.exit_art)
        sys.exit()

    # TODO: guidance option?
    elif usr_choice in ('H', 'h'):
        pass

    # If invalid entry
    else:
        print("\n\U00002757 Invalid entry, please try again")
        return display(dict)


def validate(user_input):
    """
    Validate user input.  
    
    Custom errors:
        - Empty field
        - Input too long (> 25 chars) francois.xavier.reignier@gmail.com
        - Does not contain "'" or '"' to avoid SQL injections
    """
    # NOTE: This func could be used as decorator
    try:
        if user_input == '':
            raise EmptyError
        elif len(user_input) > 25:
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
        - Empty field
        - Must contain '@' symbol
        - Does not contain "'" or '"' to avoid SQL injections
    """
    # NOTE: This func could be used as decorator
    try:
        if user_input == '':
            raise EmptyError
        elif '@' not in user_input:
            raise EmailFormatError
        elif ('"' in user_input) or ("'" in user_input):
            raise InvalidCharacterError
    except InvalidCharacterError:
        print("\U00002757 Invalid character: ' and \" are not accepted.")
        return False
    except EmptyError:
        print("\U00002757 You need to input a value.")
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


def login(user_email, password, usr_type):
    # TODO: generalize to all user types
    """Check login credentials."""

    # u = (user_email,)
    conn = sqlite3.connect("database/db_comp0066.db")
    c = conn.cursor()
    sql_pwd = 'SELECT ' + usr_type + '_password FROM ' + usr_type + ' WHERE ' + usr_type + '_email=' + "'" + user_email + "'"
    # c.execute('SELECT pw_hash FROM ' + usr_type + ' WHERE user_id=?;', u)
    c.execute(sql_pwd)
    pw_result = c.fetchone()
    if pw_result and pw_result[0] == password:
        # TODO: apply hashing
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
    # day_df = pd.DataFrame({'Booking Hours': times, 'Booking Status': ""})
    # day_df = day_df.set_index('Booking Hours')

    # Handling lunch time
    if (gp_id % 2) == 0:
        day_df.loc['12:00':'12:50'] = 'Lunch Time'
    else:
        day_df.loc['13:00':'13:50'] = 'Lunch Time'

    # Handling Working Days
    working_day_query = """SELECT gp_working_days FROM gp where gp_id == {};""".format(gp_id)
    working_day = db_read_query(working_day_query).loc[
        0, 'gp_working_days']  # will need a query to pull the first working day for a specific GP

    # This part of the code works out when the GP has weekends and populates those days with status "Weekend"
    weekend_day_range = [(working_day + 5) % 7, (working_day + 6) % 7]

    if day_df.columns[0].weekday() in weekend_day_range:
        day_df[day_df.columns[0]] = 'Weekend'

    # Make df pretty
    day_df.columns.values[0] = "Booking Status"
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

    # Handling lunch time
    if (gp_id % 2) == 0:
        week_df.loc[dt.datetime.strptime('12:00', '%H:%M').strftime('%H:%M')
                    :dt.datetime.strptime('12:50', '%H:%M').strftime('%H:%M')] = 'Lunch Time'
    elif (gp_id % 2) != 0:
        week_df.loc[dt.datetime.strptime('13:00', '%H:%M').strftime('%H:%M')
                    :dt.datetime.strptime('13:50', '%H:%M').strftime('%H:%M')] = 'Lunch Time'

    for i in range(7):
        if week_df.columns[i].weekday() in weekend_day_range:
            week_df[week_df.columns[i]] = 'Weekend'

    return week_df.fillna("")


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
