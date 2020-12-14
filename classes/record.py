# record.py

# import classes for use in Record.select()
from appointment import Appointment    # Appointment.select_patient_previous() used in Record.select()
from prescription import Prescription  # Prescription.select_patient() used in Record.select()

# import libraries
import sqlite3 as sql
import pandas as pd


class Record:
    '''
    Defines attributes and methods for patient medical record-related activities in different user flows.
    '''
    
    def __init__(self,
                 patient_id,
                 conditions,          
                 appointment_notes):  
        self.patient_id = patient_id
        self.conditions = conditions                 # list of patient condition IDs
        self.appointment_notes = appointment_notes   # dictionary with pairs {booking_id : booking_notes}

    
    def update(self):
        """
        Updating a patient's medical record (technically overriding every DB attribute w/ values from instance DFs)
        """
        # Medical conditions - deleting patient medical conditions from database
        query_conditions_delete = """DELETE FROM patient_medical_condition
                                     WHERE patient_id = '{}'""".format(self.patient_id)
        conn = sql.connect("database/db_comp0066.db")
        c = conn.cursor()
        c.execute(query_conditions_delete)
        conn.commit()
        conn.close()
        # Medical conditions - inserting updated list of medical conditions
        conn = sql.connect("database/db_comp0066.db")
        c = conn.cursor()
        for condition in self.conditions:
            c.execute("""INSERT INTO patient_medical_condition 
                         VALUES ('{}', '{}')""".format(self.patient_id, 
                                                       condition))
        conn.commit()
        conn.close()
        # Appointment notes - updating notes to new values from instance dictionary
        conn = sql.connect("database/db_comp0066.db")
        c = conn.cursor()
        for booking_id in self.appointment_notes:
            c.execute("""UPDATE booking 
                         SET booking_notes = '{}', 
                         WHERE booking_id = '{}'""".format(self.appointment_notes[booking_id], 
                                                           booking_id))
        conn.commit()
        conn.close()     

    
    @classmethod
    def select(cls, patient_id):
        """
        Generating an instance of a record to later update attributes based on user input (& also returning a DF to display in user flow)
        """
        # Generating the 'patient' dataframes
        query_attributes = """SELECT patient_id AS 'Patient ID', 
                                     patient_first_name AS 'First Name', 
                                     patient_last_name AS 'Last Name', 
                                     patient_gender AS 'Gender',
                                     patient_birth_date AS 'Birth Date', 
                                     patient_NHS_blood_donor AS 'NHS Blood Donor', 
                                     patient_NHS_organ_donor AS 'NHS Organ Donor'
                              FROM patient
                              WHERE patient_id = '{}'""".format(patient_id)
        query_conditions = """SELECT pmc.patient_medical_condition_type_id AS 'Condition ID',
                                     patient_medical_condition_type_name AS 'Condition' 
                              FROM patient_medical_condition pmc, patient_medical_condition_type pmct
                              WHERE pmc.patient_id = '{}'
                              AND pmc.patient_medical_condition_type_id = pmct.patient_medical_condition_type_id """.format(patient_id)
        conn = sql.connect("database/db_comp0066.db")
        df_attributes = pd.read_sql_query(query_attributes, conn)
        df_conditions = pd.read_sql_query(query_conditions, conn)
        conn.close()
        df_patient_concat = pd.concat([df_attributes, df_conditions], axis=1, join='outer')  # joining regular patient attributes with medical conditions
        df_patient_object = df_patient_concat.where(pd.notnull(df_patient_concat), None)     # setting NaN to None (for printing)
        df_patient_print = df_patient_object.to_markdown(tablefmt="grid", index=False)
        # Generating the 'appointments' dataframes
        df_apps = Appointment.select_patient_previous(patient_id)
        df_prescs = Prescription.select_patient(patient_id)[1]
        # Generating the record instance
        record_instance = cls(patient_id, df_conditions['Condition ID'].tolist(), None)
        return record_instance, df_patient_object, df_patient_print, df_apps, df_prescs      # df_appointments_object, df_appointments_print


    @staticmethod
    def select_conditions():
        """
        Returns a list of all possible medical conditions for reference when updating patient records.
        """
        query = """SELECT patient_medical_condition_type_id AS 'Condition ID',  
                          patient_medical_condition_type_name AS 'Condition'
                   FROM patient_medical_condition_type"""
        conn = sql.connect("database/db_comp0066.db")
        df_object = pd.read_sql_query(query, conn)
        conn.close()
        df_print = df_object.to_markdown(tablefmt="grid", index=False)
        return df_object, df_print




## CODE TESTING/DEMONSTRATION

## update()

# Record.select()
record_instance, df_obj1, df_print1, df_obj2, df_print2 = Record.select(43)
print(vars(record_instance))
print(df_obj1)
print(df_print1)
print(df_obj2)
print(df_print2)

## Record.select_conditions()
# df_obj, df_print = Record.select_conditions()
# print(df_obj)
# print(df_print)
