# prescription.py

# import libraries
import pandas as pd
import sqlite3
import datetime

class Prescription:
    '''
    Class defining all 'prescription' related methods.
    '''

    def __init__(self):
        self.prescription_id = ""
        self.prescription_timestamp = ""
        self.prescription_expiry_date = ""
        self.drug_id = ""
        self.availability_id = ""

    def insert(self): # INSERT - INSTANCE
        conn = sqlite3.connect("database/db_comp0066.db")
        c = conn.cursor()
        c.execute("INSERT INTO prescription VALUES (NULL, ?, ?, ?, ?);",
                  (self.prescription_timestamp,
                  self.prescription_expiry_date,
                  self.drug_id,
                  self.availability_id)
                  )

        conn.commit()
        conn.close()


    @staticmethod # SELECT_list - STATIC
    ## TODO: make it speficic (1 drug based on name) and unspecific (all drugs)
    def select_drug(drug_for_prescription):
        '''
        Static Method that gets values from drug table based on a specific drug that was indicated
        Input: drug_name from database
        '''
        conn = sqlite3.connect("database/db_comp0066.db")
        drugs = pd.read_sql_query("SELECT drug_id, drug_name, drug_dosage, drug_frequency_dosage FROM drug WHERE drug_name = ?;", conn, params=(drug_for_prescription,))
        conn.close()
        return drugs

    @staticmethod # SELECT patient - STATIC
    # TODO: make it speficic (1 patient based on name) and unspecific (all patients)
    def select_patient(patient_for_prescription):
        '''
        Static Method that gets values from patient table based on a specific patient_id that was indicated
        Input: patient_id from database
        '''
        conn = sqlite3.connect("database/db_comp0066.db")
        patient = pd.read_sql_query("SELECT patient_id, patient_first_name, patient_last_name FROM patient WHERE patient_id = ?;", conn, params=(patient_for_prescription,))
        conn.close()
        return patient

## testing prescription
# call classes
new_prescription = Prescription()

# timestamp for now
new_prescription.prescription_timestamp = datetime.datetime.now()
# ask user to input the expiry date
new_prescription.prescription_expiry_date = input("Enter the expiry date (Format: YY-MM-DD): ")
# select the drug_id from select_drug
## todo: implement edge cases for drug dosage, name and frequency
# drug_name = input("Enter the drug name: ")
# drug_info = Prescription.select_drug(drug_name)
## based on 2 values below drug_info needs to be filtered
# drug_dosage =
# drug_frequency_dosage =
# finally a drug_name can be inserted into Prescription.select_drug()
new_prescription.drug_id = 1
# ask user to input the availability_id
availability_id = int(input("Enter the availability id: "))
new_prescription.availability_id = availability_id

new_prescription.insert()

### DEVELOPMENT ###

if __name__ == "__main__":
    pass
