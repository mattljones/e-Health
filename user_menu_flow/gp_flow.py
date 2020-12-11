# gp_flow.py

# library imports 
from pathlib import Path
import sys 

# Change python path for imports
p = Path(__file__).parents[1]
sys.path.insert(1, str(p))

# Importing utility methods from the 'system' package
from system import utils

# import global variables from globals.py
from system import globals


############################### INPUT MENU PAGES ###########################


############################ SEQUENTIAL STEPS MENUS ########################


########################## MENU NAVIGATION DICTIONARIES ######################


main_flow_gp = {"title": "GP MAIN MENU",
                "type":"main",
                "1":(""),
                "2":(""),
                "3":("")}