# Utility functions

from pathlib import Path
import os
import sys
import sqlite3
import hashlib
import pandas as pd
import datetime as dt
from system import asciiart
import random
import string
import smtplib
from email.mime.text import MIMEText

# Change python path for imports
p = Path(__file__).parents[1]
sys.path.insert(1, str(p))

# import register, patient, gp & admin main dictionaries
from user_menu_flow.patient_flow import main_flow_patient
from user_menu_flow.gp_flow import main_flow_gp
from user_menu_flow import admin_flow 
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


class LenghtShortError(Error):
    """Raised when input is too short."""
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


class NonAlphabeticCharacterError(Error):
    """Raised when input non alphabetic character"""
    pass


# User is logged in if it has both type and id
def logged():
    """Check whether user is logged in or not."""
    return globals.usr_type in ("patient", "gp", "admin")


def logout():
    """Logout user and return to main page."""
    globals.usr_type = ""
    globals.usr_id = ""
    globals.patient_id = ""
    globals.appt_id = ""
    print("\n\U00002705 Succesfully logged out.")


# Display function for menu
def display(my_dict):
    '''
    Display function called to display menu and run the 
    functions corresponding to the user's choice.
    '''
    
    title = my_dict["title"]

    # checking if title has a subtitle
    break_loc = title.find("\n")
    if break_loc == -1:
        title_length = len(title)
    else: 
        title_length = len(title[0:break_loc])

    # formatting 'main' menus differently from sub-menus
    if my_dict["type"] == "main":
        line_length = 65
        char = "="
    else:
        line_length = 52
        char = "-"
    line = char * line_length

    # padding required to left of main title for it to be centered
    left_padding = ' ' * ((line_length - title_length) // 2)

    print("\n" + line + "\n" + left_padding + title + "\n")

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

            admin_flow.patient_id_choice = ''
            del admin_flow.patient_id_choice
            admin_flow.gp_id_choice = ''
            del admin_flow.gp_id_choice

            return display(admin_flow.main_flow_admin)

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
        print("\n" + line + "\n" + "\n\U0001F51A THANK YOU FOR USING E-HEALTH. SEE YOU NEXT TIME!")
        print(asciiart.exit_art)
        sys.exit()

    # If invalid entry
    else:
        print("\n\U00002757 Invalid entry, please try again and enter your choice.")
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

    # Remove leading and trailing whitespaces
    user_input = user_input.strip()

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


def validate_name(user_input):
    """
    Validate user input for names.  
    
    Custom errors:
        - Empty field
        - Input too short 
        - Only Aa-Zz characters
        - Input too long (> 50 chars) 
        - Does not contain "'" or '"' to avoid SQL injections
    """

    # Remove leading and trailing whitespaces
    user_input = user_input.strip()

    try:
        if user_input == '':
            raise EmptyError
        elif len(user_input) > 50:
            raise LenghtError
        elif len(user_input) < 2:
            raise LenghtShortError
        elif user_input.isalpha() == False:
            raise NonAlphabeticCharacterError
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
    except LenghtShortError:
        print("\U00002757 Input is too short.")
        return False
    except NonAlphabeticCharacterError:
        print("\U00002757 Name must only contain Aa-Zz characters.")
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
        - There is at least 1 letter before and 3 letters after @ 
    """

    # Remove leading and trailing whitespaces
    user_input = user_input.strip()

    email_query = 'SELECT patient_email FROM patient'
    emails = db_read_query(email_query)

    try:
        if user_input == '':
            raise EmptyError
        elif '@' not in user_input:
            raise EmailFormatError
        elif user_input.find('@') == 0:
            raise EmailFormatError
        elif len(user_input) - (user_input.find('@') + 1) < 3:
            raise EmailFormatError
        elif (emails['patient_email'] == user_input.lower()).any():
            raise DuplicateEmailError
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

    # Remove leading and trailing whitespaces
    user_input = user_input.strip()

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

    try:
        if user_input == '':
            raise EmptyError
        elif ('"' in user_input) or ("'" in user_input):
            raise InvalidCharacterError
        elif ((len(user_input) != 10) or
              (user_input[4] != '-') or
              (user_input[7] != '-')):
            raise DateFormatError

        year = int(user_input[:4])
        month = int(user_input[5:7])
        day = int(user_input[8:])

        dt.date(year, month, day)

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
    '''
    Asks user to input a start date and checks that it is not earlier than today
    :return: string
    '''
    print("\nPlease enter the start date (YYYY-MM-DD)\n"
          "Enter 'T' short for today")
    start_date = input("--> ")
    valid = False
    while valid == False:
        if start_date in ("T", "t"):
            valid = True
            start_date = dt.date.today().isoformat()
            return start_date
        elif validate_date(start_date):
            if dt.date.fromisoformat(start_date) >= dt.date.today():
                valid = True
                return start_date
            else:
                print("\n\U00002757 Schedule date cannot be earlier than today.")
        else:
            print("\n\U00002757 Invalid entry, please try again and enter your choice.")
        if valid == False:
            start_date = input("\n--> ")


def get_end_date():
    '''
    Asks user to input a end date and checks that it is not earlier than today
    :return: string
    '''
    print("\nPlease enter the end date (YYYY-MM-DD)")
    end_date = input("--> ")
    valid = False
    while valid == False:
        if end_date in ("T", "t"):
            valid = True
            end_date = dt.date.today().isoformat()
            return end_date
        elif validate_date(end_date):
            if dt.date.fromisoformat(end_date) > dt.date.today():
                valid = True
                return end_date
            else:
                print("\n\U00002757 Schedule date cannot be earlier than today.")
        else:
            print("\n\U00002757 Invalid entry, please try again and enter your choice.")
        if valid == False:
            end_date = input("\n--> ")


# NOTE: To test
def get_date():
    '''
    Asks user to input a start date
    :return: string
    '''
    print("\nPlease enter the start date (YYYY-MM-DD)\n"
          "Enter 'T' short for today")
    date = input("--> ")
    valid = False
    while valid == False:
        if date in ("T", "t"):
            valid = True
            date = dt.date.today().isoformat()
            return date
        elif validate_date(date):
            valid = True
            return date
        else:
            print("\n\U00002757 Invalid entry, please try again and enter your choice.")

        if valid == False:
            date = input("\n--> ")


# NOTE: To test
def end_date(start_date):
    '''
    Get a date that is equal or later than specified start_date.
    '''
    print("\nPlease enter the end date (YYYY-MM-DD)")
    end_date = input("--> ")
    valid = False
    while valid == False:
        if end_date in ("T", "t"):
            if dt.date.fromisoformat(start_date) <= dt.date.today():
                valid = True
                end_date = dt.date.today().isoformat()
                return end_date
        elif validate_date(end_date):
            if dt.date.fromisoformat(end_date) >= dt.date.fromisoformat(start_date):
                valid = True
                return end_date
            else:
                print("\n\U00002757 End date cannot be earlier than starting date {}.".format(start_date))
        else:
            print("\n\U00002757 Invalid entry, please try again and enter your choice.")
        if valid == False:
            end_date = input("\n--> ")


def login(user_email, password, usr_type):
    """Check login credentials."""

    # u = (user_email,)
    conn = sqlite3.connect("database/db_comp0066.db")
    c = conn.cursor()

    sql_hash_salt = 'SELECT ' + usr_type + '_password FROM ' + usr_type + ' WHERE ' + usr_type + '_email=' + "'" + user_email + "'"

    sql_result_df = db_read_query(sql_hash_salt)

    if sql_result_df.empty:
        return False, "confirmed"

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

    # Check if new key matches our stored key
    if hash_key_to_check == hash_key:

        if usr_type == "patient":
            sql_id = 'SELECT patient_id, patient_status FROM patient WHERE patient_email=' + "'" + user_email + "'"
            c.execute(sql_id)
            result = c.fetchone()
            usr_id, status = result[0], result[1]
            globals.usr_type = usr_type
            globals.usr_id = usr_id
            conn.close()
            return True, status

        else:
            sql_id = 'SELECT ' + usr_type + '_id FROM ' + usr_type + ' WHERE ' + usr_type + '_email=' + "'" + user_email + "'"
            c.execute(sql_id)
            usr_id = c.fetchone()[0]
            globals.usr_type = usr_type
            globals.usr_id = usr_id
            conn.close()
            return True, "confirmed"

    else:
        conn.close()
        return False, "confirmed"


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

    Patient.change_gp('auto', patient_id)

    # Return boolean to use in user flow
    return True


def help():
    """ Help user understand and navigate the program."""
    # NOTE: Advanced feature
    pass


def export():
    """ Export content of the page in .csv """
    # NOTE: Advanced feature
    pass


def day_empty_df(date, gp_id):
    '''
    Produces empty dataframe handling weekends and lunch time for a specific date and gp_id
    :param date: date as string
    :param gp_id: gp_id from database
    :return: DataFrame
    '''
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
    '''
    Produces empty dataframe handling weekends and lunch time for a specific week and gp_id
    :param start_date: data as string (starting day of week)
    :param gp_id: gp_id from database
    :return: DataFrame
    '''
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

    week_df = week_df.fillna("")

    return week_df


def split_week_df(df_object, gp_id):
    if gp_id % 2 == 0:
        lunchtime_start = '11:50'
        lunchtime_end = '13:00'
    else:
        lunchtime_start = '12:50'
        lunchtime_end = '14:00'

    df_print_morning = df_object.loc[:lunchtime_start].to_markdown(tablefmt="grid", index=True)
    df_print_afternoon = df_object.loc[lunchtime_end:].to_markdown(tablefmt="grid", index=True)
    return df_print_morning, df_print_afternoon


def db_execute(query):
    '''
    Executes sqlite queries
    :param query: sqlite query
    :return: query execution
    '''
    conn = sqlite3.connect('database/db_comp0066.db')
    c = conn.cursor()
    c.execute(query)
    conn.commit()
    conn.close()


def db_read_query(query):
    '''
    Executes sqlite queries (via DataFrame)
    :param query: sqlite query
    :return: query execution
    '''
    conn = sqlite3.connect("database/db_comp0066.db")
    result = pd.read_sql_query(query, conn)
    conn.close()
    return result


def random_string(length):
    '''
    Generate random key that is later sent to user via email to validate his/her identity
    :param length: length of random string (int)
    :return: random string (str)
    '''
    letters = string.ascii_lowercase + string.digits
    random_string = ''.join(random.choice(letters) for i in range(length))
    return random_string


def send_mail_password_reset(user_email, random_string):
    '''
    Sends a mail to user_email incl. random_string
    :param user_email: mail of user
    :param random_string: random_string generated by random_string function
    :return: send a mail to user_email
    '''
    # Establish Mail Server
    smtp_object = smtplib.SMTP('smtp.gmail.com', 587)

    # Login to Gmail
    email = 'e.health.comp0066@gmail.com'
    # password to above mentioned gmail address (please do not share with 3rd parties)
    # normally this password would be protected and not be accessible to an user.
    password = "&/h'Jj'}c)Y6?T@%:^Y["

    # Define Mail parameters
    from_address = 'e.health.comp0066@gmail.com'
    to_address = '{}'.format(user_email)
    message = MIMEText("""Hi, your code to reset your password is:\n{}""".format(random_string))
    message['Subject'] = 'Password Reset for E-HEALTH'
    message['To'] = '{}'.format(user_email)

    # Error Handling
    try:
        # Establish Mail Server
        smtp_object.ehlo()
        # Encryption
        smtp_object.starttls()
        # Login to Gmail
        smtp_object.login(email, password)
        # Send Mail
        smtp_object.sendmail(from_address, to_address, message.as_string())
    except smtplib.SMTPRecipientsRefused:
        print("Your email address seems to be invalid")
    except:
        print("An error occured while sending the mail from our Gmail Account")

    # Close connection to Mail server
    smtp_object.quit()


def send_code_to_registered_user(user_type, user_email, random_string_password_reset):
    '''
    Send mail with random_string to registered user.
    :param user_type: 'patient', 'gp' or 'admin'
    :param user_email: email of user (str)
    :param random_string_password_reset: random string generated by random_string method
    :return: email_sent = True if email sent, or = False if no user registered with this mail
    '''
    # input mail and check if in database
    patient_email_query = """
        SELECT
            {}_id,
            {}_email
        FROM
            {}
        WHERE
            {}_email = '{}';""".format(user_type, user_type, user_type, user_type, user_email)

    user_email_df = db_read_query(patient_email_query)

    # one could also do a function with the things below and above
    if user_email_df.empty:
        # there is no patient registered with this email address --> redirect to patient registration or
        # tell the user to go back with #
        message = 'There is no {} registered with this email address.'.format(user_type)
        email_sent = False

    else:
        # send email to user
        send_mail_password_reset(user_email, random_string_password_reset)
        message = '''The code to reset your password was sent to your email address: {}.\nPlease check your mail inbox and spam folder.'''.format(
            user_email)
        email_sent = True

    return email_sent, message


def compare_random_string(random_string_password_reset):
    '''
    Compare random_string_password_reset with random_string_user_input
    :return: True if random_string_user_input and random_string_password_reset match, else False
    '''
    random_string_match = False
    available_tries = 3
    while random_string_match == False and available_tries > 0:
        random_string_user_input = input("\nPlease enter your string:")
        if random_string_user_input == random_string_password_reset:
            random_string_match = True
            print('Your code matched')
        else:
            available_tries = available_tries - 1
            print('The code you entered did not match. You have {} more tries'.format(available_tries))
    return random_string_match


def password_reset_input():
    '''
    Asking user for new password after password reset and validating it using utils.validate_password
    as well as asking user to confirm password
    :return: hashed new_password
    '''
    new_password_validation = False
    new_password_match = False
    while new_password_validation == False:
        new_password = input('Please input your new password:')
        new_password_validation = validate_password(new_password)

        while new_password_validation == True and new_password_match == False:
            new_password_confirmation = input('Please confirm your new password:')
            if new_password_confirmation != new_password:
                print("\U00002757 Password confirmation does not match original password. Please enter a new password.")
                new_password_validation = False
                break
            else:
                new_password_match = True
                return new_password_match, hash_salt(new_password)


def change_password(user_type, user_email, random_string_password_reset):
    '''
    Updates password after the random_string match was validated.
    :return: Updated the password of the user in the database
    '''
    if compare_random_string(random_string_password_reset) == True:

        new_password = password_reset_input()[1]

        # Update database with new password
        update_password_query = """
            UPDATE
                {}
            SET
                {}_password = '{}'
            WHERE
                {}_email = '{}';""".format(user_type, user_type, new_password, user_type, user_email)

        db_execute(update_password_query)
        message = 'Your password has been successfully changed'

    else:
        message = 'Your password could not be changed because your code does not match'

    return True, message
