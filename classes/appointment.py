# appointment.py

# import libraries
import pandas as pd
import datetime as dt
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
    def select_gp_upcoming(select_type, gp_id, start_date, end_date=None):

        def master_gp_select(funct_gp_id, funct_start_date, funct_end_date = None):
            funct_end_date = pd.to_datetime(funct_end_date) + pd.DateOffset(hours=17)

            query = """SELECT booking_id,booking_start_time , booking_status, booking_agenda, booking_type, patient_id
                               FROM booking
                               WHERE gp_id = {} AND (strftime('%Y-%m-%d', booking_start_time) >= '{}' 
                               AND booking_start_time <= '{}');""".format(funct_gp_id, funct_start_date, funct_end_date)
            print(query)
            query_results = db_read_query(query)
            query_results.booking_start_time = query_results.booking_start_time.astype('datetime64[ns]')

            funct_start_date = pd.to_datetime(funct_start_date) + pd.DateOffset(hours=8)

            periods = 54 if (funct_end_date - funct_start_date).days == 0 else ((funct_end_date - funct_start_date).days+1) * 6 * 24
            print(periods)
            time = pd.date_range(start=pd.to_datetime(funct_start_date), periods=periods, freq='10Min').to_frame(
                name='booking_start_time').between_time('08:00', '16:50')
            df_select = pd.merge(time, query_results, left_on='booking_start_time', right_on='booking_start_time',
                                 how='left').fillna(" ")
            return print(tabulate(df_select, headers='keys', tablefmt='psql'))

        if select_type == 'day':
            master_gp_select(gp_id, start_date, start_date)

        elif select_type == 'week':
            end_date = pd.to_datetime(start_date) + pd.DateOffset(days = 7)
            master_gp_select(gp_id, start_date,end_date)

        elif select_type == 'custom':
            end_date = pd.to_datetime(end_date)
            master_gp_select(gp_id, start_date, end_date)


        #  Display GPs schedule for a specific week
        # @staticmethod
        # def select_gp_upcoming_week(gp_id, start_date):
        #     pass
        #
        # def select_gp_upcoming_custom(self):
        #     pass

    # TODO Ask Matt what's the purpose of this function
    # Select patient record of appointments
    @staticmethod
    def select_patient_previous(patient_id):
        query = """ SELECT booking_id,booking_start_time , booking_status, booking_agenda, booking_type, gp_id
                               FROM booking
                               WHERE patient_id == {} AND booking_start_time < '{}'""".format(patient_id,dt.datetime.now())

        query_results = db_read_query(query)

        return print(tabulate(pd.DataFrame(query_results), headers='keys', tablefmt='psql'))

        # # Select
        # def select_patient_previous_week(self):
        #     pass
        #
        # # Select
        # def select_patient_previous_custom(self):
        #     pass

    # Select the appoint for an upcoming patient
    @staticmethod
    def select_patient_upcoming(patient_id):
        query = """ SELECT booking_id,booking_start_time , booking_status, booking_agenda, booking_type, gp_id
                                       FROM booking
                                       WHERE patient_id == {} AND booking_start_time > '{}'""".format(patient_id,
                                                                                                      dt.datetime.now())

        query_results = db_read_query(query)

        return print(tabulate(pd.DataFrame(query_results), headers='keys', tablefmt='psql'))

    # Select the booking of a specific GP for a specific date
    @staticmethod
    def select_booking(select_type, gp_id, start_date, end_date=None):

        def master_booking_select(funct_gp_id, funct_start_date, funct_end_date=None):
            funct_end_date = pd.to_datetime(funct_end_date) + pd.DateOffset(hours=17)

            query = """SELECT booking_id,booking_start_time , booking_status, booking_agenda, booking_type, patient_id
                                           FROM booking
                                           WHERE gp_id = {} AND (strftime('%Y-%m-%d', booking_start_time) >= '{}' 
                                           AND booking_start_time <= '{}');""".format(funct_gp_id, funct_start_date,
                                                                                      funct_end_date)
            query_results = db_read_query(query)
            return print(tabulate(query_results, headers='keys', tablefmt='psql'))

        if select_type == 'day':
            master_booking_select(gp_id, start_date, start_date)

        elif select_type == 'week':
            end_date = pd.to_datetime(start_date) + pd.DateOffset(days = 7)
            master_booking_select(gp_id, start_date,end_date)
        elif select_type == 'custom':
            end_date = pd.to_datetime(end_date)
            master_booking_select(gp_id, start_date, end_date)


        # # Select the booking of a specific GP for a particular week
        # def select_booking_week(self):
        #     pass
        #
        # # Select custom booking of a specific GP
        # def select_booking_custom(self):
        #     pass

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
    @staticmethod
    def check_booking(select_type, gp_id, start_date, end_date=None):

        def master_gp_select(funct_gp_id, funct_start_date, funct_end_date=None):
            funct_end_date = pd.to_datetime(funct_end_date) + pd.DateOffset(hours=17)

            query = """SELECT booking_id,booking_start_time , booking_status, booking_agenda, booking_type, patient_id
                               FROM booking
                               WHERE gp_id = {} AND (strftime('%Y-%m-%d', booking_start_time) >= '{}' 
                               AND booking_start_time <= '{}');""".format(funct_gp_id, funct_start_date, funct_end_date)
            query_results = db_read_query(query)
            query_results.booking_start_time = query_results.booking_start_time.astype('datetime64[ns]')

            funct_start_date = pd.to_datetime(funct_start_date) + pd.DateOffset(hours=8)

            periods = 54 if (funct_end_date - funct_start_date).days == 0 else ((funct_end_date - funct_start_date).days + 1) * 6 * 24
            print(periods)
            time = pd.date_range(start=pd.to_datetime(funct_start_date), periods=periods, freq='10Min').to_frame(
                name='booking_start_time').between_time('08:00', '17:50')
            df_select = pd.merge(time, query_results, left_on='booking_start_time', right_on='booking_start_time',
                                 how='left').fillna(" ")
            final = df_select[df_select.booking_id == " "]
            return print(tabulate(final, headers='keys', tablefmt='psql'))

        if select_type == 'day':
            master_gp_select(gp_id, start_date, start_date)

        elif select_type == 'week':
            end_date = pd.to_datetime(start_date) + pd.DateOffset(days = 7)
            master_gp_select(gp_id, start_date,end_date)
        elif select_type == 'custom':
            end_date = pd.to_datetime(end_date)
            master_gp_select(gp_id, start_date, end_date)
        #
        # def check_booking_week(self):
        #     pass
        #
        # #
        # def check_booking_custom(self):
        #     pass

    # returns a bool value if there are availabilities for a specific GP
    @staticmethod
    def check_other_booking(select_type, gp_id, start_date, end_date=None):
        def master_gp_select(funct_gp_id, funct_start_date, funct_end_date=None):
            funct_end_date = pd.to_datetime(funct_end_date) + pd.DateOffset(hours=17)

            query = """SELECT booking_id,booking_start_time , booking_status, booking_agenda, booking_type, patient_id
                               FROM booking
                               WHERE gp_id = {} AND (strftime('%Y-%m-%d', booking_start_time) >= '{}' 
                               AND booking_start_time <= '{}');""".format(funct_gp_id, funct_start_date, funct_end_date)
            query_results = db_read_query(query)
            query_results.booking_start_time = query_results.booking_start_time.astype('datetime64[ns]')

            funct_start_date = pd.to_datetime(funct_start_date) + pd.DateOffset(hours=8)

            periods = 54 if (funct_end_date - funct_start_date).days == 0 else ((funct_end_date - funct_start_date).days + 1) * 6 * 24

            time = pd.date_range(start=pd.to_datetime(funct_start_date), periods=periods, freq='10Min').to_frame(
                name='booking_start_time').between_time('08:00', '17:50')
            df_select = pd.merge(time, query_results, left_on='booking_start_time', right_on='booking_start_time',
                                 how='left').fillna(" ")
            final = df_select[df_select.booking_id == " "]
            return final

        if select_type == 'day':

            if master_gp_select(gp_id, start_date, start_date).empty:
                print("No Bookings are available for GP on {}".format(start_date))
            else:
                print("GP has some availability on {}!".format(start_date))

        elif select_type == 'week':
            if master_gp_select(gp_id, start_date, start_date).empty:
                print("No Bookings are available for GP on {}".format(start_date))
            else:
                print("GP has some availability on {}!".format(start_date))
        elif select_type == 'custom':
            end_date = pd.to_datetime(end_date)
            master_gp_select(gp_id, start_date, end_date)
            if master_gp_select(gp_id, start_date, start_date).empty:
                print("No Bookings are available for GP on {}".format(start_date))
            else:
                print("GP has some availability on {}!".format(start_date))

        # #
        # def check_other_booking_week(self):
        #     pass
        #
        # #
        # def check_other_booking_custom(self):
        #     pass

    # Cancel a specific appointment
    @staticmethod
    def cancel_appointment(booking_id):
        query = """DELETE FROM booking WHERE booking_id = {};""".format(booking_id)
        db_execute(query)


# DEVELOPMENT

if __name__ == "__main__":

    # Testing book appointment method
    # Appointment('Null', '2020-12-13 10:00:00', 'confirmed', '2020-12-14 11:38:47.00',
    #             'booking agenda edit test', 'offline', '', 1, 1).book()

    # Testing Update Method
    # Appointment(1, '2020-12-08 10:00:00', 'confirmed', '2020-12-10 11:38:47.00',
    #             'booking agenda edit test', 'offline', '', 10, 10).update()

    # Testing select GP upcoming day
    # Appointment.select_gp_upcoming_day(1, '2020-12-08')

    # Appointments for upcoming week
    # Appointment.select_gp_upcoming_week(1, '2020-12-08')

    # Test deleting a specific booking
    # Appointment.cancel_appointment(3)
    Appointment.select_gp_upcoming('day', 1, '2020-12-09')

    # '2020-12-08', '2020-12-09'
    # print((pd.to_datetime('2020-12-09')-pd.to_datetime('2020-12-07')).days)

    # Appointment.select_patient_previous(1)
    #
    # Appointment.select_patient_upcoming(1)

    # Appointment.check_booking('custom', 1, '2020-12-08','2020-12-09')

    # Appointment.check_other_booking('custom', 1, '2020-12-08', '2020-12-09')
    # Appointment.select_booking('custom', 1, '2020-12-08','2020-12-09')
