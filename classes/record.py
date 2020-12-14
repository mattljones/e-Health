# record.py

# import Appointment class for use of Appointment.select_patient_previous() in Record.select()
from appointment import Appointment

# import Prescription class for use of Prescription.select_patient() in Record.select()
from prescription import Prescription

# import libraries
import sqlite3 as sql
import pandas as pd


class Record:
    '''
    Defines attributes and methods for patient medical record-related activities in different user flows.
    '''
    
    def __init__(self,
                 id_,
                 first_name,
                 last_name,
                 gender,
                 birth_date,
                 NHS_blood_donor,
                 NHS_organ_donor,
                 medical_conditions,
                 appointments,
                 prescriptions):
        self.id = id_
        self.first_name = first_name
        self.last_name = last_name
        self.gender = gender
        self.birth_date = birth_date
        self.NHS_blood_donor = NHS_blood_donor
        self.NHS_organ_donor = NHS_organ_donor
        self.medical_conditions = medical_conditions
        self.appointments = appointments
        self.prescriptions = prescriptions

    
    def update(self):
        """
        Updating a patient's medical record (technically overriding every DB attribute w/ instance values)
        """
        pass

    
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
        query_conditions = """SELECT patient_medical_condition_type_name AS 'Conditions' 
                              FROM patient_medical_condition pmc, patient_medical_condition_type pmct
                              WHERE pmc.patient_id = '{}'
                              AND pmc.patient_medical_condition_type_id = pmct.patient_medical_condition_type_id """.format(patient_id)
        conn = sql.connect("database/db_comp0066.db")
        df_attributes = pd.read_sql_query(query_attributes, conn)
        df_conditions = pd.read_sql_query(query_conditions, conn)
        df_conditions['Conditions'] = '[' + (df_conditions.index + 1).astype(str) + '] ' + df_conditions['Conditions'].astype(str)  # adding indexing
        conn.close()
        df_patient_concat = pd.concat([df_attributes, df_conditions], axis=1, join='outer')  # joining patient attributes with conditions
        df_patient_object = df_patient_concat.where(pd.notnull(df_patient_concat), None)     # setting NaN to None (for printing)
        df_patient_print = df_patient_object.to_markdown(tablefmt="grid", index=False)
        # Generating the 'appointments' dataframes
        df_apps = Appointment.select_patient_previous(patient_id)
        df_prescs = Prescription.select_patient(patient_id)[0]
        return df_patient_object, df_patient_print, df_apps, df_prescs  # df_appointments_object, df_appointments_print


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
df_obj1, df_print1, df_obj2, df_print2 = Record.select(41)
print(df_obj1)
print(df_print1)
print(df_obj2)
print(df_print2)

## Record.select_conditions()
# df_obj, df_print = Record.select_conditions()
# print(df_obj)
# print(df_print)
