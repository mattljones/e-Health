# prescription.py

# import libraries
import pandas as pd
import sqlite3 as sql
import datetime


class Prescription:
    '''
    Class defining all 'prescription' related methods.
    '''

    def __init__(self):
        self.prescription_id = ""
        self.prescription_timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.prescription_expiry_date = ""
        self.drug_id = ""
        self.drug_dosage = ""
        self.drug_frequency_dosage = ""
        self.booking_id = ""

    def insert(self):  # INSERT - INSTANCE
        '''
        Insertion of a prescription into the prescription table
        :return: none --> prescription is inserted in prescription table
        '''
        conn = sql.connect("database/db_comp0066.db")
        c = conn.cursor()
        c.execute("INSERT INTO prescription VALUES (NULL, ?, ?, ?, ?, ?, ?);",
                  (self.prescription_timestamp,
                   self.prescription_expiry_date,
                   self.drug_id,
                   self.drug_dosage,
                   self.drug_frequency_dosage,
                   self.booking_id)
                  )

        conn.commit()
        conn.close()

    @staticmethod  # SELECT_list - STATIC
    def select_drug_list():
        '''
        Static Method that returns a list of the drug table
        :return: df_drug_list in tabulate format
        '''
        conn = sql.connect("database/db_comp0066.db")

        query = '''
                    SELECT drug_id AS "ID", drug_name AS "Drug Name"
                    FROM drug'''

        df_drug_list = pd.read_sql_query(query, conn)

        conn.close()

        df_formatted = df_drug_list.to_markdown(tablefmt="grid", index=True)

        return df_formatted

    @staticmethod  # SELECT patient - STATIC
    def select_prescription_patient(patient_id):
        '''
        Static Method that gets values from patient table based on a specific patient_id that was indicated
        :param patient_for_prescription: patient_id from database
        :return:
        '''
        conn = sql.connect("database/db_comp0066.db")

        query = '''
                    SELECT prescription_timestamp AS "Prescription Creation Date", prescription_expiry_date AS "Prescription Expiry Date", drug_name AS "Drug Name", drug_dosage AS "Drug Dosage", drug_frequency_dosage AS "Intake Frequency"
                    FROM prescription AS p
                    LEFT JOIN booking AS b ON p.booking_id = b.booking_id
                    LEFT JOIN drug AS d ON p.drug_id = d.drug_id
                    WHERE patient_id = {}
                    AND booking_status = "confirmed"'''.format(patient_id)



        df_patient_prescription = pd.read_sql_query(query, conn)
        conn.close()

        df_formatted = df_patient_prescription.to_markdown(tablefmt="grid", index=True)

        return df_formatted


### TESTING ###
## testing prescription
# call classes
new_prescription = Prescription()
#see patient records
new_prescription.select_prescription_patient(22)
# see drug list
new_prescription.select_drug_list()


## Insert new prescription
# ask user to input the expiry date
new_prescription.prescription_expiry_date = input("Enter the expiry date (Format: YYYY-MM-DD): ")
new_prescription.drug_id = int(input("Enter the drug id: "))
new_prescription.booking_id = int(input("Enter the booking id: "))
new_prescription.drug_dosage = input("Enter the drug dosage: ")
new_prescription.drug_frequency_dosage = input("Enter the intake frequency: ")
new_prescription.insert()

### DEVELOPMENT ###

if __name__ == "__main__":
    pass
