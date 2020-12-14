# gp.py

# import User class for inheritance
from user import User

# import libraries
import sqlite3 as sql
import pandas as pd
import datetime


class GP(User):
    """
    Child class of 'User', inheriting attributes shared between GPs and patients.
    Defines attributes and methods for GP-related activities in different user flows. 
    """

    max_capacity = 50  # Maximum number of patients per GP 


    def __init__(self,  # default value of 'None' to enable saving user input into a blank instance (e.g. creating a new GP account) 
                 id_=None, 
                 first_name=None, 
                 last_name=None, 
                 gender=None, 
                 birth_date=None, 
                 email=None, 
                 password=None,  # password required for insert()
                 registration_date=None, 
                 working_days=None, 
                 department_id=None, 
                 specialisation_id=None, 
                 status=None):
        User.__init__(self, id_, first_name, last_name, gender, birth_date, email, password, registration_date, status)
        self.working_days = working_days
        self.department_id = department_id
        self.specialisation_id = specialisation_id


    def insert(self):  # TO DO: Add password hashing using utilities 
        """
        Inserting a new GP from an instance populated by user input (GPs cannot register themselves; instance created in user flow)
        """ 
        self.registration_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        query = """INSERT INTO gp 
                   VALUES (NULL, '{}', '{}', '{}', '{}', '{}', 
                           '{}', '{}', '{}', '{}', '{}', '{}')""".format(self.first_name, 
                                                                         self.last_name, 
                                                                         self.gender, 
                                                                         self.birth_date, 
                                                                         self.email, 
                                                                         self.password,
                                                                         self.registration_date, 
                                                                         self.working_days, 
                                                                         self.department_id, 
                                                                         self.specialisation_id, 
                                                                         self.status)
        conn = sql.connect("database/db_comp0066.db")
        c = conn.cursor()
        c.execute(query)
        conn.commit()
        conn.close()


    def update(self):
        """
        Updating a GP's details (technically overriding every DB attribute w/ instance values)
        """
        query = """UPDATE gp 
                   SET gp_first_name = '{}', 
                       gp_last_name = '{}', 
                       gp_gender = '{}', 
                       gp_birth_date = '{}', 
                       gp_email = '{}',  
                       gp_working_days = '{}', 
                       gp_department_id = '{}', 
                       gp_specialisation_id = '{}', 
                       gp_status = '{}'
                   WHERE gp_id = '{}'""".format(self.first_name, 
                                                self.last_name, 
                                                self.gender, 
                                                self.birth_date, 
                                                self.email, 
                                                self.working_days, 
                                                self.department_id, 
                                                self.specialisation_id, 
                                                self.status,
                                                self.id)
        conn = sql.connect("database/db_comp0066.db")
        c = conn.cursor()
        c.execute(query)
        conn.commit()
        conn.close()


    @classmethod
    def select(cls, gp_id):
        """
        Generating an instance of a GP to later update attributes based on user input (& also returning a DF to display in user flow)
        """
        query = """SELECT gp_id AS '[ ] GP ID', 
                          gp_first_name AS '[1] First Name', 
                          gp_last_name AS '[2] Last Name', 
                          gp_gender AS '[3] Gender',
                          gp_birth_date AS '[4] Birth Date', 
                          gp_email AS '[5] Email', 
                          gp_registration_date AS '[ ] Registration Date', 
                          gp_working_days AS '[6] Working Days', 
                          gp.gp_department_id,
                          gp.gp_specialisation_id,
                          gpd.gp_department AS '[7] Department', 
                          gps.gp_specialisation_name AS '[8] Specialisation',
                          gp_status AS '[9] Status'
                   FROM gp, gp_department gpd, gp_specialisation gps
                   WHERE gp_id = '{}'
                   AND gp.gp_department_id = gpd.gp_department_id
                   AND gp.gp_specialisation_id = gps.gp_specialisation_id""".format(gp_id)
        conn = sql.connect("database/db_comp0066.db")
        df = pd.read_sql_query(query, conn)
        conn.close()
        gp_instance = cls(*df.values[0][:6], None, *df.values[0][6:10], df.values[0][12])  # ignoring password, dept. name and spec. name
        df_display = df.drop(columns = ['gp_department_id', 'gp_specialisation_id'])  # removing IDs as not displayed initially to the user
        df_object = df_display.transpose().rename(columns={0:"Value"})
        df_print = df_object.to_markdown(tablefmt="grid", index=True)
        return gp_instance, df_object, df_print


    @staticmethod
    def select_list(type):
        """
        Returns lists of GPs: 1) all GPs; 2) active GPs 3) GPs who aren't full (defined by GP.max_capacity class variable)
        """
        if type == 'all':
            query = """SELECT gp_id AS 'GP ID',  
                              gp_last_name AS 'Name',
                              gp_birth_date AS 'Birth Date'
                       FROM gp
                       ORDER BY gp_last_name ASC"""
        elif type =='active':
            query = """SELECT gp_id AS 'GP ID',  
                              gp_last_name AS 'Name',
                              gp_birth_date AS 'Birth Date'
                       FROM gp
                       WHERE gp_status = 'active'
                       ORDER BY gp_last_name ASC"""
        elif type == 'not_full':
            query = """SELECT gp.gp_id AS 'GP ID', 
                              gp_last_name AS 'Name',
                              gp_birth_date AS 'Birth Date', 
                              COUNT(patient_id) AS "No. Patients"
                       FROM gp, patient
                       WHERE gp.gp_id = patient.gp_id
                       GROUP BY gp.gp_id
                       HAVING COUNT(patient_id) <= '{}'
                       ORDER BY "No. Patients" ASC""".format(GP.max_capacity)
        conn = sql.connect("database/db_comp0066.db")
        df_object = pd.read_sql_query(query, conn)
        conn.close()
        df_object['Name'] = 'Dr. ' + df_object['Name'].astype(str)
        df_print = df_object.to_markdown(tablefmt="grid", index=False)
        return df_object, df_print


    @staticmethod
    def select_table(type):
        """
        Returns a list of GP departments or specialisations for reference when updating
        """
        if type == 'department':
            query = """SELECT gp_department_id AS "Dept. ID",
                              gp_department AS 'Department'
                       FROM gp_department"""
        elif type == 'specialisation':
            query = """SELECT gp_specialisation_id AS "Spec. ID",
                              gp_specialisation_name AS 'Specialisation'
                       FROM gp_specialisation"""
        conn = sql.connect("database/db_comp0066.db")
        df_object = pd.read_sql_query(query, conn)
        conn.close()
        df_print = df_object.to_markdown(tablefmt="grid", index=False)
        return df_object, df_print


    @staticmethod
    def change_status(gp_id, new_status):  # TO DO: Add patient/appointment reallocation 
        """
        Changes a given GP's status (to inactive/active).
        Note: if deactivating, this auto-reallocates the GP's patients and future appointments to other GPs.
        """
        query = """UPDATE gp
                   SET gp_status = '{}'
                   WHERE gp_id = '{}'""".format(new_status, gp_id)
        conn = sql.connect("database/db_comp0066.db")
        c = conn.cursor()
        c.execute(query)
        conn.commit()
        conn.close()


    @staticmethod
    def delete(gp_id):  # TO DO: Add patient/appointment reallocation 
        """
        Deletes a GP from the GP table. 
        Note: this auto-reallocates the GP's patients and future appointments to other GPs.
        """
        query = """DELETE FROM gp
                   WHERE gp_id = '{}'""".format(gp_id)
        conn = sql.connect("database/db_comp0066.db")
        c = conn.cursor()
        c.execute(query)
        conn.commit()
        conn.close()


    @staticmethod
    def check_not_full(gp_id):
        """
        Used in Patient.change_GP() to check a GP is not full before giving them an additional patient.
        DB might have changed since GP.select_list(not_full) was called earlier in user flow.
        """
        query = """SELECT COUNT(patient_id)
                   FROM gp, patient
                   WHERE gp.gp_id = patient.gp_id 
                   AND gp.gp_id = '{}'
                   GROUP BY gp.gp_id""".format(gp_id)
        conn = sql.connect("database/db_comp0066.db")
        c = conn.cursor()
        c.execute(query)
        count = c.fetchone()
        conn.close()
        if count[0] < GP.max_capacity:
            return True
        else:
            return False




## CODE TESTING/DEMONSTRATION

# test_GP = GP(first_name="test", 
#              last_name="test", 
#              gender="male", 
#              birth_date="2020-12-13", 
#              email="test@gmail.com", 
#              password="password", 
#              working_days=1, 
#              department_id=1, 
#              specialisation_id=1, 
#              status="active")

## insert()
# test_GP.insert()

## update()
# test_GP_2 = GP.select(3)[0]
# test_GP_2.first_name = "updated_name"
# test_GP_2.update()

## GP.select()
# gp_instance, df_obj, df_print = GP.select(3)
# print(vars(gp_instance))
# print(df_obj)
# print(df_print)

## GP.select_list()
# df_obj, df_print = GP.select_list('active')
# print(df_obj)
# print(df_print)

## GP.select_table()
# df_obj, df_print = GP.select_table('department')
# print(df_obj)
# print(df_print)

## GP.change_status()
# GP.change_status(2, 'active')

## GP.delete()
# GP.delete(2)

## GP.check_not_full()
# print(GP.check_not_full(3))
