# gp_flow.py

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


########################## MENU NAVIGATION DICTIONARIES ######################


main_flow = {"title": "GP MAIN MENU",
             "type":"main",
             "1":(""),
             "2":(""),
             "3":(""),
             "X":("Logout",logout)}