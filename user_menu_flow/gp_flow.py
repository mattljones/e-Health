# gp_flow.py

# library imports 
from pathlib import Path
import sys
from datetime import date
from datetime import timedelta

# Change python path for imports
p = Path(__file__).parents[1]
sys.path.insert(1, str(p))

# Importing utility methods from the 'system' package
from system import utils

from classes.appointment import Appointment
from classes.record import Record
from classes.schedule import Schedule
from classes.prescription import Prescription

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
    return display_next_menu(next_dict)

def simple_note(next_dict):
    flow_submit_note = {"title": "Submit Note",
                 "type": "sub",
                 "1":("Submit", display_next_menu, flow_prescription),
                 "2":("No", simple_note, flow_prescription)
                 }
    

    print("\nPlase input the new note")
    new_note = input("--> ")
    Appointment(booking_id=globals.appt_id, booking_notes=new_note).update()
    print(Appointment.select(globals.appt_id)[3])

    print("\n----------------------------------------------------\n"
        "                ", "Submit Note?", "\n")
    print("[ 1 ] Yes")
    print("[ 2 ] No")
    usr_choice = input("\n--> ")
    while usr_choice not in ["1", "2"]:
        print("\nInvalid input, please try again!")
        usr_choice = input("\n--> ")
    if usr_choice == '1':
        return display_next_menu(flow_prescription)
    elif usr_choice == '2':
        return simple_note(flow_submit_note)

def edit_cc(next_dict):
    record = Record.select(globals.patient_id)[0]
    print("\n【Condition List】")
    print(Record.select_conditions()[1])
    # TODO: exception control; validation
    # TODO: UNIQUE Constraint Exception
    edit_cond_flag = True
    while edit_cond_flag:
        if record.conditions:
            print("\n[1] Add condtion\n"
                "[2] Remove condition\n")
            add_or_delete = input("--> ")
            while add_or_delete not in ["1", "2"]:
                print("\nInvalid input, please try again!")
                add_or_delete = input("--> ")
            if add_or_delete == '1':
                print("\nPlase input the condition id you want to add (1-20)")
                cond_id = input("--> ")
                while cond_id not in [str(i) for i in range(21)]:
                    print("\nInvalid input, please try again!")
                    cond_id = input("--> ")
                else:
                    record.conditions.append(cond_id)
                    record.update()
            elif add_or_delete == '2':
                print("\nPlase input the condition id you want to remove")
                cond_id = input("--> ")
                while cond_id not in [str(i) for i in range(21)]:
                    print("\nInvalid input, please try again!")
                    cond_id = input("--> ")
                else:
                    record.conditions.remove(cond_id)
                    record.update()
        else:
            print("[1] Add condtion\n"
                "[2] End (There's no more condition to remove)\n")
            add_or_delete = input("--> ")
            while add_or_delete not in ["1", "2"]:
                print("\nInvalid input, please try again!")
                add_or_delete = input("--> ")
            if add_or_delete == '1':
                print("\nPlase input the condition id you want to add (1-20)")
                cond_id = input("--> ")
                while cond_id not in [str(i) for i in range(21)]:
                    print("\nInvalid input, please try again!")
                    cond_id = input("--> ")
                else:
                    record.conditions.append(cond_id)
                    record.update()
            elif add_or_delete == '2':
                edit_cond_flag = False
        print("\nMore change?")
        print("[1] Yes\n"
            "[2] No\n")
        more_change_cc = input("--> ")
        while more_change_cc not in ["1", "2"]:
            print("\nInvalid input, please try again!")
            more_change_cc = input("--> ")
        if more_change_cc == '2':
            edit_cond_flag = False
    else:
        print("\n【Patient Table】\n", Record.select(globals.patient_id)[2])
        print("\n【Patient Table】\n", Record.select(globals.patient_id)[4])
    return display_next_menu(next_dict)

def final_confirm_prescribe(next_dict):
    print(Prescription.select_patient(globals.patient_id)[1])
    return display_next_menu(next_dict)

def no_attend(next_dict):
    Appointment.change_status(globals.appt_id, "cancelled")
    print(Appointment.select_GP_appt(globals.usr_id))
    return display_next_menu(next_dict)

def enter_note(next_dict):
    # confirm the attendance before entering note, VALUE constraint
    Appointment.change_status(globals.appt_id, "attended")
    
    # temporarily to display the change
    print(Appointment.select_GP_appt(globals.usr_id))

    print("\nPlease enter your note")
    gp_note = input("--> ")
    Appointment(booking_id=globals.appt_id, booking_notes=gp_note).update()
    # DEBUG
    # appointment = Appointment(booking_id=globals.appt_id, gp_id=globals.usr_id)
    # appointment.booking_notes = gp_note
    # appointment.update()
    # Record.select(globals.patient_id)[0]
    # record.appointment_notes[globals.appt_id] = gp_note
    # record.update()
    print(Appointment.select(globals.appt_id)[3])

    return display_next_menu(next_dict)

# def edit_prescibe(next_dict):
#     # TODO: update/delete parts of the prescription
#     flow_dosage = {"title": "Dosage",
#                  "type": "auto",
#                  "next":(enter_dosage, flow_end)
#                 }
#     return display_next_menu(flow_dosage)

# def enter_freq(next_dict):
#     print("\nPlease enter the frequency of taking drugs")
#     print("--> ")
#     print(Prescription.select_patient(globals.patient_id)[1])
#     return display_next_menu(next_dict)

# def enter_dosage(next_dict):
#     print("\nPlease enter the dosage")
#     print("--> ")
#     return display_next_menu(next_dict)

def enter_prescription(next_dict):
    flow_drug = {"title": "Add drugs?",
                 "type": "sub",
                 "1":("Yes", enter_prescription, flow_end),
                 "2":("No", final_confirm_prescribe, flow_end)
            }
    print("\n【Drug List】")
    print(Prescription.select_drug_list()[1])
    prescription = Prescription()
    prescription.booking_id = globals.appt_id
    
    print("\nPlease enter the field for prescibed drug")
    prescription.drug_id = input("--> ")
    while prescription.drug_id not in [str(i) for i in range(1, 21)]:
        print("Invalid input, please try again!")
        print("\nPlease enter the field for prescibed drug")
        prescription.drug_id = input("--> ")
    
    prescription.prescription_expiry_date = str(date.today() + timedelta(days=14))
    print("\nPlease enter the dosage")
    prescription.drug_dosage = input("--> ")

    print("\nPlease enter the frequency of taking drugs")
    prescription.drug_frequency_dosage = input("--> ")

    prescription.insert()
    print(Prescription.select_patient(globals.patient_id)[1])

    return display_next_menu(flow_drug)

def enter_appoint_id(next_dict):
    # TODO: return to home page  
    print("\nPlease enter the id of appointment which you want to confirm attendance and edit notes")
    # TODO: √ input validation
    appt_id = input("\n--> ")
    validate_appt_id = '['+ appt_id +']'
    confirmed_id = Appointment.select_GP_confirmed(globals.usr_id)[1]['Apt. ID'].values
    while validate_appt_id not in confirmed_id:
        print("The id does not exit in the confirmed list, try again!")
        appt_id = input("\n--> ")
        validate_appt_id = '['+ appt_id +']'
    globals.appt_id = appt_id
    df = Appointment.select_GP_confirmed(globals.usr_id)[2]
    appt_id = "[" + appt_id + "]"
    patient_id = int(df.loc[df['Apt. ID'] == appt_id]['patient_id'].values)
    globals.patient_id = patient_id

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

def display_confirmed_appt(next_dict):
    no_confirmed_flag = Appointment.select_GP_confirmed(globals.usr_id)[1].index.values.size
    if no_confirmed_flag == 0:
        print("\nYour do not have any confirmed appointment!")
        return display_next_menu(flow_end)
    print("\nYour confirmed appointments: ")
    print(Appointment.select_GP_confirmed(globals.usr_id)[0])
    return display_next_menu(next_dict)

def display_pending_appt(next_dict):
    no_pending_flag = Appointment.select_GP_pending(globals.usr_id)[0].index.values.size
    if no_pending_flag == 0:
        print("\nYour do not have any pending appointment!")
        return display_next_menu(flow_end)
    else:
        print(no_pending_flag)
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

    print("\nPleas enter the id of appointment you want to confirm")
    confirm_id = input("\n--> ")
    validate_confirm_id = '['+ confirm_id +']'
    pending_id = Appointment.select_GP_pending(globals.usr_id)[0]['Apt. ID'].values
    while validate_confirm_id not in pending_id:
        print("The id does not exit in the pending list, try again!")
        confirm_id = input("\n--> ")
        validate_confirm_id = '['+ confirm_id +']'
    Appointment.change_status(confirm_id, "rejected")
    print(Appointment.select_GP_appt(globals.usr_id))

    print("\n----------------------------------------------------\n"
          "                ", "Confrim another appointment?", "\n")
    print("[ 1 ] Yes")
    print("[ 2 ] No")
    usr_choice = input("\n--> ")
    if usr_choice == '1':
        return display_pending_appt(flow_confirm_appoint)
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
    validate_confirm_id = '['+ confirm_id +']'
    pending_id = Appointment.select_GP_pending(globals.usr_id)[0]['Apt. ID'].values
    while validate_confirm_id not in pending_id:
        print("The id does not exit in the pending list, try again!")
        confirm_id = input("\n--> ")
        validate_confirm_id = '['+ confirm_id +']'
    Appointment.change_status(confirm_id, "confirmed")
    print(Appointment.select_GP_appt(globals.usr_id))

    print("\n----------------------------------------------------\n"
          "                ", "Confrim another appointment?", "\n")
    print("[ 1 ] Yes")
    print("[ 2 ] No")
    usr_choice = input("\n--> ")
    if usr_choice == '1':
        return display_pending_appt(flow_confirm_appoint)
    elif usr_choice == '2':
        return display_next_menu(next_dict)

def another_confirm_all(next_dict):
    Appointment.confirm_all_GP_pending(globals.usr_id)
    print(Appointment.select_GP_appt(globals.usr_id))
    return display_next_menu(next_dict)

def remove_timeoff(next_dict):
    flow_timeoff = {"title": "View Schedule",
                 "type": "sub",
                 "1":("Add", add_timeoff, next_dict),
                 "2":("Remove", remove_timeoff, next_dict)
                }
    start_date = utils.get_start_date()
    end_date = utils.get_end_date()
    Schedule.delete_timeoff(globals.usr_id, 'custom', start_date, end_date) 
    print("\n----------------------------------------------------\n"
          "                ", "Add or Remove a new timeoff?", "\n")
    print("[ 1 ] Yes")
    print("[ 2 ] No")
    usr_choice = input("\n--> ")
    while usr_choice not in ["1", "2"]:
        print("Invalid input, please try again!")
        usr_choice = input("\n--> ")
    else:
        if usr_choice == '1':
            return display_next_menu(flow_timeoff)
        elif usr_choice == '2':
            return display_next_menu(next_dict)

def add_timeoff(next_dict):
    flow_timeoff = {"title": "View Schedule",
                 "type": "sub",
                 "1":("Add", add_timeoff, next_dict),
                 "2":("Remove", remove_timeoff, next_dict)
                }
    start_date = utils.get_start_date()
    end_date = utils.get_end_date()
    print("\nWhat is the type of timeoff?")
    print("[ 1 ] sick leave")
    print("[ 2 ] time off")
    type_timeoff = input("--> ")
    while type_timeoff not in ["1", "2"]:
        print("Invalid input, try again!")
        type_timeoff = input("--> ")
    else:
        if type_timeoff == "1":
            Schedule.insert_timeoff(globals.usr_id, 'sick leave', start_date, end_date)
        elif type_timeoff =="2":
            Schedule.insert_timeoff(globals.usr_id, 'time off', start_date, end_date)
    print("\n----------------------------------------------------\n"
          "                ", "Add or Remove a new timeoff?", "\n")
    print("[ 1 ] Yes")
    print("[ 2 ] No")
    usr_choice = input("\n--> ")
    while usr_choice not in ["1", "2"]:
        print("Invalid input, please try again!")
        usr_choice = input("\n--> ")
    else:
        if usr_choice == '1':
            return display_next_menu(flow_timeoff)
        elif usr_choice == '2':
            return display_next_menu(next_dict)

def view_another_day(next_dict):
    flow_schedule = {"title": "View Schedule",
                 "type": "sub",
                 "1":("Day", view_another_day, next_dict),
                 "2":("Week", view_another_week, next_dict)
                }
    #call schedule class method to display the schedule by day
    print("\n----------------------------------------------------\n"
        "              Schedule View by Day\n")
    start_date = utils.get_start_date()
    print("\n【", start_date, "Morning】")
    print(Schedule.select(globals.usr_id, 'day', start_date)[2])
    print("\nDo you want to view the schedule in afternoon?")
    print("[ 1 ] Yes")
    print("[ 2 ] No")
    halfday_choice = input("--> ")
    while halfday_choice not in ["1", "2"]:
        halfday_choice = input("--> ")
    else:
        if halfday_choice == "1":
            print("\n【", start_date, "Afternoon】")
            print(Schedule.select(globals.usr_id, 'day', start_date)[3])
        print("\n" + "-" * 52 + "\n" + " " * 16 + "View Schedule\n")
        print("[ 1 ] View another schedule")
        print("[ 2 ] Manage timeoff")
        print("[ # ] Go back to main page")
        usr_choice = input("\n--> ")
        while usr_choice not in ["1", "2", "#"]:
            print("Invalid input, please try again!")
            usr_choice = input("\n--> ")
        else:
            if usr_choice == '1':
                return display_next_menu(flow_schedule)
            elif usr_choice == '2':
                return display_next_menu(next_dict)
            elif usr_choice == '#':
                return display_next_menu(main_flow_gp)

def view_another_week(next_dict):
    flow_schedule = {"title": "View Schedule",
                 "type": "sub",
                 "1":("Day", view_another_day, next_dict),
                 "2":("Week", view_another_week, next_dict)
                }
    #call schedule class method to display the schedule by week
    print("\n----------------------------------------------------\n"
        "              Schedule View by Week\n")
    start_date = utils.get_start_date()
    end_date = date.fromisoformat(start_date) + timedelta(days=6)
    print("\n【From ", start_date, " to ", end_date, " Morning】")
    print(Schedule.select(globals.usr_id, 'week', start_date)[2])
    print("\nDo you want to view the schedule in afternoon?")
    print("[ 1 ] Yes")
    print("[ 2 ] No")
    halfday_choice = input("--> ")
    while halfday_choice not in ["1", "2"]:
        halfday_choice = input("--> ")
    else:
        if halfday_choice == "1":
            print("\n【From ", start_date, " to ", end_date, " Afternoon】")
            print(Schedule.select(globals.usr_id, 'week', start_date)[3])
        print("\n" + "-" * 52 + "\n" + " " * 16 + "View Schedule\n")
        print("[ 1 ] View another schedule")
        print("[ 2 ] Manage timeoff")
        print("[ # ] Go back to main page")
        usr_choice = input("\n--> ")
        while usr_choice not in ["1", "2", "#"]:
            print("Invalid input, please try again!")
            usr_choice = input("\n--> ")
        else:
            if usr_choice == '1':
                return display_next_menu(flow_schedule)
            elif usr_choice == '2':
                return display_next_menu(next_dict)
            elif usr_choice == '#':
                return display_next_menu(main_flow_gp)

def view_records(next_dict):
    # TODO: display 10 latest clients?
    print("\n【Your All Attended Appointments】")
    print(Appointment.select_GP_attended(globals.usr_id))
    print("\nPlease enter patient id you want to search:")
    patient_id = input("--> ")
    globals.patient_id = patient_id
    print("\n【Patient Table】")
    print(Record.select(patient_id)[2])
    print("\n【Appointment & Prescription Table】")
    print(Record.select(patient_id)[4])
    return display_next_menu(next_dict)

########################## MENU NAVIGATION DICTIONARIES ######################

# Empty nested dictionary to store in tuple for last menu
# before going back to main page (for display function return parameter).
flow_end = {"title": "CONTINUE E-HEALTH OR LOGOUT ?",
              "type":"sub"}

# final confirm notes & prescription flow
# flow_final_confirm = {"title": "Final confrim notes & prescription",
#                  "type": "sub",
#                  "1":("Yes", display_next_menu, flow_end),
#                  "2":("No", edit_prescibe, flow_end)
#             }

# add drugs flow
flow_drug = {"title": "Add drugs?",
                 "type": "sub",
                 "1":("Yes", enter_prescription, flow_end),
                 "2":("No", final_confirm_prescribe, flow_end)
            }

# prescription check flow
# flow_check_prescription = {"title": "Check prescription",
#                  "type": "sub",
#                  "1":("Confirm", display_next_menu, flow_drug),
#                  "2":("Edit", edit_prescibe, flow_end)
#             }

# prescription flow
flow_prescription = {"title": "Prescription",
                 "type": "sub",
                 "1":("Enter field for prescibed drug", enter_prescription, flow_drug),
                 "2":("Skip", display_next_menu, flow_end)
                 }

# submit note flow
flow_submit_note = {"title": "Submit Note",
                 "type": "sub",
                 "1":("Submit", display_next_menu, flow_prescription),
                 "2":("No", simple_note, flow_end)
                 }

# confirm attendance flow
flow_confirm_attendance = {"title": "Confirm Attendance",
                 "type": "sub",
                 "1":("Yes", enter_note, flow_submit_note),
                 "2":("No", no_attend, flow_end)
                }

# notes flow
flow_notes = {"title": "Notes -- enter appointment id?",
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
flow_timeoff = {"title": "View Schedule",
                 "type": "sub",
                 "1":("Add", add_timeoff, flow_end),
                 "2":("Remove", remove_timeoff, flow_end)
                }
# schedule flow
flow_schedule = {"title": "View Schedule",
                "type": "sub",
                "1":("Day", view_another_day, flow_timeoff),
                "2":("Week", view_another_week, flow_timeoff)
                }

# appointment flow
flow_appointments = {"title": "Appointments",
                 "type": "sub",
                 "1":("Confirm", display_pending_appt, flow_confirm_appoint),
                 "2":("Notes", display_confirmed_appt, flow_notes)
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