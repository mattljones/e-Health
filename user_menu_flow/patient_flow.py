# patient_flow.py

# library imports 
from pathlib import Path
import sys 

# Change python path for imports
p = Path(__file__).parents[1]
sys.path.insert(1, str(p))

# Importing utility methods from the 'system' package
from system.utils import display, logout

# import global variables from globals.py
from system import globals


############################### INPUT MENU PAGES ###########################



############################ SEQUENTIAL STEPS MENUS ########################

def manage_appointment():
    '''
    '''
    pass

def change_GP_pair():
    '''
    '''
    pass

def read_messages():
    '''
    '''
    pass


######################### MENU NAVIGATION DICTIONARIES ######################

next_dict_1 = {}

next_dict_2 = {}

next_dict_3 = {}

# Empty nested dictionary to store in tuple for last menu,
# for display function return parameter.
empty_dict = {}

main_flow = {"title": "PATIENT MAIN MENU",
             "type":"main",
             "1":("Book & Manage Appointments",manage_appointment,next_dict_1),
             "2":("Change default GP",change_GP_pair, next_dict_2),
             "3":("Read messages",read_messages, next_dict_3),
             "X":("Logout",logout, empty_dict)}
