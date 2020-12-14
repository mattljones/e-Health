# appointment.py

# import libraries
import pandas as pd
import datetime as dt
from tabulate import tabulate

# Switching path to master to get functions from utils folder
import sys
from pathlib import Path

path_to_master_repo = Path(__file__).parents[1]
sys.path.insert(1, str(path_to_master_repo))

# Importing utility methods from the 'system' package
from system import utils as u

"""Possible Utilities functions"""


def markdown_df(df):
    return print(tabulate(df, headers='keys', tablefmt='psql'))


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
        u.db_execute(query)

    # NOTE: should we be checking if the slot that the patient wants to book has not been previously booked and
    # doesn't fall on the weekend? Or should this be done in the front end, I think it would be easier to do it on the
    # front end

    # Update an appointment with GP
    # TODO: DONE as in the classed.md
    # TODO: Error handling, check if the appointment actually exists
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

        u.db_execute(query)

    # TODO: Check with Matt "do I understand it correctly you just want to view the details of a specific
    #  booking in the DF form
    # TODO: Error handling, check if the appointment actually exists
    # Generating an instance of an appointment to later update attributes based on user input
    @classmethod
    def select(cls, booking_id):
        booking_query = """SELECT booking_id AS 'Booking ID', p.patient_first_name AS 'Patient First Name',
                           p.patient_last_name AS 'Patient Last Name',booking_start_time AS 'Booking start time', 
                           booking_status AS 'Booking status',
                           booking_status_change_time AS 'Booking status change time',
                           booking_agenda AS 'Booking Agenda',booking_type AS 'Booking type', 
                           booking_notes AS 'Booking Notes'
                           FROM booking
                           JOIN patient p on booking.patient_id = p.patient_id 
                           WHERE booking_id = {}""".format(booking_id)
        booking_df = db_read_query(booking_query)

        return booking_df

    # Display GPs bookings for upcoming time span
    # TODO : DONE Display GPs bookings for upcoming day
    # TODO : DONE Display GPs bookings for upcoming week
    @staticmethod
    def select_GP(select_type, gp_id, start_date):

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

            schedule_day = u.db_read_query(day_query)

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
            df_select_week = u.week_empty_df(start_date, gp_id)

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
                time_row = dt.datetime.strptime(sql_result_df.loc[i, 'time'], '%H:%M:%S').strftime('%H:%M')
                df_select_week.loc[time_row, date_column] = sql_result_df.loc[i, 'booking_status']

            return df_select_week

    # Displays the DF of all pending appointment for a specific GP
    @staticmethod
    def select_GP_pending(gp_id):
        pass

    # Select patient record of appointments that they have already attended
    # TODO: DONE as in the classed.md
    @staticmethod
    def select_patient_previous(patient_id):
        query = """SELECT booking_id AS 'Appointment ID',b.gp_id AS 'GP ID', printf('DR.%s',g.gp_last_name) as GP,
                   date(booking_start_time) 'Appointment Date',
                   strftime('%H:%M:%S',booking_start_time) 'Appointment Date', booking_status AS 'Booking Status',
                   booking_type AS 'Booking Type', booking_agenda AS 'Booking Agenda',
                   booking_notes AS 'Notes from the Appointment'
                   FROM booking b
                   JOIN gp g ON b.gp_id = g.gp_id
                   WHERE patient_id == {} 
                   AND booking_start_time <= '{}'""".format(patient_id, dt.datetime.now().strftime("%Y-%m-%d %H:%M"))

        query_results = u.db_read_query(query)
        # Wrapping the text in Booking agenda and Notes from the Appointment
        query_results['Booking Agenda'] = query_results['Booking Agenda'].str.wrap(30)
        query_results['Notes from the Appointment'] = query_results['Notes from the Appointment'].str.wrap(30)

        # This variable stores the printable version of the DF
        query_results_print = query_results.to_markdown(tablefmt="grid", index=False)

        # Matt this ↓ is a DF for you to use, only with confirmed bookings
        query_results_confirmed_only = query_results[query_results['Booking Status'] == 'confirmed']
        query_results_confirmed_only_print = query_results_confirmed_only.to_markdown(tablefmt="grid", index=False)

        return query_results, query_results_print, query_results_confirmed_only, query_results_confirmed_only_print

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
            availability_df_day = Appointment.select_GP(select_type, gp_id, start_date)
            availability_df_day = availability_df_day.replace(
                ('Weekend', 'booked', 'rejected', 'confirmed', 'cancelled', 'time off', 'sick leave'),
                'Unavailable').drop(['Agenda', 'Type', 'Patient ID', 'Working Days'], axis=1)
            return availability_df_day

        elif select_type == 'week':
            availability_df_week = Appointment.select_GP(select_type, gp_id, start_date)
            availability_df_week = availability_df_week.replace(
                ('Weekend', 'booked', 'rejected', 'confirmed', 'cancelled', 'time off', 'sick leave'), 'Unavailable')
            return availability_df_week

    # Gets availabilities of a all GPs for specific start_date except for specified GP
    # TODO: Patient View : Display bookings for a specific upcoming time span of a GP that is not
    #  assigned to them by default
    @staticmethod
    def select_other_availability(select_type, gp_id, start_date):
        pass

    # Change status of a specific appointment
    # TODO:DONE rewrite the query for changing the appointment status to any
    @staticmethod
    def change_status(booking_id, new_status):
        query = """UPDATE booking SET booking_status = '{}' WHERE booking_id = {};""".format(booking_id, new_status)
        db_execute(query)

    # Confirm all of the appointments for a specific GP
    # TODO: Confirm all of the appointments for a specific GP
    @staticmethod
    def confirm_all_GP_pending(gp_id):
        query = """UPDATE booking SET booking_status = 'confirmed' 
                   WHERE gp_id = {} AND booking_status = 'booked';""".format(gp_id)
        db_execute(query)
        print("All appointments have been confirmed!")


# DEVELOPMENT

if __name__ == "__main__":
    # THIS WORKS! : Testing book appointment method
    # Appointment('Null', '2020-12-13 10:00:00', 'confirmed', '2020-12-14 11:38:47.00',
    #              'booking agenda edit test', 'offline', '', 1, 1).book()

    # THIS WORKS! : Testing Update Method
    # Appointment(1, '2020-12-08 10:00:00', 'confirmed', '2020-12-10 11:38:47.00',
    #             'booking agenda edit test', 'offline', '', 10, 10).update()

    # THIS WORKS! : Showing DF schedule for GP and Admin view
    # tabulate_df(Appointment.select_GP('week', 2, '2020-12-13'))
    # tabulate_df(Appointment.select_GP('day', 2, '2020-12-13'))

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

    # THIS WORKS! : Confirms all of the appointments
    # Appointment.confirm_all_GP_pending(2)

    # '2020-12-08', '2020-12-09'
    # print((pd.to_datetime('2020-12-09')-pd.to_datetime('2020-12-07')).days)

    Appointment.select_patient_previous(4)
    #
    # Appointment.select_patient_upcoming(1)

    # Appointment.check_booking('custom', 1, '2020-12-08','2020-12-09')

    # Appointment.check_other_booking('custom', 1, '2020-12-08', '2020-12-09')
    # Appointment.select_booking('custom', 1, '2020-12-08','2020-12-09')
