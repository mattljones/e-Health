# appointment.py

# import libraries
import pandas as pd
import datetime
import sqlite3 as sql
# import calendar
from tabulate import tabulate


def db_execute(query):
    conn = sql.connect('database/db_comp0066.db')
    c = conn.cursor()
    c.execute(query)
    # Commit to db
    conn.commit()
    print("Info successfully committed")
    # Close db
    conn.close()


def db_read_query(query):
    conn = sql.connect("database/db_comp0066.db")
    result = pd.read_sql_query(query, conn)
    conn.close()
    return result


class Appointment:
    """
    Class defining all 'appointment' related methods.
    """

    def __init__(self, booking_id=None, booking_start_time=None, booking_status=None,
                 booking_status_change_time=None, booking_agenda=None, booking_type=None,
                 booking_notes=None, gp_id=None, patient_id=None):
        self.booking_id = booking_id
        self.booking_start_time = booking_start_time
        self.booking_status = booking_status
        self.booking_status_change_time = booking_status_change_time
        self.booking_agenda = booking_agenda
        self.booking_type = booking_type
        self.booking_notes = booking_notes
        self.gp_id = gp_id
        self.patient_id = patient_id

    # Book a new appointment with GP as a patient
    def book(self):
        query = """ INSERT INTO booking
        (booking_id, booking_start_time, booking_status,booking_status_change_time,
        booking_agenda, booking_type,gp_id,patient_id)
        VALUES ({},'{}','{}','{}','{}','{}',{},{});""".format('NULL', self.booking_start_time,
                                                              'booked', '2020-12-12 10:40:20.000',
                                                              self.booking_agenda,
                                                              self.booking_type, self.gp_id,
                                                              self.patient_id)
        db_execute(query)

    # Update an appointment with GP
    def update(self):
        pass
        query = """UPDATE booking 
                     SET booking_start_time = '{}', booking_status = '{}', 
                     booking_status_change_time = '{}', booking_agenda = '{}', booking_type = '{}',
                         booking_notes = '{}', gp_id = {}, patient_id = {}
                     WHERE booking_id = {}""".format(self.booking_start_time,
                                                     self.booking_status,
                                                     self.booking_status_change_time,
                                                     self.booking_agenda, self.booking_type,
                                                     self.booking_notes, self.gp_id, self.patient_id,
                                                     self.booking_id)

        db_execute(query)

    # Display GPs schedule for a specific date
    @staticmethod
    def select_gp_upcoming_day(gp_id, input_date):
        # Assuming that the date is provided in the form YYYY-MM-D(D)
        query = """SELECT booking_id,booking_start_time , booking_status, booking_agenda, 
                   booking_type, patient_id
                   FROM booking
                   WHERE gp_id = {} AND strftime('%Y-%m-%d', booking_start_time)  = '{}';""".format(gp_id, input_date)
        query_results = db_read_query(query)

        # Blank DataFrame Production
        # DateTimeIndex of daily_slots
        current_day_starting_time = input_date + " 08:00:00"

        slot_per_day = pd.date_range(current_day_starting_time, periods=54, freq='10T')
        empty_df = pd.DataFrame({'booking_start_time': slot_per_day})

        # # transform datatype to be able to join later
        query_results.booking_start_time = query_results.booking_start_time.astype('datetime64[ns]')

        # perform join
        df_select_day = pd.merge(empty_df, query_results, left_on='booking_start_time', right_on='booking_start_time',
                                 how='left').fillna(" ")

        return print(tabulate(df_select_day, headers='keys', tablefmt='psql'))

    #  Display GPs schedule for a specific week
    def select_gp_upcoming_week(self):
        pass

    # Display GP schedule for custom input
    def select_gp_upcoming_custom(self):
        pass

    # TODO Ask Matt what's the purpose of this function
    # Select
    def select_patient_previous_day(self):
        pass

    # TODO Ask Matt what's the purpose of this function
    # Select
    def select_patient_previous_week(self):
        pass

    # TODO Ask Matt what's the purpose of this function
    # Select
    def select_patient_previous_custom(self):
        pass

    # Select the appoint for an upcoming patient
    def select_patient_upcoming(self):
        pass

    # Select the booking of a specific GP for a specific date
    def select_booking_day(self):
        pass

    # Select the booking of a specific GP for a particular week
    def select_booking_week(self):
        pass

    # Select custom booking of a specific GP
    def select_booking_custom(self):
        pass

    # Gets availabilities of a all GPs for specific date except for specified GP
    def select_other_booking_day(self):
        pass

    # Gets availabilities of a all GPs for specific week except for specified GP
    def select_other_booking_week(self):
        pass

    # Gets availabilities of a all GPs for specific interval of time except for specified GP
    def select_other_booking_custom(self):
        pass

    # TODO what is the point of these again, sorry can't wrap my head around it
    #
    def check_booking_day(self):
        pass

    #
    def check_booking_week(self):
        pass

    #
    def check_booking_custom(self):
        pass

    #
    def check_other_booking_day(self):
        pass

    #
    def check_other_booking_week(self):
        pass

    #
    def check_other_booking_custom(self):
        pass

    # Cancel a specific appointment
    @staticmethod
    def cancel_appointment(booking_id):
        query = """DELETE FROM booking WHERE booking_id = {};""".format(booking_id)
        db_execute(query)




# DEVELOPMENT

# booking_id=None, booking_start_time=None, booking_status=None,
# booking_status_change_time=None, booking_agenda=None, booking_type=None,
# booking_notes=None, gp_id=None, patient_id=None

if __name__ == "__main__":
    # Testing book appointment method
    Appointment('Null','2020-12-08 10:00:00', 'confirmed', '2020-12-10 11:38:47.00',
                'booking agenda edit test', 'offline', '', 1, 1).book()

    # Testing Update Method
    # Appointment(1, '2020-12-08 10:00:00', 'confirmed', '2020-12-10 11:38:47.00',
    # 'booking agenda edit test', 'offline', '', 10, 10).update()

    # # Testing select GP upcoming day
    # Appointment.select_gp_upcoming_day(10, '2020-12-08')

    # Test deleting a specific booking
    Appointment.cancel_appointment(2)
