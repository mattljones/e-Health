# gp.py

# import libraries
import pandas as pd
import sqlite3 as sql

class GP():
    '''
    Class defining all 'GP' related methods.
    The GP class instantiates GP objects from the database.
    '''

    def __init__(self, gp_id):
        '''
        GP class constructor storing gp_id as class variable.
        '''
        self.gp_id = gp_id


    def __str__(self):
        '''
        GP class method printing GP's details from database when asked to print an instance of the class.
        '''
        
        conn = sql.connect("config/db_comp0066.db")
        df = pd.read_sql_query("SELECT * FROM gp WHERE gp_id =" + str(self.gp_id) + ";", conn)
        conn.close()

        return(str(df.head()))








### DEVELOPMENT ###

if __name__ == "__main__":
    pass