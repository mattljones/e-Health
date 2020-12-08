# schedule.py

# import libraries
import pandas as pd
import sqlite3 as sql

class Schedule:
    '''
    Class defining all 'schedule' related methods.
    '''

    @staticmethod # SELECT day - STATIC
    def select_day(gp_id, date):
        conn = sqlite3.connect("database/db_comp0066.db")
        schedule_day = pd.read_sql_query("SELECT date(availability_start_time), availability_status, availability_agenda, availability_type, patient_id FROM availability WHERE gp_id = ? AND availability_start_time = ?;", conn, params=(gp_id, date))
        conn.close()
        return schedule_day


    @staticmethod  # SELECT week - STATIC
    def select_week(gp_id, date_day1):
        # creates a df with groups of columns as days (e.g. time, status)
        rng = pd.date_range(start=date_day1, periods=7, freq='d')
        conn = sqlite3.connect("database/db_comp0066.db")
        schedule_week = pd.read_sql_query("SELECT availability_start_time, availability_status, availability_agenda, availability_type, patient_id FROM availability WHERE gp_id = ? AND availability_start_time = ?;", conn, params=(gp_id, date(date)))
        conn.close()
        return schedule_week

    @staticmethod # COMBINED SELECT
    def select(gp_id, **kwargs):
        if len(kwargs) == 1:
            # select_day, defined here or elsewhere
            return len(kwargs)
        if len(kwargs) == 2:
            # select_week or select_custom, possibly with intelligent sizing based on # days, defined here or elsewhere
            return len(kwargs)


df= Schedule.select_day(1,'2020-12-08')

import time
s = "2020-12-08 08:00:00"
r = datetime.datetime(*time.strptime(s, "%Y-%m-%d %H:%M:%S")[:5])
r.date


pd.date_range("8:00", "16:50", freq="10min").strftime('%H:%M:%S')


### DEVELOPMENT ###

if __name__ == "__main__":
    pass