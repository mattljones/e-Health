# e_health_main.py

# Importing classes defined in the 'classes' package
from classes.patient import Patient
from classes.gp import GP
from classes.appointment import Appointment
from classes.prescription import Prescription
from classes.record import Record
from classes.schedule import Schedule

# Importing utility methods from the 'system' package
from system import register_login
from system import utilities
from system import usrhelper

# Importing menu paths for each user from the 'user_menu_flow' package
from user_menu_flow import admin_flow
from user_menu_flow import patient_flow
from user_menu_flow import gp_flow

