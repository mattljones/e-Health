# patient.py

# import libraries
import sqlite3 as sql
import pandas as pd

# Switching path to master to get functions from utils folder
import sys
from pathlib import Path
path_to_master_repo = Path(__file__).parents[1]
sys.path.insert(1, str(path_to_master_repo))

# import User class for inheritance
from classes.user import User

# import GP class for use of GP.check_not_full() in Patient.change_GP()
from classes.gp import GP


class Patient(User):
    """
    Child class of 'User', inheriting shared attributes.
    Defines patient-related attributes & methods for different user flows. 
    """
    
    # password not required as no insert(): patients register themselves
    def __init__(self,
                 id_,
                 gp_id, 
                 first_name, 
                 last_name, 
                 gender, 
                 birth_date, 
                 email, 
                 registration_date, 
                 NHS_blood_donor,
                 NHS_organ_donor,
                 status):
        User.__init__(self, id_, first_name, last_name, gender, birth_date, 
                      email, None, registration_date, status) 
        self.gp_id = gp_id
        self.NHS_blood_donor = NHS_blood_donor
        self.NHS_organ_donor = NHS_organ_donor


    def update(self):
        """
        Updates a patient's details (overrides DB attributes w/ instance)
        """

        query = """
                UPDATE patient 
                SET patient_first_name = '{}', 
                    patient_last_name = '{}', 
                    patient_gender = '{}', 
                    patient_birth_date = '{}', 
                    patient_email = '{}',  
                    patient_NHS_blood_donor = '{}', 
                    patient_NHS_organ_donor = '{}', 
                    patient_status = '{}'
                WHERE patient_id = '{}'
                """.format(self.first_name, 
                           self.last_name, 
                           self.gender, 
                           self.birth_date, 
                           self.email, 
                           self.NHS_blood_donor, 
                           self.NHS_organ_donor, 
                           self.status,
                           self.id)
        conn = sql.connect("database/db_comp0066.db")
        c = conn.cursor()
        c.execute(query)
        conn.commit()
        conn.close()


    @classmethod
    def select(cls, patient_id):
        """
        Generates an instance of the patient & a dataframe summarising their 
        attributes to display in user flow.
        Instance passed to user flow for storing user-inputted values.

        Args:
            patient_id (int): ID of the patient to be viewed

        Returns:
            patient_instance (instance): Used for storing future user inputs
            df_object (pandas DF): Raw DF (can be searched etc.)
            df_print (string): Pretty DF for printing
        """

        query = """
                SELECT patient_id AS 'Patient ID', 
                       patient.gp_id,
                       gp.gp_last_name AS 'Default GP',
                       patient_first_name AS '[1] First Name', 
                       patient_last_name AS '[2] Last Name', 
                       patient_gender AS '[3] Gender',
                       patient_birth_date AS '[4] Birth Date', 
                       patient_email AS '[5] Email', 
                       patient_registration_date AS 'Registration Date', 
                       patient_NHS_blood_donor AS '[6] Blood donor',
                       patient_NHS_blood_donor AS '[7] Organ donor',
                       patient_status AS '[8] Status'
                FROM patient, gp
                WHERE patient_id = '{}'
                AND patient.gp_id = gp.gp_id
                """.format(patient_id)
        conn = sql.connect("database/db_comp0066.db")
        df = pd.read_sql_query(query, conn)
        conn.close()
        # ignoring GP name in patient instance (id stored instead)
        patient_instance = cls(*df.values[0][:2], *df.values[0][3:]) 
        # collecting GP information 
        df['Default GP'] = 'Dr. ' + df['Default GP'].astype(str) \
                               + ' (ID: ' + df['gp_id'].astype(str) + ')' 
        # removing GP ID as this has been combined with the GP's name (above)
        df_display = df.drop(columns = ['gp_id'])  
        # transposing for better readability
        df_object = df_display.transpose().rename(columns={0:"Value"}) 
        df_print = df_object.to_markdown(tablefmt="grid", index=True)
        return patient_instance, df_object, df_print


    @staticmethod
    def select_list(type, patient_last_name=None):
        """
        Returns lists of patients: 1) pending confirmation by an admin 
                                   2) with a matching last_name

        Args:
            type ('pending', 'matching'): type of list desired
                                          pending => not confirmed yet
                                          matching => based on last name 
            patient_last_name (str, optional): Search string for 'matching' type. 
                                               Defaults to None.

        Returns:
            df_object (pandas DF): Raw DF (can be searched etc.)
            df_print (string): Pretty DF for printing
        """        

        if type == 'pending':
            query = """
                    SELECT patient_id AS 'Patient ID',
                           patient_first_name AS 'First Name',
                           patient_last_name AS 'Last Name',  
                           patient_birth_date AS 'Birth Date',
                           patient_registration_date AS 'Registration Date'
                    FROM patient
                    WHERE patient_status = 'pending'
                    ORDER BY "Registration Date" ASC
                    """
            conn = sql.connect("database/db_comp0066.db")
            df_object = pd.read_sql_query(query, conn)
            conn.close()

        elif type == 'matching':
            query = """
                    SELECT patient_id AS 'Patient ID',
                           patient.gp_id,
                           gp.gp_last_name AS 'Default GP',
                           patient_first_name AS 'First Name',
                           patient_last_name AS 'Last Name',  
                           patient_birth_date AS 'Birth Date'
                    FROM patient, gp
                    WHERE patient_last_name = '{}'
                    AND patient.gp_id = gp.gp_id
                    AND patient_status = 'confirmed'
                    ORDER BY "First Name" ASC
                    """.format(patient_last_name)

            conn = sql.connect("database/db_comp0066.db")
            df = pd.read_sql_query(query, conn)
            conn.close()
            # collecting GP information
            df['Default GP'] = 'Dr. ' + df['Default GP'].astype(str) \
                               + ' (ID: ' + df['gp_id'].astype(str) + ')'
            # removing GP ID as it has been combined with GP name (above)
            df_object = df.drop(columns = ['gp_id']) 
        df_print = df_object.to_markdown(tablefmt="grid", index=False)
        return df_object, df_print

    
    @staticmethod
    def select_gp_details(patient_id):
        """
        Retrieves a patient's current default GP's ID and name

        Args:
            patient_id (int): [description]

        Returns:
            gp_id (int): Patient's default GP's ID
            gp_name (string): Patient's default GP's name in format 'Dr. last_name'
        """

        query = """
                SELECT patient.gp_id AS 'GP ID',
                       gp_last_name AS 'Name'
                FROM patient, gp
                WHERE patient_id = '{}'
                AND patient.gp_id = gp.gp_id
                """.format(patient_id)
        conn = sql.connect("database/db_comp0066.db")
        df = pd.read_sql_query(query, conn)
        conn.close()
        gp_id, gp_name = df.values.tolist()[0]
        gp_name = 'Dr. ' + gp_name
        return gp_id, gp_name


    @staticmethod
    def change_gp(type, patient_id, new_gp_id=None):
        """
        Changes a patient's default GP.

        Args:
            type ('auto', 'specific'): auto => least full GP (patient flow)
                                       specific => specified GP (admin flow)
            patient_id (int): ID of patient whose default GP is to be changed
            new_gp_id (int, optional): ID of the patient's new default GP

        Returns:
            boolean: True (success) or False (failure)
            new_gp_name (string): if True, GP name in format 'Dr. last_name'
        """

        # getting a list of GPs who aren't full
        df_not_full = GP.select_list('not_full')[0]
        num_GP_not_full = len(df_not_full.index)

        # GPs could (theoretically) all be at maximum capacity
        if num_GP_not_full == 0:
            return False, None

        else:
            # patient user flow - automatic allocation based on least full GP 
            if type == 'auto':
                new_gp_id = df_not_full['GP ID'].iloc[0]
            # admin user flow - specifying a specific GP for a patient
            # GP might have become full since GP.select_list('not full')
            # was called earler in the admin user flow
            elif type =='specific' and new_gp_id not in df_not_full['GP ID']:
                return False, None

            query = """
                    UPDATE patient
                    SET gp_id = '{}'
                    WHERE patient_id = '{}'
                    """.format(new_gp_id, patient_id)
            conn = sql.connect("database/db_comp0066.db")
            c = conn.cursor()
            c.execute(query)
            conn.commit()
            conn.close()
            
            new_gp_name = df_not_full['Name'].\
                          where(df_not_full['GP ID'] == new_gp_id)[0]
                          
            return True, new_gp_name


    @staticmethod
    def confirm(type, patient_id=None): 
        """
        Confirms patients: either 1) all or 
                                  2) a single patient

        Args:
            type ('all', 'single'): if want to confirm all pending or only 1
            patient_id (int, optional): ID of 'single' patient to confirm.  
                                        Defaults to None.
        """        

        if type == 'all':
            query = """
                    UPDATE patient
                    SET patient_status = 'confirmed'
                    WHERE patient_status = 'pending'
                    """

        elif type == 'single':
            query = """
                    UPDATE patient
                    SET patient_status = 'confirmed'
                    WHERE patient_id = '{}'
                    """.format(patient_id)

        conn = sql.connect("database/db_comp0066.db")
        c = conn.cursor()
        c.execute(query)
        conn.commit()
        conn.close()


    @staticmethod
    def delete(patient_id): 
        """
        Deletes a patient from the patient table. 
        Note: database auto-deletes appointments and records (ON CASCADE)

        Args:
            patient_id (int): ID of patient to be deleted
        """        

        query = """
                DELETE FROM patient
                WHERE patient_id = '{}'
                """.format(patient_id)
        conn = sql.connect("database/db_comp0066.db")
        c = conn.cursor()
        c.execute(query)
        conn.commit()
        conn.close()




if __name__ == "__main__":

    ## update()
    #test_patient = Patient.select(4)[0]
    #test_patient.first_name = "updated_name2"
    #test_patient.update()

    ## Patient.select()
    # patient_instance, df_obj, df_print = Patient.select(4)
    # print(vars(patient_instance))
    # print(df_obj)
    # print(df_print)

    ## Patient.select_list()
    # df_obj, df_print = Patient.select_list('matching', 'Moon')
    # print(df_obj)
    # print(df_print)

    ## Patient.select_gp_details()
    # gp_id, gp_name = Patient.select_gp_details(2)
    # print(gp_id)
    # print(gp_name)

    ## Patient.change_gp()
    # success, new_gp_name = Patient.change_gp('auto', 2)
    # print(success)
    # print(new_gp_name)

    ## Patient.confirm()
    # Patient.confirm('all')

    ## Patient.delete()
    # Patient.delete(1)

    pass