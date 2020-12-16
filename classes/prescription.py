# prescription.py

# import libraries
import pandas as pd
import sqlite3 as sql
import datetime
from system import utils as u


class Prescription:
    '''
    Class defining all 'prescription' related methods.
    '''

    def __init__(self):
        self.prescription_expiry_date = ""
        self.drug_id = ""
        self.drug_dosage = ""
        self.drug_frequency_dosage = ""
        self.booking_id = ""

    def insert(self):  # INSERT - INSTANCE
        '''
        Insertion of a prescription into the prescription table
        :return: no return, as prescription is inserted in prescription table
        '''
        insert_query = """
                        INSERT INTO prescription
                        VALUES (NULL, '{}', '{}', {}, '{}', '{}', {});""".format(
            datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            self.prescription_expiry_date,
            self.drug_id,
            self.drug_dosage,
            self.drug_frequency_dosage,
            self.booking_id)

        u.db_execute(insert_query)

    @staticmethod  # SELECT_list - STATIC
    def select_drug_list():
        '''
        Select all drugs from the drug table
        :return: DataFrame with drugs list
        '''

        # Initialize query
        select_drug_query = '''
                            SELECT drug_id AS "Drug ID", drug_name AS "Drug Name"
                            FROM drug'''
        # Execute query
        df_object = u.db_read_query(select_drug_query)

        # Produce df_print
        df_print = df_object.to_markdown(tablefmt="grid", index=False)

        return df_object, df_print

    @staticmethod  # SELECT patient - STATIC
    def select_patient(patient_id):
        '''
        Static Method that gets values from patient table based on a specific patient_id that was indicated
        :param patient_for_prescription: patient_id from database
        :return:
        '''

        # Initialize query
        select_patient_query = '''
                                    SELECT
                                        drug_name AS "Drug Name",
                                        drug_dosage AS "Drug Dosage",
                                        drug_frequency_dosage AS "Intake Frequency",
                                        prescription_expiry_date AS "Expiry Date",
                                        p.booking_id AS "Apt. ID"
                                    FROM
                                        prescription AS p
                                    LEFT JOIN
                                        booking AS b ON p.booking_id = b.booking_id
                                    LEFT JOIN
                                        drug AS d ON p.drug_id = d.drug_id
                                    WHERE
                                        patient_id = {}
                                    AND
                                        booking_status = 'confirmed';'''.format(patient_id)
        # Execute query
        df_object = u.db_read_query(select_patient_query)

        # Produce df_print
        df_print = df_object.to_markdown(tablefmt="grid", index=False)

        return df_object, df_print


### DEVELOPMENT ###

if __name__ == "__main__":
    pass

### TESTING ###
## testing prescription
# call classes
new_prescription = Prescription()
# see patient records
df = new_prescription.select_patient(22)[1]
# see drug list
df = new_prescription.select_drug_list()[1]


## Insert new prescription
# ask user to input the expiry date
# new_prescription.prescription_expiry_date = input("Enter the expiry date (Format: YYYY-MM-DD): ")
# new_prescription.drug_id = int(input("Enter the drug id: "))
# new_prescription.booking_id = int(input("Enter the booking id: "))
# new_prescription.drug_dosage = input("Enter the drug dosage: ")
# new_prescription.drug_frequency_dosage = input("Enter the intake frequency: ")
# new_prescription.insert()
#
# new_prescription.prescription_expiry_date = '2020-12-12'
# new_prescription.drug_id = 1
# new_prescription.booking_id = 2
# new_prescription.drug_dosage = '12 mg'
# new_prescription.drug_frequency_dosage = 'hallo'
# new_prescription.insert()
