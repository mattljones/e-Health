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

empty_method = lambda next_dict:utils.display(next_dict)

########################## MENU NAVIGATION DICTIONARIES ######################

# Empty nested dictionary to store in tuple for last menu
# before going back to main page (for display function return parameter).
empty_dict = {"title": "CHANGES SAVED",
              "type":"sub"}


# schedule flow
flow_schedule = {"title": "Schedule",
                 "type": "sub",
                 "1":("pass")
                }

# availability flow
flow_availability = {"title": "Availability",
                 "type": "sub",
                 "1":("pass")
                }

# appointment flow
flow_appointments = {"title": "Appointments",
                 "type": "sub",
                 "1":("pass")
                }

# records flow
flow_records = {"title": "Records",
                 "type": "sub",
                 "1":("pass")
                }

# gp main page dictionary
main_flow_gp = {"title": "GP MAIN MENU",
                "type":"main",
                "1":("View Schedule", empty_method, flow_schedule),
                "2":("Add availability", empty_method, flow_schedule),
                "3":("Manage Appointments", empty_method, flow_schedule),
                "4":("Records", empty_method, flow_schedule)}