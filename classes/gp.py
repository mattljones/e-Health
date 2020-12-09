# gp.py

# import User class
from user import User

# import libraries
import sqlite3 as sql
import pandas as pd


class GP(User):
    """
    Child class of 'User', inheriting attributes shared between user types.
    Defines attributes and methods for GP-related activities in different user flows. 
    """

    max_capacity = 2500  # Maximum number of patients per GP 


    def __init__(self, id_="", first_name="", last_name="", gender="", birth_date="", email="", password="",
                 registration_date="", working_days="", department_id="", specialisation_id=""):
        User.__init__(self, id_, first_name, last_name, gender, birth_date, email, password, registration_date)
        self.working_days = working_days
        self.department_id = department_id
        self.specialisation_id = specialisation_id


    def insert(self):
        """
        Inserts a new GP into the database from an instance. 
        """
        conn = sql.connect("database/db_comp0066.db")
        c = conn.cursor()
        c.execute("""INSERT INTO gp 
                     VALUES (NULL, ?, ?, ?, ?, ?, ?, NULL, ?, ?, ?, ?);""",
                  (self.first_name, self.last_name, self.gender, self.birth_date, self.email, self.password,
                   self.working_days, self.department_id, self.specialisation_id, self.status))
        conn.commit()
        conn.close()


    def update(self):
        """
        Updates a GP's attributes from an instance created to display the GP's attributes. 
        Users will likely have only updated a subset of the attributes in practice. 
        """
        conn = sql.connect("database/db_comp0066.db")
        c = conn.cursor()
        c.execute("""UPDATE gp 
                     SET gp_first_name = ?, gp_last_name = ?, gp_gender = ?, gp_birth_date = ?, gp_email = ?, gp_password = ?,
                         gp_registration_date = ?, gp_working_days = ?, gp_department_id = ?, gp_specialisation_id = ?, gp_status = ?
                     WHERE gp_id = ?""",
                  (self.first_name, self.last_name, self.gender, self.birth_date, self.email, self.password,
                   self.registration_date, self.working_days, self.department_id, self.specialisation_id, self.status,
                   self.id))
        conn.commit()
        conn.close()


    @classmethod
    def select_gp(cls, gp_id):
        """
        Factory method creating a GP instance from a SELECT query and returning a corresponding (transposed) dataframe.
        """
        conn = sql.connect("database/db_comp0066.db")
        df = pd.read_sql_query("""SELECT gp_id AS 'ID', gp_first_name AS 'First Name', gp_last_name AS 'Last Name', gp_gender AS 'Gender',
                                  gp_birth_date AS 'Birth Date', gp_email AS 'Email', gp_registration_date AS 'Registration Date', 
                                  gp_working_days AS 'Working Days', gp_department_id AS 'Department', gp_specialisation_id AS 'Specialisation'
                                  FROM gp
                                  WHERE gp_id = ?""", 
                               conn, params=(gp_id,))
        conn.close()
        instance = cls(*df.to_records(index=False)[0])
        df_transposed = df.transpose().rename(columns={0:"Value"})
        df_formatted = df_transposed.to_markdown(tablefmt="grid", index=True)
        return instance, df_formatted


    @staticmethod
    def select_list(type):
        """
        Returns lists of GPs: 1) all GPs or 2) GPs who aren't full (less than 2,500 patients)
        """
        if type == 'all':
            conn = sql.connect("database/db_comp0066.db")
            df = pd.read_sql_query("""SELECT gp_id AS 'ID', gp_first_name AS 'First Name', gp_last_name AS 'Last Name'
                                      FROM gp
                                      ORDER BY gp_last_name ASC""", 
                                   conn)
            conn.close()
            df_formatted = df.to_markdown(tablefmt="grid", index=False)
            return df_formatted
        elif type == 'not_full':
            conn = sql.connect("database/db_comp0066.db")
            df = pd.read_sql_query("""SELECT gp_id AS 'ID', gp_first_name AS 'First Name', gp_last_name AS 'Last Name', COUNT(patient_id) AS 'No. Patients'
                                      FROM gp, patient
                                      WHERE gp.gp_id = patient.gp_id
                                      GROUP BY gp_id
                                      ORDER BY 'No. Patients' ASC""", 
                                   conn)
            conn.close()
            df_not_full = df.loc[df['No. Patients'] <= GP.max_capacity]
            df_formatted = df_not_full.to_markdown(tablefmt="grid", index=False)
            return df_formatted            


    @staticmethod
    def change_status(gp_id, new_status):
        """
        Changes a given GP's status to a new, given status.
        """
        conn = sql.connect("database/db_comp0066.db")
        c = conn.cursor()
        c.execute("""UPDATE gp
                     SET gp_status = ?
                     WHERE gp_id = ?""", 
                  (new_status, gp_id))
        conn.commit()
        conn.close()


    @staticmethod
    def delete(gp_id):
        """
        Deletes a GP from the GP table. Note: this will xxx.
        """
        conn = sql.connect("database/db_comp0066.db")
        c = conn.cursor()
        c.execute("""DELETE FROM gp
                     WHERE gp_id = ?""", 
                  (gp_id,))
        conn.commit()
        conn.close()


    @staticmethod
    def check_full(gp_id):
        """
        Checks if a given GP is full (i.e. can take no extra patients).
        """
        conn = sql.connect("database/db_comp0066.db")
        c = conn.cursor()
        c.execute("""SELECT COUNT(patient_id)
                     FROM gp, patient
                     WHERE gp.gp_id = patient.gp_id AND gp_id = ?
                     GROUP BY gp_id""", 
                  (gp_id,))
        count = c.fetchone()
        conn.close()
        if count[0] <= GP.max_capacity:
            return False
        else:
            return True


### DEVELOPMENT ###

if __name__ == "__main__":
    pass
