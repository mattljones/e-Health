# appointment.py

# import libraries
import pandas as pd
import datetime as dt

# Switching path to master to get functions from utils folder
import sys
from pathlib import Path

path_to_master_repo = Path(__file__).parents[1]
sys.path.insert(1, str(path_to_master_repo))

# Importing utility methods from the 'system' package
from system import utils as u

"""Possible Utilities functions"""


def markdown_df_idex_true(df):
    return print(df.to_markdown(tablefmt="grid", index=True))


def markdown_df_idex_false(df):
    return print(df.to_markdown(tablefmt="grid", index=False))


class Appointment:
    """
    Class defining all 'appointment' related methods.
    """

    def __init__(self, booking_id=None, booking_start_time=None, booking_status=None, booking_agenda=None,
                 booking_type=None,
                 booking_notes=None, gp_id=None, patient_id=None):

        self.booking_id = booking_id
        self.booking_start_time = booking_start_time
        self.booking_status = booking_status
        self.booking_agenda = booking_agenda
        self.booking_type = booking_type
        self.booking_notes = booking_notes
        self.gp_id = gp_id
        self.patient_id = patient_id

    # Book a new appointment with GP as a patient
    # TODO: DONE, checked and works flawlessly
    def book(self):
        query = """ INSERT INTO booking
        (booking_id, booking_start_time, booking_status,
        booking_agenda, booking_type,gp_id,patient_id,booking_status_change_time)
        VALUES ({},'{}','{}','{}','{}',{},{},'{}');""".format('NULL', self.booking_start_time,
                                                              'booked',
                                                              self.booking_agenda,
                                                              self.booking_type, self.gp_id,
                                                              self.patient_id,
                                                              dt.datetime.today().strftime("%Y-%m-%d %H:%M"))
        print(query)
        u.db_execute(query)

    # NOTE: should we be checking if the slot that the patient wants to book has not been previously booked and
    # doesn't fall on the weekend? Or should this be done in the front end, I think it would be easier to do it on the
    # front end

    # Update an appointment with GP
    # TODO: DONE as in the classed.md
    # TODO: Error handling, check if the appointment actually exists
    def update(self):
        # booking_id, booking_start_time, booking_status,
        # booking_agenda, booking_type, gp_id, patient_id, booking_status_change_time
        query = """UPDATE booking 
                     SET booking_start_time = '{}', booking_status = '{}', 
                     booking_status_change_time = '{}', booking_agenda = '{}', booking_type = '{}',
                         booking_notes = '{}', gp_id = {}, patient_id = {}
                     WHERE booking_id = {}""".format(self.booking_start_time,
                                                     self.booking_status,
                                                     dt.datetime.today().strftime("%Y-%m-%d %H:%M"),
                                                     self.booking_agenda, self.booking_type,
                                                     self.booking_notes, self.gp_id, self.patient_id,
                                                     self.booking_id)

        u.db_execute(query)

    # TODO: Error handling, check if the appointment actually exists
    # Generating an instance of an appointment to later update attributes based on user input
    @classmethod
    def select(cls, booking_id):
        booking_query = """SELECT booking_id AS 'Apt. ID', booking.gp_id AS 'GP_id', g.gp_last_name AS "GP",
                           p.patient_first_name AS 'Patient',
                           p.patient_last_name AS 'P. Last Name',booking_start_time AS 'Date', 
                           booking_status AS 'Status',
                           booking_status_change_time AS 'Status change time',
                           booking_agenda AS 'Agenda',booking_type AS 'Type', 
                           booking_notes AS 'Notes'
                           FROM booking
                           JOIN patient p on booking.patient_id = p.patient_id 
                           JOIN gp g on booking.gp_id = g.gp_id
                           WHERE booking_id = {}""".format(booking_id)

        df_object = u.db_read_query(booking_query)
        # Editing format of the table
        df_object['GP'] = 'Dr.' + df_object['GP'].astype(str) + ' (ID: ' + df_object['GP_id'].astype(str) + ')'
        df_object['Patient'] = df_object['Patient'].astype(str) + ' ' + df_object['P. Last Name'].astype(str)

        # Dropping no longer needed columns
        df_object = df_object.drop(columns=['GP_id', 'P. Last Name'])

        # Wrapping text for the lager sections of the DF
        df_object['Agenda'] = df_object['Agenda'].str.wrap(30)
        df_object['Notes'] = df_object['Notes'].str.wrap(30)

        df_print = df_object.to_markdown(tablefmt="grid", index=False)

        return df_object, df_print

    # Display GPs bookings for upcoming time span
    # TODO : DONE Display GPs bookings for upcoming day
    # TODO : DONE Display GPs bookings for upcoming week
    # TODO : Workout with Matt what is the functionality of this
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
            # formated
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
            sql_result_df = u.db_read_query(week_query)
            print(sql_result_df)
            # inserts all the data from the sql_result_df into the empty week DF
            for i in range(sql_result_df.shape[0]):
                date_column = dt.datetime.strptime(sql_result_df.loc[i, 'start_date'], '%Y-%m-%d').date()
                time_row = dt.datetime.strptime(sql_result_df.loc[i, 'time'], '%H:%M:%S').strftime('%H:%M')
                df_select_week.loc[time_row, date_column] = sql_result_df.loc[i, 'booking_status']

            return df_select_week

    # TODO: DONE Displays the DF of all pending appointment for a specific GP after the current time
    @staticmethod
    def select_GP_pending(gp_id):
        pending_query = """SELECT booking_id AS 'Apt. ID', p.patient_first_name AS 'Patient',
                   p.patient_last_name AS 'P. Last Name',booking_start_time AS 'Date', booking_status AS 'Status',
                   booking_status_change_time AS 'Status change time',booking_agenda AS 'Agenda',booking_type AS 'Type'
                   FROM booking b
                   JOIN patient p on b.patient_id = p.patient_id
                   WHERE booking_status == 'booked' 
                   AND b.booking_start_time > '{}' 
                   AND b.gp_id =={}""".format(dt.datetime.now().strftime("%Y-%m-%d %H:%M"), gp_id)

        df_object = u.db_read_query(pending_query)
        df_object['Patient'] = df_object['Patient'].astype(str) + ' ' + df_object['P. Last Name'].astype(str)

        # Dropping no longer needed columns
        df_object = df_object.drop(columns='P. Last Name')
        df_object['Agenda'] = df_object['Agenda'].str.wrap(30)
        df_print = df_object.to_markdown(tablefmt="grid", index=False)

        return df_object, df_print

    # Select patient record of appointments that they have already attended
    # TODO: DONE as in the classed.md
    @staticmethod
    def select_patient(timeframe, patient_id, status=None):
        """"
        param timeframe: previous or upcoming
        :param patient_id: Patient specific id that we can fetch from the  global variables
        :param status: Optional, so for Patient's records to match with prescriptions
        :return: df_object = Raw Dataframe that can be used to manipulate the data
        :return: df_print = User friendly DF that can be printed
        """
        timeframe = timeframe.lower()
        sign = {'previous': '<', 'upcoming': '>'}

        query = """SELECT booking_id AS 'Apt. ID',b.gp_id AS 'GP ID', printf('Dr. %s',g.gp_last_name) as GP,
                   strftime('%Y-%M-%d %H:%M',booking_start_time) 'Date', 
                   booking_status AS 'Booking Status',booking_type AS 'Type', 
                   booking_agenda AS 'Booking Agenda', booking_notes AS 'Notes'
                   FROM booking b
                   JOIN gp g ON b.gp_id = g.gp_id
                   WHERE patient_id == {} 
                   AND booking_start_time {}= '{}'""".format(patient_id, sign[timeframe],
                                                             dt.datetime.now().strftime("%Y-%m-%d %H:%M"))

        query_results = u.db_read_query(query)

        # Wrapping the text in Booking agenda and Notes from the Appointment
        query_results['Booking Agenda'] = query_results['Booking Agenda'].str.wrap(30)
        query_results['Notes'] = query_results['Notes'].str.wrap(30)
        query_results['GP'] = query_results['GP'].astype(str) + ' (ID: ' + query_results['GP ID'].astype(str) + ')'
        query_results = query_results.drop(columns='GP ID')
        # This variable stores the printable version of the DF

        if timeframe == 'previous' and status == 'confirmed':
            # Matt this ↓ is a DF for you to use, only with confirmed bookings
            # your input would look like select_patient('previous',patient_id,'confirmed')
            df_object = query_results[query_results['Booking Status'] == 'confirmed'].drop(columns=['Booking Status',
                                                                                                    'Booking Agenda'])
            df_print = df_object.to_markdown(tablefmt="grid", index=False)
            return df_object, df_print

        else:
            df_object = query_results
            df_print = df_object.to_markdown(tablefmt="grid", index=False)
            return df_object, df_print

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

        # Change lunchtime to unuav

        get_gp_query = """SELECT gp_id FROM patient WHERE patient_id = {}""".format(patient_id)
        gp_id = u.db_read_query(get_gp_query).loc[0, 'gp_id']

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
    def select_other_availability(start_date):
        query_get_gp_id = """SELECT gp_id, count(gp_id) 'appoint_per_gp' FROM booking GROUP BY gp_id 
                             ORDER BY appoint_per_gp LIMIT 1"""
        gp_id_min_bookings = u.db_read_query(query_get_gp_id).iloc[0][0]
        print(gp_id_min_bookings)

    # Change status of a specific appointment
    # TODO: DONE rewrite the query for changing the appointment status to any
    @staticmethod
    def change_status(booking_id, new_status):
        query = """UPDATE booking SET booking_status = '{}' WHERE booking_id = {};""".format(booking_id, new_status)
        u.db_execute(query)

    # Confirm all of the appointments for a specific GP
    # TODO: DONE Confirm all of the appointments for a specific GP
    @staticmethod
    def confirm_all_GP_pending(gp_id):
        query = """UPDATE booking SET booking_status = 'confirmed' 
                   WHERE gp_id = {} AND booking_status = 'booked';""".format(gp_id)
        u.db_execute(query)
        print("All appointments have been confirmed!")


# DEVELOPMENT

if __name__ == "__main__":
    # THIS WORKS! : Testing book appointment method
    # Sequence for input: booking_id, booking_start_time, booking_status,
    #                     booking_agenda, booking_type,gp_id,patient_id
    # Appointment('Null', '2020-12-13 10:00', 'confirmed',
    #              'booking agenda edit test', 'offline', ' ', 1, 1).book()

    # THIS WORKS! : Testing Update Method
    # Appointment(60, '2020-12-13 10:00', 'confirmed',
    #              'booking agenda edit test 1', 'online', ' ', 10, 10).update()

    # THIS WORKS! : Returns a DF for a specific booking based on the booking_id provided
    # print(Appointment.select(10)[1])

    # THIS WORKS! : Showing DF schedule for GP and Admin view
    # markdown_df_index_true(Appointment.select_GP('week', 2, '2020-12-13'))
    # markdown_df_index_false(Appointment.select_GP('day', 2, '2020-12-13'))

    # THIS WORKS! : Showing DF schedule for Patient view
    # For this test I've used patient 9 since their GP by default is 2 so
    # we can easily compare the DF to make sure they look the same
    # markdown_df_idex_true(Appointment.select_availability('week', 9, '2020-12-13'))
    # markdown_df_idex_false(Appointment.select_availability('day', 9, '2020-12-13'))

    # Appointments for upcoming week
    # Appointment.select_gp_upcoming_week(1, '2020-12-08')

    # Test deleting a specific booking
    # Appointment.cancel_appointment(3)
    # Appointment.select_gp_upcoming( 1)

    # THIS WORKS! : Confirms all of the appointments
    # Appointment.confirm_all_GP_pending(2)

    # THIS WORKS! : Displays all of the appointments for a patient that were in the past
    # Appointment.select_patient_previous(4)

    # THIS WORKS! : Displays all of the upcoming appointments for a specific patient
    # print(Appointment.select_patient('previous', 4, 'confirmed')[1])

    # THIS WORKS! : Displays all of the appointments with a status 'booked' for a particular GP where date > now
    # print(Appointment.select_GP_pending(1)[1])

    # Display
    # Appointment.select_other_availability('2020-12-09')

    # Appointment.check_booking('custom', 1, '2020-12-08','2020-12-09')

    # Appointment.check_other_booking('custom', 1, '2020-12-08', '2020-12-09')
    # Appointment.select_booking('custom', 1, '2020-12-08','2020-12-09')
