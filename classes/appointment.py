# appointment.py

# import libraries
import pandas as pd
import datetime as dt
import sqlite3 as sql
# import calendar
from tabulate import tabulate

"""Possible Utilities functions"""


def tabulate_df(df):
    return print(tabulate(df, headers='keys', tablefmt='psql'))


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


def week_empty_df(start_date, gp_id):
    days = pd.date_range(start=start_date, periods=7, freq='D')
    times = pd.date_range(start='08:00:00', periods=54, freq='10Min')  # .to_frame(name='Working Hours',index=False)
    week_df = pd.DataFrame(index=times.time, columns=days.date)

    working_day_query = """SELECT gp_working_days FROM gp where gp_id == {};""".format(gp_id)
    working_day = db_read_query(working_day_query).loc[
        0, 'gp_working_days']  # will need a query to pull the first working day for a specific GP

    # This part of the code works out when the GP has weekends and populates those days with status "Weekend"
    weekend_day_range = [(working_day + 5) % 7, (working_day + 6) % 7]

    for i in range(7):
        if week_df.columns[i].weekday() in weekend_day_range:
            week_df[week_df.columns[i]] = 'Weekend'
    return week_df.fillna(" ")


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
    # TODO: DONE
    def book(self):
        query = """ INSERT INTO booking
        (booking_id, booking_start_time, booking_status,booking_status_change_time,
        booking_agenda, booking_type,gp_id,patient_id)
        VALUES ({},'{}','{}','{}','{}','{}',{},{});""".format('NULL', self.booking_start_time,
                                                              'booked', dt.datetime.today(),
                                                              self.booking_agenda,
                                                              self.booking_type, self.gp_id,
                                                              self.patient_id)
        db_execute(query)

    # NOTE: should we be checking if the slot that the patient wants to book has not been previously booked and
    # doesn't fall on the weekend? Or should this be done in the front end, I think it would be easier to do it on the
    # front end

    # Update an appointment with GP
    # TODO: DONE as in the classed.md
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

    # Display GPs bookings for upcoming time span
    # TODO : DONE Display GPs bookings for upcoming day
    # TODO : DONE Display GPs bookings for upcoming wee
    @staticmethod
    def select(select_type, gp_id, start_date):

        """
        :param select_type: GP can select either the day view or the week view of their schedule
        :param gp_id: GP specific id that we can fetch from the  global variables
        :param start_date: GP can specify the first day of the week they wish to see
        :return: DataFrame containing all of the booking slots and their status
        """

        if select_type == 'day':

            # this is in format '%Y-%m-%d'
            day_selection = dt.datetime.strptime(start_date, '%Y-%m-%d').date()

            # database queries
            day_query = """Select strftime('%Y-%m-%d', booking_start_time) booking_dates, 
                       strftime('%Y-%m-%d %H:%M', booking_start_time) booking_hours, 
                       booking_status AS 'Booking Status', 
                       booking_agenda AS 'Agenda', booking_type AS 'Type', patient_id AS 'Patient ID', 
                       gp_working_days AS 'Working Days' 
                       FROM booking b left join gp g on b.gp_id = g.gp_id 
                       WHERE b.gp_id = {} AND booking_dates = '{}';""".format(gp_id, day_selection)

            schedule_day = db_read_query(day_query)

            # Producing the empty DataFrame for a day
            date_for_splits = dt.datetime.combine(day_selection, dt.time(8, 0))
            # produce a DateTimeIndex of daily_slots
            daily_slots = pd.date_range(date_for_splits, periods=54, freq='10T')
            # Putting it together
            df_raw = pd.DataFrame({'Booking Start Time': daily_slots})

            # transform datatype to be able to join later
            schedule_day.booking_hours = schedule_day.booking_hours.astype('datetime64[ns]')

            # perform join
            df_select_day = pd.merge(df_raw, schedule_day, left_on='Booking Start Time', right_on='booking_hours',
                                     how='left')

            # drop booking_dates and booking_hours as they are not needed anymore
            df_select_day = df_select_day.drop(columns=['booking_dates', 'booking_hours']).fillna("")

            return df_select_day

        elif select_type == 'week':
            # forms an empty DF for a week from the date specified for a specific GP
            df_select_week = week_empty_df(start_date, gp_id)

            # Works out the end date for a week that was specified
            end_date = dt.datetime.strptime(start_date, "%Y-%m-%d").date() + dt.timedelta(days=6)

            # SQLite query and forms a DF sql_result_df with booking for a specific GP
            week_query = """SELECT date(booking_start_time) start_date,strftime('%H:%M:%S',booking_start_time) time,
                       booking_status
                       FROM booking
                       WHERE gp_id = {} 
                       AND start_date BETWEEN '{}' and '{}';""".format(gp_id, start_date, end_date)
            sql_result_df = db_read_query(week_query)

            # inserts all the data from the sql_result_df into the empty week DF
            for i in range(sql_result_df.shape[0]):
                date_column = dt.datetime.strptime(sql_result_df.loc[i, 'start_date'], '%Y-%m-%d').date()
                time_row = dt.datetime.strptime(sql_result_df.loc[i, 'time'], '%H:%M:%S').time()
                df_select_week.loc[time_row, date_column] = sql_result_df.loc[i, 'booking_status']

            return df_select_week

    # Select patient record of appointments that they have already attended
    # TODO: DONE as in the classed.md
    @staticmethod
    def select_patient_previous(patient_id):
        query = """ SELECT booking_id,booking_start_time , booking_status, booking_agenda, booking_type, gp_id
                               FROM booking
                               WHERE patient_id == {} AND booking_start_time < '{}'""".format(patient_id,
                                                                                              dt.datetime.now())

        query_results = db_read_query(query)

        return print(tabulate(pd.DataFrame(query_results), headers='keys', tablefmt='psql'))

    # Select the appoint for an upcoming patient
    # TODO: DONE as in the classed.md
    @staticmethod
    def select_patient_upcoming(patient_id):
        query = """ SELECT booking_id,booking_start_time , booking_status, booking_agenda, booking_type, gp_id
                                       FROM booking
                                       WHERE patient_id == {} AND booking_start_time > '{}'""".format(patient_id,
                                                                                                      dt.datetime.now())

        query_results = db_read_query(query)

        return print(tabulate(pd.DataFrame(query_results), headers='keys', tablefmt='psql'))

    # Select the booking of a specific GP for a specific start_date with specification of day or week
    # TODO: DONE Patient View : Display bookings for a specific upcoming time span
    @staticmethod
    def select_availability(select_type, patient_id, start_date):

        """
        :param select_type: Patient can select either the day view or the week view of their schedule
        :param patient_id: GP specific id that we can fetch from the  global variables
        :param start_date: GP can specify the first day of the week they wish to see
        :return: DataFrame containing all of the booking slots and their status
        """

        get_gp_query = """SELECT gp_id FROM patient WHERE patient_id = {}""".format(patient_id)
        gp_id = db_read_query(get_gp_query).loc[0, 'gp_id']

        if select_type == 'day':
            availability_df_day = Appointment.select(select_type, gp_id, start_date)
            availability_df_day = availability_df_day.replace(
                ('Weekend', 'booked', 'rejected', 'confirmed', 'cancelled', 'time off', 'sick leave'),
                'Unavailable').drop(['Agenda', 'Type', 'Patient ID', 'Working Days'], axis=1)
            return availability_df_day

        elif select_type == 'week':
            availability_df_week = Appointment.select(select_type, gp_id, start_date)
            availability_df_week = availability_df_week.replace(
                ('Weekend', 'booked', 'rejected', 'confirmed', 'cancelled', 'time off', 'sick leave'), 'Unavailable')
            return availability_df_week

    # Gets availabilities of a all GPs for specific start_date except for specified GP
    # TODO: Patient View : Display bookings for a specific upcoming time span of a GP that is not assigned to them by default
    def select_other_booking_day(self):
        pass

    # Gets availabilities of a all GPs for specific week except for specified GP
    # TODO: Patient View : Display bookings for a specific upcoming time span of a GP that is not assigned to them by default
    def select_other_booking_week(self):
        pass

    # Gets availabilities of a all GPs for specific interval of time except for specified GP
    # TODO: Patient View : Display bookings for a specific upcoming time span of a GP that is not assigned to them by default
    def select_other_booking_custom(self):
        pass

    # Select the booking of a gp that is not your default GP for a specific start_date with specification of day or week
    @staticmethod
    # TODO: Ask Matt what is the point of these
    def check_booking_day(select_type, gp_id, start_date, end_date=None):
        pass

    def check_booking_week(self):
        pass

    def check_booking_custom(self):
        pass

    # returns a bool value if there are availabilities for a specific GP
    @staticmethod
    # TODO: Patient View : returns a boolean value if a specific GP has availability ofr the provide time frame
    def check_other_booking(select_type, gp_id, start_date, end_date=None):
        pass

    # TODO: Patient View : returns a boolean value if a specific GP has availability ofr the provide time frame
    def check_other_booking_week(self):
        pass

    # TODO: Patient View : returns a boolean value if a specific GP has availability ofr the provide time frame
    def check_other_booking_custom(self):
        pass

    # Cancel a specific appointment
    # TODO rewrite the query for changing the appointment status to canceled
    @staticmethod
    def cancel_appointment(booking_id):
        query = """UPDATE booking SET booking_status = 'cancelled' WHERE booking_id = {};""".format(booking_id)
        db_execute(query)

    # Reject a specific appointment
    # TODO:DONE rewrite the query for changing the appointment status to rejected
    @staticmethod
    def reject_appointment(booking_id):
        query = """UPDATE booking SET booking_status = 'rejected' WHERE booking_id = {};""".format(booking_id)
        db_execute(query)


# DEVELOPMENT

if __name__ == "__main__":
    # THIS WORKS! : Testing book appointment method
    # Appointment('Null', '2020-12-13 10:00:00', 'confirmed', '2020-12-14 11:38:47.00',
    #              'booking agenda edit test', 'offline', '', 1, 1).book()

    # THIS WORKS! : Testing Update Method
    # Appointment(1, '2020-12-08 10:00:00', 'confirmed', '2020-12-10 11:38:47.00',
    #             'booking agenda edit test', 'offline', '', 10, 10).update()

    # THIS WORKS! : Showing DF schedule for GP and Admin view
    # tabulate_df(Appointment.select('week', 2, '2020-12-13'))
    # tabulate_df(Appointment.select('day', 2, '2020-12-13'))

    # THIS WORKS! : Showing DF schedule for Patient view
    # For this test I've used patient 9 since their GP by default is 2 so
    # we can easily compare the DF to make sure they look the same
    # tabulate_df(Appointment.select_availability('week', 9, '2020-12-13'))
    # tabulate_df(Appointment.select_availability('day', 9, '2020-12-13'))

    # Appointments for upcoming week
    # Appointment.select_gp_upcoming_week(1, '2020-12-08')

    # Test deleting a specific booking
    # Appointment.cancel_appointment(3)
    # Appointment.select_gp_upcoming('day', 1, '2020-12-09')

    # '2020-12-08', '2020-12-09'
    # print((pd.to_datetime('2020-12-09')-pd.to_datetime('2020-12-07')).days)

    # Appointment.select_patient_previous(1)
    #
    # Appointment.select_patient_upcoming(1)

    # Appointment.check_booking('custom', 1, '2020-12-08','2020-12-09')

    # Appointment.check_other_booking('custom', 1, '2020-12-08', '2020-12-09')
    # Appointment.select_booking('custom', 1, '2020-12-08','2020-12-09')
