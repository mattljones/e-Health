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

display_next_menu = lambda next_dict:utils.display(next_dict)

############################### INPUT MENU PAGES ###########################
def enter_drug(next_dict):
    pass
    return display_next_menu(next_dict)

def display_prescription(next_dict):
    # TODO: display notes & prescription
    pass
    return display_next_menu(next_dict)

def empty_prescription(next_dict):
    # TODO: take a blank prescription
    return display_prescription(next_dict)

def empty_note(next_dict):
    # TODO: take a blank note
    return display_prescription(next_dict)

def enter_note(next_dict):
    pass
    return display_prescription(next_dict)

def prescibe(next_dict):
    # TODO: take the input of field of drug
    flow_dosage = {"title": "Dosage",
                 "type": "auto",
                 "next":(enter_dosage, flow_freq)
                }
    return utils.display(flow_dosage)

def enter_freq(next_dict):
    pass
    # TODO: display the prescription so far
    return display_prescription(next_dict)

def enter_dosage(next_dict):
    pass
    return display_next_menu(next_dict)

def enter_field(next_dict):
    pass
    return display_next_menu(next_dict)

def enter_appoint_id(next_dict):
    pass
    return display_next_menu(next_dict)

############################ SEQUENTIAL STEPS MENUS ########################

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

# final confirm notes & prescription flow
flow_final_confirm = {"title": "Final confrim notes & prescription",
                 "type": "sub",
                 "1":("Yes", display_next_menu, flow_end),
                 "2":("No", prescibe, flow_end)
            }

# add drugs flow
flow_drug = {"title": "Add drugs?",
                 "type": "sub",
                 "1":("Yes", prescibe, flow_end),
                 "2":("No", display_next_menu, flow_final_confirm)
            }

# prescription check flow
flow_check_prescription = {"title": "Check prescription",
                 "type": "sub",
                 "1":("Confirm", display_next_menu, flow_drug),
                 "2":("Edit", prescibe, flow_end)
            }

# frequency flow
flow_freq = {"title": "Frequency",
                 "type": "auto",
                 "next":(enter_freq, flow_check_prescription)
            }

# dosage flow
flow_dosage = {"title": "Dosage",
                 "type": "auto",
                 "next":(enter_dosage, flow_freq)
                }

# prescription flow
flow_prescription = {"title": "Prescription",
                 "type": "sub",
                 "1":("Enter field for prescibed drug", enter_field, flow_dosage),
                 "2":("Skip", empty_prescription, flow_final_confirm)
                 }

# submit note flow
# TODO: public notes?
flow_submit_note = {"title": "Submit Note",
                 "type": "sub",
                 "1":("Submit", display_next_menu, flow_prescription),
                 "2":("No", display_next_menu, flow_end)
                 }

# confirm attendance flow
flow_confirm_attendance = {"title": "Confirm Attendance",
                 "type": "sub",
                 "1":("Yes", enter_note, flow_submit_note),
                 "2":("No", empty_note, flow_end)
                }

# notes flow
flow_notes = {"title": "Notes -- enter appointment id",
              "type": "auto",
              "next":(enter_appoint_id, flow_confirm_attendance)
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
                 "2":("Notes", display_next_menu, flow_notes)
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