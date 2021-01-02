from system import utils as u
import sqlite3

# Generate random key
import random
import string
def random_string(length):
    '''

    :param length: length of random string (int)
    :return: random string (str)
    '''
    letters = string.ascii_lowercase
    random_string = ''.join(random.choice(letters) for i in range(length))
    return random_string

# important to call the random_string function and assign it to a global variable to later compare it
random_string_password_reset = random_string(8)


import smtplib
from email.mime.text import MIMEText
import getpass
def send_mail_password_reset(user_email, random_string):
    '''

    :param user_email:
    :return:
    '''
    # Establish Mail Server
    smtp_object = smtplib.SMTP('smtp.gmail.com', 587)
    smtp_object.ehlo()

    # Encryption
    smtp_object.starttls()

    # Login to Gmail
    email = 'e.health.comp0066@gmail.com'
    password = "&/h'Jj'}c)Y6?T@%:^Y["
    smtp_object.login(email,password)

    # Define Mail parameters
    from_address = 'e.health.comp0066@gmail.com'
    to_address = '{}'.format(user_email)
    message = MIMEText("""Hi, your code to reset your password is:\n{}""".format(random_string))
    message['Subject'] = 'Password Reset for E-HEALTH'
    message['To'] = '{}'.format(user_email)

    # Send Mail
    smtp_object.sendmail(from_address,to_address,message.as_string())

patient_user_email = input('Please input your email address:')

def send_mail_if_patient_registered(patient_user_email):
    # input mail and check if in database
    patient_email_query = """
        SELECT
            patient_id,
            patient_email
        FROM
            patient
        WHERE
            patient_email = '{}';""".format(patient_user_email)

    patient_email_df = u.db_read_query(patient_email_query)

    # one could also do a function with the things below and above
    if patient_email_df.empty:
        # there is no patient registered with this email address --> redirect to patient registration or
        # tell the user to go back with #
        print('There is no patient registered with this email address')

    else:
        # send email to user
        send_mail_password_reset(patient_email_df.loc[0,'patient_email'], random_string_password_reset)
        print('The code to reset your password was sent to your email address.\nPlease check your mail inbox and spam folder')

send_mail_if_patient_registered(patient_user_email)

# Compare random strings
def compare_random_string():
    '''
    Compare random_string_password_reset with random_string_user_input
    :return: True if random_string_user_input and random_string_password_reset match, else False
    '''
    random_string_match = False
    n = 3
    while random_string_match == False and n > 0:
        random_string_user_input = input("Please enter your string:")
        if random_string_user_input == random_string_password_reset:
            random_string_match = True
            print('Your code matched')
        else:
            n = n - 1
            print('The code you entered did not match. You have {} more tries'.format(n))
    return random_string_match


def change_password():
    '''
    Updates password after the random_string match was validated.
    :return: Updated the password of the user in the database
    '''
    if compare_random_string() == True:
        new_patient_password = input('Please input your new password:')

    # Update database with new password
    update_password_query = """
        UPDATE
            patient
        SET
            patient_password = '{}'
        WHERE
            patient_id = {};""".format(new_patient_password, patient_email_df.loc[0,'patient_id'])

    u.db_execute(update_password_query)
    print('Your password has been successfully changed')

change_password()