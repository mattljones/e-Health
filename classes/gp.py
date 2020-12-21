# gp.py

# import libraries
import sqlite3 as sql
import pandas as pd
from datetime import datetime
from itertools import cycle

# Switching path to master to get functions from utils folder
import sys
from pathlib import Path
path_to_master_repo = Path(__file__).parents[1]
sys.path.insert(1, str(path_to_master_repo))

# import User class for inheritance
from classes.user import User


class GP(User):
    """
    Child class of 'User', inheriting shared attributes. 
    Defines GP-related attributes & methods for different user flows. 
    """

    max_capacity = 50  # Maximum number of patients per GP 

    # default value 'None' for saving user input into a blank instance 
    def __init__(self,  
                 id_=None, 
                 first_name=None, 
                 last_name=None, 
                 gender=None, 
                 birth_date=None, 
                 email=None, 
                 password_raw=None,      # raw password required for insert()
                 registration_date=None, 
                 working_days=None, 
                 department_id=None, 
                 specialisation_id=None, 
                 status=None):
        User.__init__(self, id_, first_name, last_name, gender, birth_date, 
                      email, password_raw, registration_date, status)
        self.working_days = working_days
        self.department_id = department_id
        self.specialisation_id = specialisation_id


    def insert(self):  # TODO: add password hashing from utilties
        """
        Inserts a new GP from an instance populated by user input.
        GPs cannot register themselves: instance created in user flow.
        """ 

        self.registration_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        query = """
                INSERT INTO gp 
                VALUES (NULL, '{}', '{}', '{}', '{}', '{}', 
                        '{}', '{}', '{}', '{}', '{}', '{}')
                """.format(self.first_name, 
                           self.last_name, 
                           self.gender, 
                           self.birth_date, 
                           self.email, 
                           self.password_raw,
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
        Updates a GP's details (overrides DB attributes w/ instance values)
        """

        query = """
                UPDATE gp 
                SET gp_first_name = '{}', 
                    gp_last_name = '{}', 
                    gp_gender = '{}', 
                    gp_birth_date = '{}', 
                    gp_email = '{}',  
                    gp_working_days = '{}', 
                    gp_department_id = '{}', 
                    gp_specialisation_id = '{}', 
                    gp_status = '{}'
                WHERE gp_id = '{}'
                """.format(self.first_name, 
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
        Generates an instance of the GP & a dataframe summarising their 
        attributes to display in user flow.
        Instance passed to user flow for storing user-inputted values.

        Args:
            gp_id (int): ID of the GP to be viewed 

        Returns:
            gp_instance (instance): Used for storing future user inputs
            df_object (pandas DF): Raw DF (can be searched etc.)
            df_print (string): Pretty DF for printing
        """    

        query = """
                SELECT gp_id AS '[ ] GP ID', 
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
                AND gp.gp_specialisation_id = gps.gp_specialisation_id
                """.format(gp_id)
        conn = sql.connect("database/db_comp0066.db")
        df = pd.read_sql_query(query, conn)
        conn.close()
        # ignoring password, dept. name and spec. name
        gp_instance = cls(*df.values[0][:6], None, *df.values[0][6:10], df.values[0][12])  
        # removing IDs as not displayed initially to the user
        df_display = df.drop(columns = ['gp_department_id', 'gp_specialisation_id'])       
        # transposing for better readability
        df_object = df_display.transpose().rename(columns={0:"Value"})                     
        df_print = df_object.to_markdown(tablefmt="grid", index=True)
        return gp_instance, df_object, df_print


    @staticmethod
    def select_list(type):
        """
        Returns lists of GPs: 1) all GPs; 
                              2) active GPs 
                              3) GPs who aren't full

        Args:
            type ('all', 'active', 'not_full'): type of list desired
                                                not_full wrt. patients, not apps.

        Returns:
            df_object (pandas DF): Raw DF (can be searched etc.)
            df_print (string): Pretty DF for printing
        """        

        if type == 'all':
            query = """
                    SELECT gp_id AS 'GP ID',  
                           gp_last_name AS 'Name',
                           gp_birth_date AS 'Birth Date'
                    FROM gp
                    ORDER BY gp_last_name ASC
                    """

        elif type =='active':
            query = """
                    SELECT gp_id AS 'GP ID',  
                           gp_last_name AS 'Name',
                           gp_birth_date AS 'Birth Date'
                    FROM gp
                    WHERE gp_status = 'active'
                    ORDER BY gp_last_name ASC
                    """

        elif type == 'not_full':
            query = """
                    SELECT gp.gp_id AS 'GP ID', 
                           gp_last_name AS 'Name',
                           gp_birth_date AS 'Birth Date', 
                           COUNT(patient_id) AS "No. Patients"
                    FROM gp, patient
                    WHERE gp.gp_id = patient.gp_id
                    AND gp_status = 'active'
                    GROUP BY gp.gp_id
                    HAVING COUNT(patient_id) < '{}'
                    ORDER BY "No. Patients" ASC
                    """.format(GP.max_capacity)

        conn = sql.connect("database/db_comp0066.db")
        df_object = pd.read_sql_query(query, conn)
        conn.close()
        # Adding 'Dr.' prefix to GP last name
        df_object['Name'] = 'Dr. ' + df_object['Name'].astype(str) 
        df_print = df_object.to_markdown(tablefmt="grid", index=False)
        return df_object, df_print


    @staticmethod
    def select_table(type):
        """
        Returns a list of GP departments/specialisations for reference.

        Args:
            type ('department', 'specialisation'): type of table desired

        Returns:
            df_object (pandas DF): Raw DF (can be searched etc.)
            df_print (string): Pretty DF for printing
        """        

        if type == 'department':
            query = """
                    SELECT gp_department_id AS "Dept. ID",
                           gp_department AS 'Department'
                    FROM gp_department
                    """
                    
        elif type == 'specialisation':
            query = """
                    SELECT gp_specialisation_id AS "Spec. ID",
                           gp_specialisation_name AS 'Specialisation'
                    FROM gp_specialisation
                    """
                    
        conn = sql.connect("database/db_comp0066.db")
        df_object = pd.read_sql_query(query, conn)
        conn.close()
        df_print = df_object.to_markdown(tablefmt="grid", index=False)
        return df_object, df_print

    
    @staticmethod
    def reallocate_patients(gp_id):
        """
        Automatically reallocates a GP (who is being deleted)'s patients to 
        other GPs with capacity. Preserves the 'shape' of the distribution 
        of patients (as some GPs might have more for a reason). 

        Args:
            gp_id (int): ID of the GP being deleted

        Returns:
            boolean: True (success) or False (not enough total capacity)
            shortfall: if False, number of patients beyond current capacity
        """
        
        # retieving list of GPs with capacity for new patients
        df_not_full = GP.select_list('not_full')[0]
        # retrieving number of patients to reallocate
        if gp_id in df_not_full['GP ID'].tolist():
            num_reallocate = df_not_full[df_not_full['GP ID'] == gp_id]['No. Patients'].iloc[0]

        else:
            num_reallocate = GP.max_capacity
        # limiting reallocation to remaining GPs only
        df_other_not_full = df_not_full[df_not_full['GP ID'] != gp_id]
        # creating data structures used in reallocation while loop
        gp_capacity_dict = dict(zip(df_other_not_full['GP ID'],\
                                GP.max_capacity - df_other_not_full['No. Patients']))
        gp_not_full_list = list(gp_capacity_dict)
        capacity = sum(gp_capacity_dict.values())
        shortfall = num_reallocate - capacity
        
        # if patients cannot *all* be reallocated, do not reallocate any
        if shortfall > 0:
            return False, shortfall

        else:
            count = 0
            index = 0
            # list of (new_gp_id, old_gp_id) used in executemany() method
            allocations = []
            # Iterates over a list of GPs with capacity for new patients, 
            # adding one each time. Preserves the 'shape' of the 
            # distribution (as some GPs might have more patients for a reason).
            while count < num_reallocate:
                new_gp_id = gp_not_full_list[index]
                allocations.append((new_gp_id, gp_id, gp_id))
                gp_capacity_dict[new_gp_id] -= 1
                count += 1
                # updating index pointer
                if index == len(gp_not_full_list) - 1:
                    index = 0
                    if gp_capacity_dict[new_gp_id] == 0:
                        gp_not_full_list.remove(new_gp_id)
                else:
                    if gp_capacity_dict[new_gp_id] == 0:
                        gp_not_full_list.remove(new_gp_id)
                    else:
                        index += 1

            conn = sql.connect("database/db_comp0066.db")
            c = conn.cursor()
            c.executemany("""
                          UPDATE patient
                          SET gp_id = ?
                          WHERE gp_id = ?
                          AND patient_id IN (SELECT MIN(patient_id)
                                             FROM patient
                                             WHERE gp_id = ?)
                          """, allocations)
            conn.commit()
            conn.close()
            return True, None

    
    @staticmethod
    def reallocate_appointments(gp_id):
        """
        Automatically reallocates a GP (who is being deleted)'s appointments 
        to other GPs free at those times. Preserves the 'shape' of the 
        distribution of appointments (as some GPs might have more for a reason).

        Args:
            gp_id (int): ID of the GP being deleted

        Returns:
            boolean: True (success) or False (not all slots can be covered)
            df_object: if False, appointments that can't be reallocated
            df_print: if False, Pretty DF for printing
        """

        # retrieving list of GPs (and how many there are)
        df_active_gp = GP.select_list('active')[0]
        num_gp = df_active_gp['GP ID'].nunique()
        # retrieving current time
        time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
        # query selecting *this* GP's upcoming appointment times
        query_this_gp_start_times = """
                                    SELECT booking_start_time
                                    FROM booking
                                    WHERE gp_id = '{}'
                                    AND booking_start_time >= '{}'
                                    """.format(gp_id, time_now)
        # query retrieving all GPs' upcoming appointments at the above times
        query_all_gp_upcoming = """
                                SELECT booking_id AS 'Apt. ID',
                                       booking_start_time AS 'Time',
                                       gp_id AS 'GP ID'
                                FROM booking
                                WHERE booking_start_time IN ({})
                                """.format(query_this_gp_start_times)
        conn = sql.connect("database/db_comp0066.db")
        df_all_gp_upcoming = pd.read_sql_query(query_all_gp_upcoming, conn)
        conn.close()
        # sub-sets of df_all_gp_upcoming: this GP, and all other GPs
        df_this_gp_upcoming = df_all_gp_upcoming[df_all_gp_upcoming['GP ID'] == gp_id]
        df_other_gp_upcoming = df_all_gp_upcoming[df_all_gp_upcoming['GP ID'] != gp_id]
        # counting how many GPs have appointments per time slot 
        columns1 = ['Time']
        columns2 = ['Apt. ID', 'GP ID']
        df_gp_count = df_all_gp_upcoming.groupby(columns1)[columns2].nunique()
        # if one appointment cannot be reallocated, reallocate *none*
        if num_gp in df_gp_count['GP ID'].tolist():
            times_no_capacity = df_gp_count[df_gp_count['GP ID'] == num_gp].index.tolist()
            # dataframe containing appointments which are causing the reallocation to fail
            df_object = df_this_gp_upcoming[df_this_gp_upcoming['Time'].isin(times_no_capacity)].drop(columns='GP ID')
            df_print = df_object.to_markdown(tablefmt="grid", index=False)
            return False, df_object, df_print

        else:
            # convert to string to allow concatenation in .groupby() method
            df_other_gp_upcoming['Apt. ID'] = df_other_gp_upcoming['Apt. ID'].apply(str)
            df_other_gp_upcoming['GP ID'] = df_other_gp_upcoming['GP ID'].apply(str)
            # df with lists of *other* GPs with appointments at same time as one of *this* GP's upcoming appointments 
            df_other_gp_grouped = df_other_gp_upcoming.groupby(columns1)[columns2].agg(', '.join).reset_index() 
            # create dictionary with key:value pairs of {timestamp, [GPs already with appointment at this time]}
            other_gp_clashes = dict(zip(df_other_gp_grouped['Time'], df_other_gp_grouped['GP ID'].tolist()))
            # simple list of other GPs
            other_gp_list = df_active_gp['GP ID'].tolist()
            other_gp_list.remove(gp_id)
            # simple list of *this* GPs upcoming appointment times (for reallocation)
            app_times = list(other_gp_clashes)

            index = 0
            other_gp_cycle = cycle(other_gp_list)
            new_gp_id = next(other_gp_cycle)
            # list of (new_gp_id, old_gp_id, app_time) used in executemany() method
            allocations = []
            # iterating through appointment times 1-by-1
            while index < len(app_times):
                # cycling through GPs until an available GP at this time is found
                while str(new_gp_id) in other_gp_clashes[app_times[index]]:
                    new_gp_id = next(other_gp_cycle)

                allocations.append((new_gp_id, gp_id, app_times[index]))
                new_gp_id = next(other_gp_cycle)
                index += 1

            conn = sql.connect("database/db_comp0066.db")
            c = conn.cursor()
            c.executemany("""
                            UPDATE booking
                            SET gp_id = ?
                            WHERE gp_id = ?
                            AND booking_start_time = ?
                            """, allocations)
            conn.commit()
            conn.close()
            return True, None, None


    @staticmethod  # TODO: Add patient/appointment reallocation 
    def change_status(gp_id, new_status):  
        """
        Changes a given GP's status (to inactive/active).
        Note: if deactivating, this auto-reallocates patients & appointments.

        Args:
            gp_id (int): ID of the GP whose status is to be changed
            new_status ('inactive', 'active'): GP's new status
        """        

        query = """
                UPDATE gp
                SET gp_status = '{}'
                WHERE gp_id = '{}'
                """.format(new_status, gp_id)
        conn = sql.connect("database/db_comp0066.db")
        c = conn.cursor()
        c.execute(query)
        conn.commit()
        conn.close()


    @staticmethod
    def delete(gp_id):  # TODO: Add patient/appointment reallocation 
        """
        Deletes a GP from the GP table. 
        Note: this auto-reallocates patients & appointments.

        Args:
            gp_id (int): ID of the GP to be deleted
        """        

        query = """
                DELETE FROM gp
                WHERE gp_id = '{}'
                """.format(gp_id)
        conn = sql.connect("database/db_comp0066.db")
        c = conn.cursor()
        c.execute(query)
        conn.commit()
        conn.close()




if __name__ == "__main__":

    ## insert()
    # test_GP = GP(first_name="test", 
    #              last_name="test", 
    #              gender="male", 
    #              birth_date="2020-12-13", 
    #              email="test@gmail.com", 
    #              password_raw="password", 
    #              working_days=1, 
    #              department_id=1, 
    #              specialisation_id=1, 
    #              status="active")
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

    ## GP.reallocate_patients()
    # GP.reallocate_patients(7)

    ## GP.reallocate_appointments()
    # GP.reallocate_appointments(1)

    ## GP.change_status()
    # GP.change_status(2, 'inactive')

    ## GP.delete()
    # GP.delete(2)

    pass
