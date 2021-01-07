# gp_flow.py

# library imports 
from pathlib import Path
import sys
from datetime import date
from datetime import timedelta

# Change python path for customized pakcage imports
p = Path(__file__).parents[1]
sys.path.insert(1, str(p))

# import utility methods from the 'system' package
from system import utils
# import class methods from "classes" package
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
    """[summary]

    Args:
        next_dict (dict): [description]

    Returns:
        [type]: [description]
    """
    record = Record.select(globals.patient_id)[0]
    print("\nPlease input the appointment id of the notes you want to change")
    # TODO: validate the input
    apt_id = input("--> ")
    print("\nPlease input the new note")
    new_note = input("--> ")
    record.appointment_notes[apt_id] = new_note
    record.update()
    print(Record.select(globals.patient_id)[4])
    return display_next_menu(next_dict)

def simple_note(next_dict):
    flow_submit_note = {"title": "SUBMIT NOTES ?",
                 "type": "sub",
                 "1":("Yes", display_next_menu, flow_prescription),
                 "2":("No", simple_note, flow_prescription)
                 }

    print("\nPlease input the new note")
    new_note = input("--> ")
    Appointment(booking_id=globals.appt_id, booking_notes=new_note).update()
    print(Appointment.select(globals.appt_id)[3])

    print("\n----------------------------------------------------\n"
        "                ", "Submit Notes?", "\n")
    print("[ 1 ] Yes")
    print("[ 2 ] No")
    usr_choice = input("\n--> ")
    while usr_choice not in ["1", "2"]:
        print("\n\U00002757 Invalid input, please try again!")
        usr_choice = input("\n--> ")
    if usr_choice == '1':
        return display_next_menu(flow_prescription)
    elif usr_choice == '2':
        return simple_note(flow_submit_note)

def edit_cc(next_dict):
    record = Record.select(globals.patient_id)[0]
    print("\n【Condition List】")
    print(Record.select_conditions()[1])
    edit_cond_flag = True
    while edit_cond_flag:
        if record.conditions:
            print("\n[ 1 ] Add condition\n"
                "[ 2 ] Remove condition\n")
            add_or_delete = input("--> ")
            while add_or_delete not in ["1", "2"]:
                print("\n\U00002757 Invalid input, please try again!")
                add_or_delete = input("--> ")
            if add_or_delete == '1':
                print("\nPlease enter the id of the condition you want to add")
                cond_id = input("--> ")
                # input validation
                while cond_id not in [str(i) for i in range(21)] or cond_id in record.conditions:
                    print("\n\U00002757 Invalid input or duplicated id, please try again!")
                    cond_id = input("--> ")
                else:
                    record.conditions.append(cond_id)
                    record.update()
                    print("The condition (id=" + cond_id + ") has been successfully added!")
            elif add_or_delete == '2':
                print("\nPlease enter the id of the condition you want to remove")
                cond_id = input("--> ")
                while cond_id not in [str(i) for i in range(21)] or cond_id not in record.conditions:
                    print("\n\U00002757 Invalid input, please try again!")
                    cond_id = input("--> ")
                else:
                    record.conditions.remove(cond_id)
                    record.update()
                    print("The condition (id=" + cond_id + ") has been successfully removed!\n")
        
        # if the condition cell is empty
        else:
            print("[ 1 ] Add condition\n"
                "[ 2 ] End (Patient currently has no conditions to remove)\n")
            add_or_end = input("--> ")
            while add_or_end not in ["1", "2"]:
                print("\n\U00002757 Invalid input, please try again!")
                add_or_end = input("--> ")
            if add_or_end == '1':
                print("\nPlease enter the id of the condition you want to add")
                cond_id = input("--> ")
                while cond_id not in [str(i) for i in range(21)] or cond_id in record.conditions:
                    print("\n\U00002757 Invalid input or duplicated id, please try again!")
                    cond_id = input("--> ")
                else:
                    record.conditions.append(cond_id)
                    record.update()
                    print("The condition (id=" + cond_id + ") has been successfully added!")
            elif add_or_end == '2':
                edit_cond_flag = False
                continue
        
        print("\nAdd or remove another condition?")
        print("[ 1 ] Yes\n"
            "[ 2 ] No\n")
        more_change_cc = input("--> ")
        while more_change_cc not in ["1", "2"]:
            print("\n\U00002757 Invalid input, please try again!")
            more_change_cc = input("--> ")
        if more_change_cc == '2':
            edit_cond_flag = False
    else:
        print("\n【Patient Table】")
        print(Record.select(globals.patient_id)[2])
        if Record.select(globals.patient_id)[3].index.values.size == 0:
            pass
        else:
            print("\n【Appointment & Prescription Table】")
            print(Record.select(globals.patient_id)[4])
    return display_next_menu(next_dict)

def final_confirm_prescribe(next_dict):
    print(Prescription.select_patient(globals.patient_id)[1])
    return display_next_menu(next_dict)

def no_attend(next_dict):
    Appointment.change_status(globals.appt_id, "cancelled")
    print("\nAppointment " + str(globals.appt_id) + " has been successfully cancelled!\n")
    # TODO: delete at the final version
    # print(Appointment.select_GP_appt(globals.usr_id))
    return display_next_menu(next_dict)

def enter_note(next_dict):
    # confirm the attendance before entering note, VALUE constraint
    Appointment.change_status(globals.appt_id, "attended")
    # TODO: delet in the final version
    # print(Appointment.select_GP_appt(globals.usr_id))
    print("\nPlease enter your notes on the appointment")
    gp_note = input("--> ")
    Appointment(booking_id=globals.appt_id, booking_notes=gp_note).update()
    print(Appointment.select(globals.appt_id)[3])

    return display_next_menu(next_dict)

def enter_prescription(next_dict):
    flow_drug = {"title": "ADD ANOTHER PRESCRIPTION ?",
                 "type": "sub",
                 "1":("Yes", enter_prescription, flow_end),
                 "2":("No", final_confirm_prescribe, flow_end)
            }
    print("\n【Drug List】")
    print(Prescription.select_drug_list()[1])
    prescription = Prescription()
    prescription.booking_id = globals.appt_id
    
    print("\nPlease enter the drug id")
    prescription.drug_id = input("--> ")
    while prescription.drug_id not in [str(i) for i in range(1, 21)]:
        print("\U00002757 Invalid input, please try again!")
        print("\nPlease enter the drug id")
        prescription.drug_id = input("--> ")
    
    prescription.prescription_expiry_date = str(date.today() + timedelta(days=14))
    print("\nPlease enter the dosage")
    prescription.drug_dosage = input("--> ")

    print("\nPlease enter the frequency of taking drugs")
    prescription.drug_frequency_dosage = input("--> ")

    prescription.insert()

    print("\nThe prescription has been successfully added!")
    print("")
    print(Prescription.select_patient(globals.patient_id)[1])

    return display_next_menu(flow_drug)

def enter_appoint_id(next_dict):
    # TODO: return to home page  
    print("\nPlease enter an appointment ID")
    appt_id = input("\n--> ")
    while appt_id == "" or appt_id.isspace() == True:
        print("\n\U00002757 Invalid input, please try again!")
        appt_id = input("\n--> ")
    confirmed_id = [str(i) for i in Appointment.select_GP_confirmed(globals.usr_id)[1]['Apt. ID'].values]
    while appt_id not in confirmed_id:
        print("\nThe id does not exit in the confirmed list, try again!")
        appt_id = input("\n--> ")
    globals.appt_id = int(appt_id)
    df = Appointment.select_GP_confirmed(globals.usr_id)[2]
    patient_id = int(df.loc[df['Apt. ID'] == int(appt_id)]['patient_id'].values)
    globals.patient_id = patient_id

    return display_next_menu(next_dict)

############################ SEQUENTIAL STEPS MENUS ########################

def correct_note_change(next_dict):
    flow_record_edit = {"title": "EDIT WHAT PART OF THE RECORDS ?",
                 "type": "sub",
                 "1":("Chronic conditions", edit_cc, flow_confirm_change),
                 "2":("Notes", edit_notes, flow_confirm_change)
                }
    return display_next_menu(flow_record_edit)

def correct_cc_change(next_dict):
    flow_cc_edit = {"title": "EDIT CONDITION",
                 "type": "auto",
                 "next":(edit_cc, flow_only_cc_confirm)
                }
    return display_next_menu(flow_cc_edit)

# TODO: booking id input validation

def display_confirmed_appt(next_dict):
    no_confirmed_flag = Appointment.select_GP_confirmed(globals.usr_id)[1].index.values.size
    if no_confirmed_flag == 0:
        print("\nYour do not have any confirmed appointment before now!")
        return display_next_menu(flow_end)
    print("\n【Your confirmed appointments before now (sorted by start time)】")
    print(Appointment.select_GP_confirmed(globals.usr_id)[0])
    return display_next_menu(next_dict)

def display_pending_appt(next_dict):
    no_pending_flag = Appointment.select_GP_pending(globals.usr_id)[0].index.values.size
    if no_pending_flag == 0:
        print("\nYour do not have any pending appointment!")
        return display_next_menu(flow_end)
    else:
        print("\n【Your pending appointments】")
        print(Appointment.select_GP_pending(globals.usr_id)[1])
        return display_next_menu(next_dict)

def another_confirm_rej(next_dict):
    flow_confirm_appoint = {"title": "CONFIRM APPOINTMENTS",
                 "type": "sub",
                 "1":("Confirm all", another_confirm_all, next_dict),
                 "2":("Confirm one", another_confirm_one, next_dict),
                 "3":("Reject one", another_confirm_rej, next_dict)
                }

    print("\nPlease enter the id of appointment you want to reject")
    confirm_id = input("\n--> ")
    pending_id = Appointment.select_GP_pending(globals.usr_id)[0]['Apt. ID'].values
    while confirm_id not in str(pending_id):
        print("The id does not exist in the pending list, try again!")
        confirm_id = input("\n--> ")
    print("\nPleas give the reason of rejection")
    reason = input("\n--> ")
    while reason == "" or reason.isspace() == True:
        print("\U00002757 Invalid input, please try again!")
        reason = input("\n--> ")
    Appointment.change_status(confirm_id, "rejected", reason)
    print("\nAppointment " + confirm_id + " has been successfully rejected!")
    # TODO: delete at the final version
    # print(Appointment.select_GP_appt(globals.usr_id))

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
    flow_confirm_appoint = {"title": "CONFIRM APPOINTMENTS",
                 "type": "sub",
                 "1":("Confirm all", another_confirm_all, next_dict),
                 "2":("Confirm one", another_confirm_one, next_dict),
                 "3":("Reject one", another_confirm_rej, next_dict)
                }

    print("\nPleas enter the id of appointment you want to confirm")
    confirm_id = input("\n--> ")
    pending_id = Appointment.select_GP_pending(globals.usr_id)[0]['Apt. ID'].values
    while confirm_id not in str(pending_id):
        print("The id does not exit in the pending list, try again!")
        confirm_id = input("\n--> ")
    Appointment.change_status(confirm_id, "confirmed")
    print("\nAppointment " + confirm_id + " has been successfully confirmed!")
    # TODO: delete at the final version
    # print(Appointment.select_GP_appt(globals.usr_id))

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
    # TODO: delete at the final version
    # print(Appointment.select_GP_appt(globals.usr_id))
    return display_next_menu(next_dict)

def remove_timeoff(next_dict):
    flow_timeoff = {"title": "MANAGE TIMEOFF",
                 "type": "sub",
                 "1":("Add", add_timeoff, next_dict),
                 "2":("Remove", remove_timeoff, next_dict)
                }
    start_date = utils.get_start_date()
    end_date = utils.get_end_date()
    Schedule.delete_timeoff(globals.usr_id, 'custom', None, start_date, end_date)
    print("\nThe timeoff has been successfully removed!")
    print("\n----------------------------------------------------\n"
          "                ", "Add or Remove more timeoff?", "\n")
    print("[ 1 ] Yes")
    print("[ 2 ] No")
    usr_choice = input("\n--> ")
    while usr_choice not in ["1", "2"]:
        print("\U00002757 Invalid input, please try again!")
        usr_choice = input("\n--> ")
    else:
        if usr_choice == '1':
            return display_next_menu(flow_timeoff)
        elif usr_choice == '2':
            return display_next_menu(next_dict)

def add_timeoff(next_dict):
    flow_timeoff = {"title": "VIEW SCHEDULE",
                 "type": "sub",
                 "1":("Add", add_timeoff, next_dict),
                 "2":("Remove", remove_timeoff, next_dict)
                }
    print("\nWhat is the type of timeoff?")
    print("[ 1 ] sick leave")
    print("[ 2 ] time off")
    type_timeoff = input("--> ")
    while type_timeoff not in ["1", "2"]:
        print("\U00002757 Invalid input, try again!")
        type_timeoff = input("--> ")
    start_date = utils.get_start_date()
    end_date = utils.get_end_date()
    if type_timeoff == "1":
        while Schedule.check_timeoff_conflict(globals.usr_id, start_date, end_date)[0] == True:
            print("\n\U00002757 You have appointments during the period and cannot add timeoff!")
            print("\n【Conflicts Table】")
            print(Schedule.check_timeoff_conflict(globals.usr_id, start_date, end_date)[2])
            print("\nDo yo still want to add timeoff?")
            print("[ 1 ] Yes")
            print("[ 2 ] No")
            yes_or_no = input("--> ")
            while yes_or_no not in ["1", "2"]:
                print("\n\U00002757 Invalid entry, please try again and enter your choice.")
                yes_or_no = input("\n--> ")
            if yes_or_no == "1":
                start_date = utils.get_start_date()
                end_date = utils.get_end_date()
            elif yes_or_no == "2":
                return display_next_menu(main_flow_gp)
        else:
            Schedule.insert_timeoff(globals.usr_id, 'sick leave', start_date, end_date)
    elif type_timeoff =="2":
        while Schedule.check_timeoff_conflict(globals.usr_id, start_date, end_date)[0] == True:
            print("\n\U00002757 You have appointments during the period and cannot add timeoff!")
            print("\n【Conflicts Table】")
            print(Schedule.check_timeoff_conflict(globals.usr_id, start_date, end_date)[2])
            print("\nDo yo still want to add timeoff?")
            print("[ 1 ] Yes")
            print("[ 2 ] No")
            yes_or_no = input("\n--> ")
            while yes_or_no not in ["1", "2"]:
                print("\n\U00002757 Invalid entry, please try again and enter your choice.")
                yes_or_no = input("--> ")
            if yes_or_no == "1":
                start_date = utils.get_start_date()
                end_date = utils.get_end_date()
            elif yes_or_no == "2":
                return display_next_menu(main_flow_gp)
        else:
            Schedule.insert_timeoff(globals.usr_id, 'time off', start_date, end_date)
    print("\nThe timeoff has been successfully added!")
    print("\n----------------------------------------------------\n"
          "                ", "Add or Remove more timeoff?", "\n")
    print("[ 1 ] Yes")
    print("[ 2 ] No")
    usr_choice = input("\n--> ")
    while usr_choice not in ["1", "2"]:
        print("\U00002757 Invalid input, please try again!")
        usr_choice = input("\n--> ")
    else:
        if usr_choice == '1':
            return display_next_menu(flow_timeoff)
        elif usr_choice == '2':
            return display_next_menu(next_dict)

def view_another_day(next_dict):
    flow_schedule = {"title": "VIEW SCHEDULE",
                 "type": "sub",
                 "1":("Day", view_another_day, next_dict),
                 "2":("Week", view_another_week, next_dict)
                }
    #call schedule class method to display the schedule by day
    print("\n----------------------------------------------------\n"
        "              Schedule View by Day\n")
    start_date = utils.get_start_date()
    print("\n【"+ start_date + " Morning】")
    print(Schedule.select(globals.usr_id, 'day', start_date)[2])
    print("\nDo you want to view the schedule for the afternoon?")
    print("[ 1 ] Yes")
    print("[ 2 ] No")
    halfday_choice = input("\n--> ")
    while halfday_choice not in ["1", "2"]:
        print("\U00002757 Invalid input, please try again!")
        halfday_choice = input("--> ")
    else:
        if halfday_choice == "1":
            print("\n【" + start_date + " Afternoon】")
            print(Schedule.select(globals.usr_id, 'day', start_date)[3])
        print("\n" + "-" * 52 + "\n" + " " * 16 + "View schedule\n")
        print("[ 1 ] View schedule main page")
        print("[ 2 ] Manage timeoff")
        print("[ # ] Go back to main page")
        usr_choice = input("\n--> ")
        while usr_choice not in ["1", "2", "#"]:
            print("\U00002757 Invalid input, please try again!")
            usr_choice = input("\n--> ")
        else:
            if usr_choice == '1':
                return display_next_menu(flow_schedule)
            elif usr_choice == '2':
                return display_next_menu(next_dict)
            elif usr_choice == '#':
                return display_next_menu(main_flow_gp)

def view_another_week(next_dict):
    flow_schedule = {"title": "VIEW SCHEDULE",
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
    print("\nDo you want to view the schedule for the afternoon?")
    print("[ 1 ] Yes")
    print("[ 2 ] No")
    halfday_choice = input("--> ")
    while halfday_choice not in ["1", "2"]:
        halfday_choice = input("--> ")
    else:
        if halfday_choice == "1":
            print("\n【From ", start_date, " to ", end_date, " Afternoon】")
            print(Schedule.select(globals.usr_id, 'week', start_date)[3])
        print("\n" + "-" * 52 + "\n" + " " * 16 + "View schedule\n")
        print("[ 1 ] View schedule main page")
        print("[ 2 ] Manage timeoff")
        print("[ # ] Go back to main page")
        usr_choice = input("\n--> ")
        while usr_choice not in ["1", "2", "#"]:
            print("\U00002757 Invalid input, please try again!")
            usr_choice = input("\n--> ")
        else:
            if usr_choice == '1':
                return display_next_menu(flow_schedule)
            elif usr_choice == '2':
                return display_next_menu(next_dict)
            elif usr_choice == '#':
                return display_next_menu(main_flow_gp)

def view_records(next_dict):
    # display today's schedule
    date_time_now = date.today().strftime("%Y-%m-%d")
    df = Schedule.select(globals.usr_id, 'day', date_time_now)[0]
    without_lunch = df[df['Status'] != "LUNCH"]
    final_df = without_lunch[without_lunch['Status'] != ""]
    # TODO: if the schedule is empty, could the gp search?
    if final_df.index.values.size == 0:
        print("\nYour do not have any appointment today!")
        return display_next_menu(flow_end)
    print("\n【Today's Appointments】\n")
    print(final_df.to_markdown(tablefmt="grid", index=False))

    print("\nPlease enter a patient id (today's patients above for reference)")
    # input validation
    patient_id = input("--> ")
    while patient_id.isdigit() == False or patient_id == " " or patient_id.isspace()== True or Record.select(patient_id)[1].index.values.size == 0:
        print("\n\U00002757 Invalid input or non-existent patient id above, please try again!")
        patient_id = input("--> ")
    globals.patient_id = patient_id
    print("\n【Patient Table】")
    print(Record.select(patient_id)[2])
    if Record.select(patient_id)[3].index.values.size == 0:
        print("\nThis patient does not has any attended appointment, so there is no 【Prescription Table】 and you cannot edit the notes!")
        return display_next_menu(flow_only_cc_edit)
    else:
        print("\n【Appointment & Prescription Table】")
        print(Record.select(patient_id)[4])
    return display_next_menu(next_dict)

########################## MENU NAVIGATION DICTIONARIES ######################

# Empty nested dictionary to store in tuple for last menu
# before going back to main page (for display function return parameter).
flow_end = {"title": "CONTINUE E-HEALTH OR LOGOUT ?",
              "type":"sub"}

# add drugs flow
flow_drug = {"title": "ADD ANOTHER PRESCRIPTION ?",
                 "type": "sub",
                 "1":("Yes", enter_prescription, flow_end),
                 "2":("No", final_confirm_prescribe, flow_end)
            }

# prescription flow
flow_prescription = {"title": "ADD A PRESCRIPTION ?",
                 "type": "sub",
                 "1":("Yes", enter_prescription, flow_drug),
                 "2":("No", display_next_menu, flow_end)
                 }

# submit note flow
flow_submit_note = {"title": "SUBMIT CHANGES ?",
                 "type": "sub",
                 "1":("Yes", display_next_menu, flow_prescription),
                 "2":("No", simple_note, flow_end)
                 }

# confirm patient attendance flow
flow_confirm_attendance = {"title": "CONFIRM PATIENT ATTENDANCE ?",
                 "type": "sub",
                 "1":("Yes", enter_note, flow_submit_note),
                 "2":("No", no_attend, flow_end)
                }

# notes flow
flow_notes = {"title": "POST-APPOINTMENT STEPS",
              "type": "auto",
              "next":(enter_appoint_id, flow_confirm_attendance)
            }

# confirm appointment flow
flow_confirm_appoint = {"title": "CONFIRM APPOINTMENTS",
                "type": "sub",
                "1":("Confirm all", another_confirm_all, flow_end),
                "2":("Confirm one", another_confirm_one, flow_end),
                "3":("Reject one", another_confirm_rej, flow_end)
                }

# timeoff flow
flow_timeoff = {"title": "MANAGE TIMEOFF",
                 "type": "sub",
                 "1":("Add", add_timeoff, flow_end),
                 "2":("Remove", remove_timeoff, flow_end)
                }
# schedule flow
flow_schedule = {"title": "VIEW SCHEDULE",
                "type": "sub",
                "1":("Day", view_another_day, flow_timeoff),
                "2":("Week", view_another_week, flow_timeoff)
                }

# appointment flow
flow_appointments = {"title": "APPOINTMENTS",
                 "type": "sub",
                 "1":("Confirm", display_pending_appt, flow_confirm_appoint),
                 "2":("Notes", display_confirmed_appt, flow_notes)
                }

flow_confirm_change = {"title": "SUBMIT CHANGES ?",
                 "type": "sub",
                 "1":("Yes", display_next_menu, flow_end),
                 "2":("No (edit this patient's records further)", correct_note_change, flow_end)
                }

flow_only_cc_confirm = {"title": "SUBMIT CHANGES ?",
                 "type": "sub",
                 "1":("Yes", display_next_menu, flow_end),
                 "2":("No (edit this patient's condition further)", correct_cc_change, flow_end)
                }


flow_only_cc_edit = {"title": "DO YOU WANT TO EDIT THE CONDITIONS OF THIS PATIENT ?",
                 "type": "sub",
                 "1":("Yes", edit_cc, flow_only_cc_confirm),
                 "2":("No", display_next_menu, flow_end)
                }

flow_record_edit = {"title": "EDIT WHAT PART OF THE RECORDS ?",
                 "type": "sub",
                 "1":("Chronic conditions", edit_cc, flow_confirm_change),
                 "2":("Notes", edit_notes, flow_confirm_change)
                }

# flow of decision on editing records of a patient
flow_record_choose = {"title": "EDIT RECORDS OF THIS PATIENT ?",
                 "type": "sub",
                 "1":("Yes", display_next_menu, flow_record_edit),
                 "2":("No", display_next_menu, flow_end)
                }

# records flow
flow_records = {"title": "RECORDS",
                 "type": "sub",
                 "1":("Search patient records", view_records, flow_record_choose)
                }

# gp main page dictionary
main_flow_gp = {"title": "GP MAIN MENU",
                "type":"main",
                "1":("View schedule", display_next_menu, flow_schedule),
                "2":("Manage timeoff", display_next_menu, flow_timeoff),
                "3":("Manage appointments", display_next_menu, flow_appointments),
                "4":("Manage patient records", display_next_menu, flow_records)}