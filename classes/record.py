# record.py

# import libraries
import pandas as pd
import sqlite3 as sql

class Record:
    '''
    Class defining all 'record' related methods.
    '''
    
    def __init__(self, status=""):
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

    
    @classmethod
    def select(cls, patient_id):
        """
        Factory method creating a Record instance from a SELECT query and returning a corresponding (transposed) dataframe.
        """
        # TO DO: think about whether an instance is actually needed here. If not > static method.
        # TO DO: consider importing and using appointment/prescription methods below
        conn = sql.connect("database/db_comp0066.db")
        df_details = pd.read_sql_query("""SELECT patient_id AS 'Patient ID', patient_first_name AS 'First Name', patient_last_name AS 'Last Name', patient_gender AS 'Gender',
                                          patient_birth_date AS 'Birth Date', patient_NHS_blood_donor AS 'NHS Blood Donor', patient_NHS_organ_donor AS 'NHS Organ Donor'
                                          FROM patient
                                          WHERE patient_id = ?""", 
                                       conn, params=(patient_id,))
        df_appointments = pd.read_sql_query("""SELECT booking_id AS 'Appointment ID', booking_start_time AS 'Time', booking_notes AS 'GP Notes', 
                                               gp_first_name AS 'GP First Name', gp_last_name AS 'GP Last Name'
                                               FROM booking, gp
                                               WHERE booking.gp_id = gp.gp_id AND patient_id = ? AND booking_status = 'confirmed'""", 
                                            conn, params=(patient_id,))
        df_prescriptions = pd.read_sql_query("""SELECT prescription_id AS 'Prescription ID', drug_name AS 'Drug', drug_dosage AS 'Dosage', drug_frequency_dosage AS 'Frequency' 
                                                FROM booking, prescription, drug
                                                WHERE booking.booking_id = prescription.booking_id AND prescription.drug_id = drug.drug_id AND patient_id = ?""", 
                                             conn, params=(patient_id,))
        conn.close()
        df_combined = pd.concat([df_appointments, df_prescriptions], axis=1, join='inner', sort=False)
        df_details_formatted = df_details.to_markdown(tablefmt="grid", index=False)
        df_combined_formatted = df_combined.to_markdown(tablefmt="grid", index=False)
        return df_details_formatted, df_combined_formatted


### DEVELOPMENT ###

if __name__ == "__main__":
    pass