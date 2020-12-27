# record.py

# import libraries
import sqlite3 as sql
import pandas as pd

# Switching path to master to get functions from utils folder
import sys
from pathlib import Path
path_to_master_repo = Path(__file__).parents[1]
sys.path.insert(1, str(path_to_master_repo))

# import classes for use in Record.select()
from classes.appointment import Appointment    
from classes.prescription import Prescription


class Record:
    """
    Defines methods for patient medical record-related activities.
    An instance contains: 1) Patient ID 
                          2) Patient conditions (editable)
                          3) Previous appointment notes (editable)
    When a medical record is viewed, these are shown in context (across 2 DFs) 
    alongside other non-editable attributes, e.g. prescriptions.
    """
    
    def __init__(self,
                 patient_id,
                 conditions,          
                 appointment_notes):  
        self.patient_id = patient_id
        # list of patient condition IDs
        self.conditions = conditions                 
        # dictionary with pairs {booking_id : booking_notes}
        self.appointment_notes = appointment_notes   

    
    def update(self):
        """
        Updates medical record details (overrides DB w/ instance)
        """

        # Medical conditions - deleting original conditions from DB
        query_conditions_delete = """
                                  DELETE FROM patient_medical_condition
                                  WHERE patient_id = '{}'
                                  """.format(self.patient_id)
        conn = sql.connect("database/db_comp0066.db")
        c = conn.cursor()
        c.execute(query_conditions_delete)
        conn.commit()
        conn.close()

        # Medical conditions - inserting updated list of medical conditions
        conn = sql.connect("database/db_comp0066.db")
        c = conn.cursor()
        for condition in self.conditions:
            c.execute("""
                      INSERT INTO patient_medical_condition 
                      VALUES ('{}', '{}')
                      """.format(self.patient_id, 
                                 condition))
        conn.commit()
        conn.close()
        
        # Appointment notes - update to new values from instance dictionary
        conn = sql.connect("database/db_comp0066.db")
        c = conn.cursor()
        for booking_id in self.appointment_notes:
            c.execute("""
                      UPDATE booking 
                      SET booking_notes = '{}' 
                      WHERE booking_id = '{}'
                      """.format(self.appointment_notes[booking_id], 
                                 booking_id))
        conn.commit()
        conn.close()     

    
    @classmethod
    def select(cls, patient_id):
        """
        Generates an instance of the record & **2** dataframes summarising 
        relevant attributes (some editable, some not) to display in user flow.
        Instance passed to user flow for storing user-inputted values.

        Args:
            patient_id (int): ID of the patient whose records are to be viewed

        Returns: (patient = patient-centric, apps = appointment-centric)
            record_instance (instance): Used for storing future user inputs
            df_patient_object (pandas DF): Raw DF (can be searched etc.)
            df_patient_print (string): Pretty DF for printing
            df_apps_object (pandas DF): Raw DF (can be searched etc.)
            df_apps_print (string): Pretty DF for printing
        """        

        # 1 - GENERATING 'PATIENT' DATAFRAMES
        query_attributes = """
                           SELECT patient_id AS 'ID', 
                                  patient_first_name AS 'First Name', 
                                  patient_last_name AS 'Last Name', 
                                  patient_gender AS 'Gender',
                                  patient_birth_date AS 'Birth Date', 
                                  patient_NHS_blood_donor AS 'Blood Donor', 
                                  patient_NHS_organ_donor AS 'Organ Donor'
                           FROM patient
                           WHERE patient_id = '{}'
                           """.format(patient_id)
        query_conditions = """
                           SELECT pmc.patient_medical_condition_type_id AS 'Cond. ID',
                                  patient_medical_condition_type_name AS 'Condition',
                                  pmc.patient_id AS 'ID' 
                           FROM patient_medical_condition pmc, patient_medical_condition_type pmct
                           WHERE pmc.patient_id = '{}'
                           AND pmc.patient_medical_condition_type_id = pmct.patient_medical_condition_type_id
                           """.format(patient_id)
        conn = sql.connect("database/db_comp0066.db")
        df_atts = pd.read_sql_query(query_attributes, conn)
        df_conds = pd.read_sql_query(query_conditions, conn)
        conn.close()
        # joining regular patient attributes with medical conditions
        df_patient_merge = pd.merge(df_atts, df_conds, how='left', on='ID')
        # replacing nulls with blank strings
        df_patient_object = df_patient_merge.where(pd.notnull(df_patient_merge), '')
        # adding line breaks between conditions so printed in one row 
        columns1 = ['ID', 'First Name', 'Last Name', 'Gender',\
                    'Birth Date', 'Blood Donor', 'Organ Donor']
        columns2 = ['Cond. ID', 'Condition']
        df_patient_breaks = df_patient_object.groupby(columns1)[columns2].agg('\n'.join).reset_index() 
        df_patient_print = df_patient_breaks.to_markdown(tablefmt="grid", index=False)

        # 2 - GENERATING 'APPOINTMENT' DATAFRAMES
        df_apps = Appointment.select_patient('previous', patient_id, 'confirmed')[0]
        df_prescs = Prescription.select_patient(patient_id)[0]
        # joining appointments with corresponding prescriptions
        df_apps_merge = pd.merge(df_apps, df_prescs, how='left', on='Apt. ID')
        # replacing nulls with blank strings & adding text wrapping for notes
        df_apps_object = df_apps_merge.where(pd.notnull(df_apps_merge), '')
        df_apps_object['Notes'] = df_apps_object['Notes'].str.wrap(20)
        # rename column to save horizontal space
        df_apps_object.rename(columns={'Apt. ID': 'ID'}, inplace=True)
        # add line breaks in columns to save horizontal space & re-format slightly
        df_apps_object['GP'] = df_apps_object['GP'].apply(lambda x: x[0:4]\
                                                    + x[4:].replace(' ', '\n', 1))
        df_apps_object['Date'] = df_apps_object['Date'].apply(lambda x: x[0:10]\
                                                        + '\n' + '(' + x[11:] + ')')
        # adding a GP ID column for use in GP user flow (GPs can only edit own notes)
        df_apps_object['GP ID'] = df_apps_object['GP'].astype(str).str[-2]
        # adding line breaks between prescriptions so printed in one row
        columns1 = ['ID', 'Date', 'GP', 'Type', 'Notes']
        columns2 = ['Drug Name', 'Dosage', 'Frequency', 'Expires']
        df_apps_breaks = df_apps_object.groupby(columns1)[columns2].agg('\n'.join).reset_index()
        df_apps_print = df_apps_breaks.to_markdown(tablefmt="grid", index=False)

        # 3 - GENERATING RECORD INSTANCE
        record_instance = cls(patient_id, df_conds['Cond. ID'].tolist(),\
                              dict(zip(df_apps['Apt. ID'], df_apps['Notes'])))
                              
        return record_instance, df_patient_object, df_patient_print, df_apps_object, df_apps_print


    @staticmethod
    def select_conditions():
        """
        Returns list of (all) medical conditions for reference.

        Returns:
            df_object (pandas DF): Raw DF (can be searched etc.)
            df_print (string): Pretty DF for printing
        """        

        query = """
                SELECT patient_medical_condition_type_id AS 'Condition ID',  
                       patient_medical_condition_type_name AS 'Condition'
                FROM patient_medical_condition_type
                """
        conn = sql.connect("database/db_comp0066.db")
        df_object = pd.read_sql_query(query, conn)
        conn.close()
        df_print = df_object.to_markdown(tablefmt="grid", index=False)
        return df_object, df_print




if __name__ == "__main__":

    ## update()
    # record_instance = Record.select(43)[0]
    # print(record_instance)
    # print(vars(record_instance))
    # record_instance.conditions.remove('6')
    # record_instance.conditions.append('10')
    # record_instance.appointment_notes['1'] = 'update_test_test'
    # record_instance.update()

    ## Record.select()
    # record_instance, df_obj1, df_print1, df_obj2, df_print2 = Record.select(43)
    # print(vars(record_instance))
    # print(df_obj1)
    # print(df_print1)
    # print(df_obj2)
    # print(df_print2)

    ## Record.select_conditions()
    # df_obj, df_print = Record.select_conditions()
    # print(df_obj)
    # print(df_print)

    pass
