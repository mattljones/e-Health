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
globals.init()

############################### INPUT MENU PAGES ###########################


############################ SEQUENTIAL STEPS MENUS ########################

display_next_menu = lambda next_dict:utils.display(next_dict)

########################## MENU NAVIGATION DICTIONARIES ######################

# Empty nested dictionary to store in tuple for last menu
# before going back to main page (for display function return parameter).
flow_end = {"title": "CHANGES SAVED",
              "type":"sub"}


# schedule flow
flow_schedule = {"title": "Schedule",
                 "type": "sub",
                 "1":("pass", display_next_menu, flow_end)
                }

# availability flow
flow_availability = {"title": "Availability",
                 "type": "sub",
                 "1":("pass", display_next_menu, flow_end)
                }

# appointment flow
flow_appointments = {"title": "Appointments",
                 "type": "sub",
                 "1":("pass", display_next_menu, flow_end)
                }

# records flow
flow_records = {"title": "Records",
                 "type": "sub",
                 "1":("pass", display_next_menu, flow_end)
                }

# gp main page dictionary
main_flow_gp = {"title": "GP MAIN MENU",
                "type":"main",
                "1":("View Schedule", display_next_menu, flow_schedule),
                "2":("Add availability", display_next_menu, flow_availability),
                "3":("Manage Appointments", display_next_menu, flow_appointments),
                "4":("Records", display_next_menu, flow_records)}