import sqlite3
import pandas as pd
import classes

# INSERTING GP - INSTANCE method

new_gp = classes.GP()
new_gp.first_name = input("Enter the first name: ")
new_gp.last_name = input("Enter the last name: ")
new_gp.gender = input("Enter the gender: ")
new_gp.birth_date = input("Enter the birth date: ")
new_gp.email = input("Enter the email: ")
new_gp.password = input("Enter the password: ")
new_gp.specialisation_id = input("Enter the specialisation id: ")
new_gp.department_id = input("Enter the department id: ")
new_gp.working_days = input("Enter the working days: ")
new_gp.status = input("Enter the status: ")

new_gp.insert()

# conn = sqlite3.connect("database.db")
# gp = pd.read_sql_query("SELECT * FROM gp;", conn)
# print(gp)
# conn.close()


# INSERTING GP - STATIC method

# first_name = input("Enter the first name: ")
# last_name = input("Enter the last name: ")
# gender = input("Enter the gender: ")
# birth_date = input("Enter the birth date: ")
# email = input("Enter the email: ")
# password = input("Enter the password: ")
# specialisation_id = input("Enter the specialisation id: ")
# department_id = input("Enter the department id: ")
# working_days = input("Enter the working days: ")
# status = input("Enter the status: ")
#
# classes.GP.insert_static(first_name, last_name, gender, birth_date, email, password, specialisation_id, department_id, working_days, status)
#
# conn = sqlite3.connect("database.db")
# gp = pd.read_sql_query("SELECT * FROM gp;", conn)
# print(gp)
# conn.close()