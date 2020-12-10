import sqlite3
import pandas as pd

class GP:

    def __init__(self):
        self.gp_id = ""
        self.first_name = ""
        self.last_name = ""
        self.gender = ""
        self.birth_date = ""
        self.email = ""
        self.password = ""
        self.registration_date = ""
        self.specialisation_id = ""
        self.department_id = ""
        self.working_days = ""
        self.status = ""

    def insert(self): # INSERT - INSTANCE
        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        c.execute("INSERT INTO gp VALUES (NULL, ?, ?, ?, ?, ?, ?, NULL, ?, ?, ?, ?);",
                                            (self.first_name,
                                             self.last_name,
                                             self.gender,
                                             self.birth_date,
                                             self.email,
                                             self.password,
                                             self.specialisation_id,
                                             self.department_id,
                                             self.working_days,
                                             self.status)
                                            )
        conn.commit()
        conn.close()

    @staticmethod # INSERT - STATIC
    def insert_static(first_name, last_name, gender, birth_date, email, password, specialisation_id, department_id, working_days, status):
        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        c.execute("INSERT INTO gp VALUES (NULL, ?, ?, ?, ?, ?, ?, NULL, ?, ?, ?, ?);",
                                            (first_name,
                                             last_name,
                                             gender,
                                             birth_date,
                                             email,
                                             password,
                                             specialisation_id,
                                             department_id,
                                             working_days,
                                             status)
                                            )
        conn.commit()
        conn.close()


class Schedule:

    @staticmethod # SELECT day - STATIC
    def select_day(gp_id, date):
        conn = sqlite3.connect("database.db")
        schedule_day = pd.read_sql_query("SELECT date, status, agenda, type, patient_id FROM appointment WHERE gp_id = ? AND date = ?;", conn, params=(gp_id, date))
        conn.close()
        return schedule_day


    @staticmethod  # SELECT week - STATIC
    def select_week(gp_id, date_day1):
    # creates a df with groups of columns as days (e.g. time, status)
        pass

    @staticmethod # COMBINED SELECT
    def select(gp_id, **kwargs):
        if len(kwargs) == 1:
            # select_day, defined here or elsewhere
            return len(kwargs)
        if len(kwargs) == 2:
            # select_week or select_custom, possibly with intelligent sizing based on # days, defined here or elsewhere
            return len(kwargs)
