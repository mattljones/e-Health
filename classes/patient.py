# patient.py

# import libraries
import pandas as pd
import sqlite3 as sql

class Patient():
    '''
    Class defining all 'patient' related methods.
    The patient class instantiates patient objects from the database.
    '''

    def __init__(self, patient_id):
        '''
        Patient class constructor storing patient_id as class variable.
        '''
        self.patient_id = patient_id

    def __str__(self):
        '''
        Patient class method printing patient's details from database when asked to print an instance of the class.
        '''

        conn = sql.connect("database/db_comp0066.db")
        df = pd.read_sql_query("SELECT * FROM patient WHERE patient_id =" + str(self.patient_id) + ";", conn)
        conn.close()

        return("\n" + str(df.head()) + "\n")

    def update():
        '''
        Method to update patient's details in the database
        '''
        pass

    def select_pending():
        '''
        '''
        pass

    def select_matching():
        '''
        '''
        pass

    








### DEVELOPMENT ###

if __name__ == "__main__":

    p1 = Patient(2)
    print(p1)