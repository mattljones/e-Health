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

def another_confirm(next_dict):
    flow_confirm_appoint = {"title": "Confirm Appointments",
                 "type": "sub",
                 "1":("Confirm", another_confirm, next_dict),
                 "2":("Reject", another_confirm, next_dict)
                }
    print("\n----------------------------------------------------\n"
          "                ", "Confrim another appointment?", "\n")
    print("[ 1 ] Yes")
    print("[ 2 ] No")
    usr_choice = input("\n--> ")
    if usr_choice == '1':
        return utils.display(flow_confirm_appoint)
    elif usr_choice == '2':
        return utils.display(next_dict)

def another_avail(next_dict):
    flow_availability = {"title": "Schedule",
                 "type": "sub",
                 "1":("Add", another_avail, next_dict),
                 "2":("Remove", another_avail, next_dict)
                }
    print("\n----------------------------------------------------\n"
          "                ", "Add or Remove a new availabilty", "\n")
    print("[ 1 ] Yes")
    print("[ 2 ] No")
    usr_choice = input("\n--> ")
    if usr_choice == '1':
        return utils.display(flow_availability)
    elif usr_choice == '2':
        return utils.display(next_dict)

def view_another_day(next_dict):
    flow_schedule = {"title": "Schedule",
                 "type": "sub",
                 "1":("Day", view_another_day, next_dict),
                 "2":("Week", view_another_week, next_dict),
                 "3":("Custom", view_another_custom, next_dict),
                }
    # TODO: call schedule class method to display the schedule
    print("\n----------------------------------------------------\n"
          "                ", "Schedule by day", "\n")
    print("[ 1 ] View another schedule")
    print("[ 2 ] Manage the availability")
    usr_choice = input("\n--> ")
    if usr_choice == '1':
        return utils.display(flow_schedule)
    elif usr_choice == '2':
        return utils.display(next_dict)

def view_another_week(next_dict):
    flow_schedule = {"title": "Schedule",
                 "type": "sub",
                 "1":("Day", view_another_day, next_dict),
                 "2":("Week", view_another_week, next_dict),
                 "3":("Custom", view_another_custom, next_dict),
                }
    # TODO: call schedule class method to display the schedule
    print("\n----------------------------------------------------\n"
          "                ", "Schedule by Week", "\n")
    print("[ 1 ] View another schedule")
    print("[ 2 ] Manage the availability")
    usr_choice = input("\n--> ")
    if usr_choice == '1':
        return utils.display(flow_schedule)
    elif usr_choice == '2':
        return utils.display(next_dict)

def view_another_custom(next_dict):
    flow_schedule = {"title": "Schedule",
                 "type": "sub",
                 "1":("Day", view_another_day, next_dict),
                 "2":("Week", view_another_week, next_dict),
                 "3":("Custom", view_another_custom, next_dict),
                }
    # TODO: call schedule class method to display the schedule
    print("\n----------------------------------------------------\n"
          "                ", "Custom Schedule", "\n")
    print("[ 1 ] View another schedule")
    print("[ 2 ] Manage the availability")
    usr_choice = input("\n--> ")
    if usr_choice == '1':
        return utils.display(flow_schedule)
    elif usr_choice == '2':
        return utils.display(next_dict)

########################## MENU NAVIGATION DICTIONARIES ######################

# Empty nested dictionary to store in tuple for last menu
# before going back to main page (for display function return parameter).
flow_end = {"title": "CONTINUE E-HEALTH OR LOGOUT ?",
              "type":"sub"}

# notes flow
flow_notes = {"title": "Notes",
                 "type": "sub",
                 "1":("Yes", display_next_menu, flow_end),
                 "2":("No", display_next_menu, flow_end)
                }

# confirm appointment flow
flow_confirm_appoint = {"title": "Confirm Appointments",
                 "type": "sub",
                 "1":("Confirm", another_confirm, flow_end),
                 "2":("Reject", another_confirm, flow_end)
                }

# availability flow
flow_availability = {"title": "Schedule",
                 "type": "sub",
                 "1":("Add", another_avail, flow_end),
                 "2":("Remove", another_avail, flow_end)
                }
# schedule flow
flow_schedule = {"title": "Schedule",
                "type": "sub",
                "1":("Day", view_another_day, flow_availability),
                "2":("Week", view_another_week, flow_availability),
                "3":("Custom", view_another_custom, flow_availability),
                }

# appointment flow
flow_appointments = {"title": "Appointments",
                 "type": "sub",
                 "1":("Confirm", display_next_menu, flow_confirm_appoint),
                 "2":("Notes", display_next_menu, flow_end)
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