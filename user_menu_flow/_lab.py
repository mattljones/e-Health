# import sqlite3
# conn = sqlite3.connect("database/db_comp0066.db")
# c = conn.cursor()
# sql_pwd = "SELECT patient_password FROM patient WHERE patient_email='wikinerd@msn.com'"
# r = c.execute(sql_pwd)
# print(type(r))
# print(r)
# print(r.fetchall())

'''
https://www.asciiart.eu/miscellaneous/medical
https://stackoverflow.com/questions/23623288/print-full-ascii-art
http://www.asciiworld.com/-Miscelleneaous-.html
'''

# def b(y):
#     return y + 1

# def a(x):
#     b(x)

# a(6)

import os
import hashlib
salt = os.urandom(32)

def hash_salt(password):
    """
    Hash and salt passwords.
    """

    salt = os.urandom(32)
    print('salt: ', salt)

    hash_key = hashlib.pbkdf2_hmac(
        'sha256', 
        password.encode('utf-8'), 
        salt, 
        100000
    )
    print('hash_key: ', hash_key)

    hash_salt = salt + hash_key

    return hash_salt

a = hash_salt('123')
print(type(a))
print(a)