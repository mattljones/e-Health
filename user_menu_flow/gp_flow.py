# gp_flow.py

# library imports 
from pathlib import Path
import sys
from datetime import date

# Change python path for imports
p = Path(__file__).parents[1]
sys.path.insert(1, str(p))

# Importing utility methods from the 'system' package
from system import utils

from classes.appointment import Appointment
from classes.record import Record
from classes.schedule import Schedule

# import global variables from globals.py
from system import globals
globals.init()

display_next_menu = lambda next_dict:utils.display(next_dict)

############################### INPUT MENU PAGES ###########################
def edit_notes(next_dict):
    record = Record.select(globals.patient_id)[0]
    print("\nPlase input the appointment id of note you want to change")
    # TODO: validate the input and provide return
    apt_id = input("--> ")
    print("\nPlase input the new note")
    new_note = input("--> ")
    record.appointment_notes[apt_id] = new_note
    record.update()
    print(Record.select(globals.patient_id)[4])
    return display_prescription(next_dict)

def edit_cc(next_dict):
    record = Record.select(globals.patient_id)[0]
    # TODO: exception control; validation
    edit_cond_flag = True
    while edit_cond_flag:
        if record.conditions:
            print("[1] Add condtion\n"
                "[2] Remove condition\n")
            add_or_delete = input("--> ")
            if add_or_delete == '1':
                print("\nPlase input the condition id you want to add (1-20)")
                cond_id = input("--> ")
                record.conditions.append(cond_id)
                record.update()
            elif add_or_delete == '2':
                print("\nPlase input the condition id you want to remove")
                cond_id = input("--> ")
                record.conditions.remove(cond_id)
                record.update()
        else:
            print("[1] Add condtion\n"
                "[2] End (There's no more condition to remove)\n")
            add_or_delete = input("--> ")
            if add_or_delete == '1':
                print("\nPlase input the condition id you want to add (1-20)")
                cond_id = input("--> ")
                record.conditions.append(cond_id)
                record.update()
            elif add_or_delete == '2':
                edit_cond_flag = False
        print("\nMore change?")
        print("[1] Yes\n"
            "[2] No\n")
        tmp = input("--> ")
        if tmp == '2':
            edit_cond_flag = False
    else:
        print("\n【Patient Table】\n", Record.select(globals.patient_id)[2])
        print("\n【Patient Table】\n", Record.select(globals.patient_id)[4])
    return display_prescription(next_dict)

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
    return display_next_menu(flow_dosage)

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

def correct_note_change(next_dict):
    flow_record_edit = {"title": "Edit what part of the records?",
                 "type": "sub",
                 "1":("Chronic Condition", edit_cc, flow_confirm_change),
                 "2":("Notes", edit_notes, flow_confirm_change)
                }
    return display_next_menu(flow_record_edit)

# TODO: booking id input validation

def displey_pending_appt(next_dict):
    # TODO: how to tell if there is an unconfirmed appointment
    # print("\nYour do not have any pending appointment!")
    print("\nYour pending appointments: ")
    print(Appointment.select_GP_pending(globals.usr_id)[1])
    return display_next_menu(next_dict)

def another_confirm_rej(next_dict):
    flow_confirm_appoint = {"title": "Confirm Appointments",
                 "type": "sub",
                 "1":("Confirm All", another_confirm_all, next_dict),
                 "2":("Confirm One", another_confirm_one, next_dict),
                 "3":("Reject One", another_confirm_rej, next_dict)
                }

    print("\nPleas enter the id of appointment you want to reject")
    reject_id = input("\n--> ")
    Appointment.change_status(reject_id, "rejected")
    print(Appointment.select_GP_appt(globals.usr_id)[1])

    print("\n----------------------------------------------------\n"
          "                ", "Confrim another appointment?", "\n")
    print("[ 1 ] Yes")
    print("[ 2 ] No")
    usr_choice = input("\n--> ")
    if usr_choice == '1':
        return display_next_menu(flow_confirm_appoint)
    elif usr_choice == '2':
        return display_next_menu(next_dict)

def another_confirm_one(next_dict):
    flow_confirm_appoint = {"title": "Confirm Appointments",
                 "type": "sub",
                 "1":("Confirm All", another_confirm_all, next_dict),
                 "2":("Confirm One", another_confirm_one, next_dict),
                 "3":("Reject One", another_confirm_rej, next_dict)
                }

    print("\nPleas enter the id of appointment you want to confirm")
    confirm_id = input("\n--> ")
    Appointment.change_status(confirm_id, "confirmed")
    print(Appointment.select_GP_appt(globals.usr_id)[1])

    print("\n----------------------------------------------------\n"
          "                ", "Confrim another appointment?", "\n")
    print("[ 1 ] Yes")
    print("[ 2 ] No")
    usr_choice = input("\n--> ")
    if usr_choice == '1':
        return display_next_menu(flow_confirm_appoint)
    elif usr_choice == '2':
        return display_next_menu(next_dict)

def another_confirm_all(next_dict):
    flow_confirm_appoint = {"title": "Confirm Appointments",
                 "type": "sub",
                 "1":("Confirm All", another_confirm_all, next_dict),
                 "2":("Confirm One", another_confirm_one, next_dict),
                 "3":("Reject One", another_confirm_rej, next_dict)
                }
    Appointment.confirm_all_GP_pending(globals.usr_id)
    print(Appointment.select_GP_appt(globals.usr_id)[1])

    print("\n----------------------------------------------------\n"
          "                ", "Confrim another appointment?", "\n")
    print("[ 1 ] Yes")
    print("[ 2 ] No")
    usr_choice = input("\n--> ")
    if usr_choice == '1':
        return display_next_menu(flow_confirm_appoint)
    elif usr_choice == '2':
        return display_next_menu(next_dict)

def remove_timeoff(next_dict):
    flow_timeoff = {"title": "Schedule",
                 "type": "sub",
                 "1":("Add", add_timeoff, next_dict),
                 "2":("Remove", remove_timeoff, next_dict)
                }
    start_date = utils.get_start_date()
    end_date = utils.get_end_date()
    Schedule.delete_timeoff(globals.usr_id, 'custom', 'time off', start_date, end_date)

    print("\n----------------------------------------------------\n"
          "                ", "Add or Remove a new timeoff?", "\n")
    print("[ 1 ] Yes")
    print("[ 2 ] No")
    usr_choice = input("\n--> ")
    if usr_choice == '1':
        return display_next_menu(flow_timeoff)
    elif usr_choice == '2':
        return display_next_menu(next_dict)

def add_timeoff(next_dict):
    flow_timeoff = {"title": "Schedule",
                 "type": "sub",
                 "1":("Add", add_timeoff, next_dict),
                 "2":("Remove", remove_timeoff, next_dict)
                }
    # TODO: add availability
    # TODO: fix Schedule.insert_timeoff
    start_date = utils.get_start_date()
    end_date = utils.get_end_date()
    Schedule.insert_timeoff(globals.usr_id, 'time off', start_date, end_date)

    print("\n----------------------------------------------------\n"
          "                ", "Add or Remove a new availabilty?", "\n")
    print("[ 1 ] Yes")
    print("[ 2 ] No")
    usr_choice = input("\n--> ")
    if usr_choice == '1':
        return display_next_menu(flow_timeoff)
    elif usr_choice == '2':
        return display_next_menu(next_dict)

def view_another_day(next_dict):
    flow_schedule = {"title": "Schedule",
                 "type": "sub",
                 "1":("Day", view_another_day, next_dict),
                 "2":("Week", view_another_week, next_dict)
                }
    #call schedule class method to display the schedule by day
    print("\n----------------------------------------------------\n"
        "              Schedule View by Day\n")
    start_date = utils.get_start_date()
    print(start_date)
    print(Schedule.select(globals.usr_id, 'day', start_date)[1])

    print("\n----------------------------------------------------\n"
          "                ", "Schedule", "\n")
    print("[ 1 ] View another schedule")
    print("[ 2 ] Manage timeoff")
    usr_choice = input("\n--> ")
    if usr_choice == '1':
        return display_next_menu(flow_schedule)
    elif usr_choice == '2':
        return display_next_menu(next_dict)

def view_another_week(next_dict):
    flow_schedule = {"title": "Schedule",
                 "type": "sub",
                 "1":("Day", view_another_day, next_dict),
                 "2":("Week", view_another_week, next_dict)
                }
    #call schedule class method to display the schedule by week
    print("\n----------------------------------------------------\n"
        "              Schedule View by Week\n")
    start_date = utils.get_start_date()
    print(start_date)
    print(Schedule.select(globals.usr_id, 'week', start_date)[1])

    print("\n----------------------------------------------------\n"
          "                ", "Schedule", "\n")
    print("[ 1 ] View another schedule")
    print("[ 2 ] Manage timeoff")
    usr_choice = input("\n--> ")
    if usr_choice == '1':
        return display_next_menu(flow_schedule)
    elif usr_choice == '2':
        return display_next_menu(next_dict)

def view_records(next_dict):
    # TODO: display 10 latest clients
    print("\nPlease enter patient id you want to search:")
    patient_id = input("--> ")
    globals.patient_id = patient_id
    print("\n【Patient Table】")
    print(Record.select(patient_id)[2])
    print("\n【Appointment Table】")
    print(Record.select(patient_id)[4])
    return display_next_menu(next_dict)

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
                "1":("Confirm All", another_confirm_all, flow_end),
                "2":("Confirm One", another_confirm_one, flow_end),
                "3":("Reject One", another_confirm_rej, flow_end)
                }

# timeoff flow
flow_timeoff = {"title": "Schedule",
                 "type": "sub",
                 "1":("Add", add_timeoff, flow_end),
                 "2":("Remove", remove_timeoff, flow_end)
                }
# schedule flow
flow_schedule = {"title": "Schedule",
                "type": "sub",
                "1":("Day", view_another_day, flow_timeoff),
                "2":("Week", view_another_week, flow_timeoff)
                }

# appointment flow
flow_appointments = {"title": "Appointments",
                 "type": "sub",
                 "1":("Confirm", displey_pending_appt, flow_confirm_appoint),
                 "2":("Notes", display_next_menu, flow_notes)
                }

flow_confirm_change = {"title": "Confirm edit",
                 "type": "sub",
                 "1":("Yes", display_next_menu, flow_end),
                 "2":("Change More / No", correct_note_change, flow_end)
                }

flow_record_edit = {"title": "Edit what part of the records?",
                 "type": "sub",
                 "1":("Notes", edit_notes, flow_confirm_change),
                 "2":("Chronic Condition", edit_cc, flow_confirm_change)
                }

# flow of decision on editing records of a patient
flow_record_choose = {"title": "Edit Records of this patient?",
                 "type": "sub",
                 "1":("Yes", display_next_menu, flow_record_edit),
                 "2":("No", display_next_menu, flow_end)
                }

# records flow
flow_records = {"title": "Records",
                 "type": "sub",
                 "1":("Search patient", view_records, flow_record_choose)
                }

# gp main page dictionary
main_flow_gp = {"title": "GP MAIN MENU",
                "type":"main",
                "1":("View Schedule", display_next_menu, flow_schedule),
                "2":("Manage timeoff", display_next_menu, flow_timeoff),
                "3":("Manage Appointments", display_next_menu, flow_appointments),
                "4":("Records", display_next_menu, flow_records)}