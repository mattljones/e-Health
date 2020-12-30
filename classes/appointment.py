# appointment.py

# import libraries
import pandas as pd
import datetime as dt
import random

# Switching path to master to get functions from utils folder
import sys
from pathlib import Path

path_to_master_repo = Path(__file__).parents[1]
sys.path.insert(1, str(path_to_master_repo))

# Importing utility methods from the 'system' package
from system import utils as u
from classes.schedule import Schedule


class Appointment:
    """
    Class defining all 'appointment' related methods.
    """

    def __init__(self, booking_id=None, booking_start_time=None, booking_status=None, booking_agenda=None,
                 booking_type=None, booking_notes=None, gp_id=None, patient_id=None):

        self.booking_id = booking_id
        self.booking_start_time = booking_start_time
        self.booking_status = booking_status
        self.booking_agenda = booking_agenda
        self.booking_type = booking_type
        self.booking_notes = booking_notes
        self.gp_id = gp_id
        self.patient_id = patient_id

    # Book a new appointment with GP as a patient
    def book(self):
        """
        :return: Boolean value if the booking was made. If false, this implies that:
        that particular GP already has a booking on that date i.e. DF returned from the DB != EmptyDF
        """

        # fist we need to check to make sure that the booking is still available

        booking_check_query_gp = """SELECT *
                                 FROM booking
                                 WHERE gp_id == {} AND booking_status <> ('rejected' or 'canceled')
                                 AND booking_start_time == '{}'
                                 AND (booking_status <> 'rejected' 
                                 OR  booking_status <> 'rejected')""".format(self.gp_id,
                                                                             self.booking_start_time)
        booking_check_result_gp = u.db_read_query(booking_check_query_gp).empty

        booking_check_query_patient = """SELECT *
                                         FROM booking
                                         WHERE patient_id == {}
                                         AND booking_start_time == '{}'""".format(self.patient_id,
                                                                                  self.booking_start_time)

        booking_check_result_patient = u.db_read_query(booking_check_query_patient).empty

        if dt.datetime.strptime(self.booking_start_time, '%Y-%m-%d %H:%M') <= dt.datetime.now():
            booking_check_result, reason = False, "You can not book an appointment in the past"
            return booking_check_result, reason

        if booking_check_result_gp and booking_check_result_patient:
            booking_check_result, reason = True, 'The appointment has been booked!'
            query = """ INSERT INTO booking
            (booking_id, booking_start_time, booking_status,
            booking_agenda, booking_type,gp_id,gp_last_name,patient_id,booking_status_change_time)
            VALUES ({},'{}','{}','{}','{}',{},'{}',{},'{}');""".format('NULL', self.booking_start_time,
                                                                       'booked',
                                                                       self.booking_agenda,
                                                                       self.booking_type, self.gp_id,
                                                                       Appointment.get_gp_last_name(self.gp_id),
                                                                       self.patient_id,
                                                                       dt.datetime.today().strftime("%Y-%m-%d %H:%M"))
            u.db_execute(query)

        elif booking_check_result_gp:
            booking_check_result, reason = False, "You already have a booking with a GP at this time and date"
        else:
            booking_check_result, reason = False, "GP is not available at this time and date"
        return booking_check_result, reason

    # Update an appointment with GP
    # Need to add Error handling, check if the appointment actually exists
    def update(self):

        # Updating booking notes
        query = """UPDATE booking 
                   SET booking_notes = '{}' 
                   WHERE booking_id = {}""".format(self.booking_notes, self.booking_id)
        u.db_execute(query)

    # Need to add  Error handling, check if the appointment actually exists
    # Generating an instance of an appointment to later update attributes based on user input

    @classmethod
    def select(cls, booking_id):

        """
        :param booking_id: provide a booking ID to view all of the information about that particular appointment
        :return: appointment_instance that has all the information about the booking
        :return: df_object is a raw dataframe that can be used to pull data from it
        :return: df_print is a user friendly DF that can be used to display information to the user
        """

        booking_query = """SELECT booking_id AS 'Apt. ID', booking.gp_id AS 'GP_id', booking.gp_last_name AS "GP",
                           p.patient_first_name AS 'Patient',
                           p.patient_last_name AS 'P. Last Name', booking.patient_id AS 'P ID',
                           booking_start_time AS 'Date', booking_status AS 'Status',
                           booking_status_change_time AS 'Status change time',
                           booking_agenda AS 'Agenda',booking_type AS 'Type', 
                           booking_notes AS 'Notes'
                           FROM booking
                           JOIN patient p on booking.patient_id = p.patient_id 
                           JOIN gp g on booking.gp_id = g.gp_id
                           WHERE booking_id = {}""".format(booking_id)

        df_object = u.db_read_query(booking_query)

        appointment_instance = cls(df_object.loc[0, 'Apt. ID'], df_object.loc[0, 'Date'],
                                   df_object.loc[0, 'Status'], df_object.loc[0, 'Agenda'],
                                   df_object.loc[0, 'Type'], df_object.loc[0, 'Notes'],
                                   df_object.loc[0, 'GP_id'], df_object.loc[0, 'P ID'])

        # Editing format of the table
        df_object['GP'] = 'Dr.' + df_object['GP'].astype(str) + ' (ID: ' + df_object['GP_id'].astype(str) + ')'
        df_object['Patient'] = df_object['Patient'].astype(str) + ' ' + df_object['P. Last Name'].astype(str) + \
                               " (ID: " + df_object['P ID'].astype(str) + ")"

        # Dropping no longer needed columns
        df_object = df_object.drop(columns=['GP_id', 'P. Last Name', 'P ID'])

        # Wrapping text for the lager sections of the DF
        df_object['Agenda'] = df_object['Agenda'].str.wrap(20)
        df_object['Notes'] = df_object['Notes'].str.wrap(20)
        df_object['Patient'] = df_object['Patient'].str.wrap(10)
        df_object['GP'] = df_object['GP'].str.wrap(15)

        df_print_notes = df_object[['Apt. ID', 'Patient', 'Notes']].to_markdown(tablefmt="grid", index=False)

        df_object.columns = ['Apt. ID []', 'GP []', 'Patient []', 'Date []', 'Status [1]', 'Status change time []',
                             'Agenda [2]', 'Type [3]', 'Notes [4]']
        df_print = df_object.to_markdown(tablefmt="grid", index=False)

        return appointment_instance, df_object, df_print, df_print_notes

    # Display GPs bookings for upcoming time span
    @staticmethod
    def select_GP(select_type, gp_id, start_date):

        """
        :param select_type: GP can select either the day view or the week view of their schedule
        :param gp_id: GP specific id that we can fetch from the  global variables
        :param start_date: GP can specify the first day of the week they wish to see
        :return: df_object is a raw dataframe that can be used to pull data from it
        :return: df_print is a user friendly DF that can be used to display information to the user
        """
        # this is in format '%Y-%m-%d'
        start_date = dt.datetime.strptime(start_date, '%Y-%m-%d').date()

        if select_type == 'day':

            # database queries
            day_query = """Select booking_id AS 'Booking ID',
                           strftime('%H:%M', booking_start_time) booking_hours,
                           booking_agenda AS 'Agenda', booking_type AS 'Type', b.patient_id AS 'Patient', 
                           p.patient_first_name, p.patient_last_name
                           FROM booking b
                           JOIN patient p ON b.patient_id = p.patient_id 
                           WHERE b.gp_id == {} 
                           AND strftime('%Y-%m-%d', booking_start_time) = '{}' 
                           AND booking_status == 'confirmed';""".format(gp_id, start_date)

            sql_result_df = u.db_read_query(day_query)
            raw_sql_df = sql_result_df[['Booking ID']]

            sql_result_df['Booking ID'] = '[' + sql_result_df['Booking ID'].astype(str) + ']'
            sql_result_df['Patient'] = sql_result_df['patient_first_name'].astype(str) + " " + \
                                       sql_result_df['patient_last_name'].astype(str) + \
                                       '(' + sql_result_df['Patient'].astype(str) + ')'

            sql_result_df = sql_result_df.drop(columns=['patient_first_name', 'patient_last_name'])
            # Producing the empty DataFrame for a day
            df_select_day_empty = u.day_empty_df(start_date, 2)
            # df_select_day = df_select_day.update(sql_result_df)

            df_object = pd.merge(df_select_day_empty, sql_result_df, left_on=df_select_day_empty.index,
                                 right_on='booking_hours', how='left')

            for i in range(len(df_object)):
                if pd.isnull(df_object.at[i, 'Booking ID']) == False:
                    df_object.at[i, 'Status'] = df_object.at[i, 'Booking ID']

            df_object = df_object.drop(columns=['Booking ID', 'booking_hours']).fillna('')
            df_object['Agenda'] = df_object['Agenda'].str.wrap(30)
            df_object['Patient'] = df_object['Patient'].str.wrap(15)
            df_object = df_object.rename(columns={"Status": "Bookings"})
            df_object = df_object.set_index(df_select_day_empty.index)

            # drop booking_dates and booking_hours as they are not needed anymore
            df_print_morning, df_print_afternoon = u.split_week_df(df_object, gp_id)
            df_print = df_object.to_markdown(tablefmt="grid", index=True)

            return df_object, df_print, df_print_morning, df_print_afternoon, raw_sql_df

        elif select_type == 'week':
            # forms an empty DF for a week from the date specified for a specific GP
            df_select_week = u.week_empty_df(start_date, gp_id)

            # Works out the end date for a week that was specified
            end_date = start_date + dt.timedelta(days=6)

            # SQLite query and forms a DF sql_result_df with booking for a specific GP
            week_query = """SELECT date(booking_start_time) start_date,strftime('%H:%M:%S',booking_start_time) time,
                       booking_status,booking_id
                       FROM booking
                       WHERE gp_id = {} 
                       AND start_date BETWEEN '{}' and '{}' 
                       AND booking_status = 'confirmed';""".format(gp_id, start_date, end_date)
            sql_result_df = u.db_read_query(week_query)
            raw_sql_df = sql_result_df[['booking_id']]
            sql_result_df['booking_id'] = '[' + sql_result_df['booking_id'].astype(str) + ']'

            # inserts all the data from the sql_result_df into the empty week DF
            for i in range(sql_result_df.shape[0]):
                date_column = dt.datetime.strptime(sql_result_df.loc[i, 'start_date'], '%Y-%m-%d').date()
                time_row = dt.datetime.strptime(sql_result_df.loc[i, 'time'], '%H:%M:%S').strftime('%H:%M')
                df_select_week.loc[time_row, date_column] = sql_result_df.loc[i, 'booking_id']

            df_object = df_select_week
            df_print_morning, df_print_afternoon = u.split_week_df(df_object, gp_id)
            df_print = df_object.to_markdown(tablefmt="grid", index=True)

            return df_object, df_print, df_print_morning, df_print_afternoon, raw_sql_df

    # Displays the DF of all appointments for a specific GP after the current time
    @staticmethod
    def select_GP_appt(gp_id):

        pending_query = """SELECT booking_id AS 'Apt. ID', p.patient_first_name AS 'Patient + ID',
                   p.patient_last_name AS 'P. Last Name', b.patient_id, booking_start_time AS 'Date', booking_status 
                   AS 'Status', booking_status_change_time AS 'Status change time',
                   booking_agenda AS 'Agenda',booking_type AS 'Type'
                   FROM booking b
                   JOIN patient p on b.patient_id = p.patient_id
                   WHERE b.gp_id =={}""".format(gp_id)

        df_object = u.db_read_query(pending_query)
        df_object['Patient + ID'] = df_object['Patient + ID'].astype(str) + ' ' + \
                                    df_object['P. Last Name'].astype(str) + ' (' + \
                                    df_object['patient_id'].astype(str) + ')'

        df_object['Apt. ID'] = "[" + df_object['Apt. ID'].astype(str) + "]"
        # Dropping no longer needed columns
        df_object = df_object.drop(columns=['P. Last Name', "patient_id"])
        df_object['Agenda'] = df_object['Agenda'].str.wrap(30)
        df_print = df_object.to_markdown(tablefmt="grid", index=False)

        return df_print

    # Displays the DF of all attended appointment for a specific GP
    @staticmethod
    def select_GP_attended(gp_id):
        """
        :param gp_id: GP specific id that we can fetch from the  global variables
        :return: df_object is a raw dataframe that can be used to pull data from it
        :return: df_print is a user friendly DF that can be used to display information to the user
        """

        pending_query = """SELECT booking_id AS 'Apt. ID', p.patient_first_name AS 'Patient + ID',
                   p.patient_last_name AS 'P. Last Name', b.patient_id, booking_start_time AS 'Date', booking_status 
                   AS 'Status', booking_status_change_time AS 'Status change time',
                   booking_agenda AS 'Agenda',booking_type AS 'Type'
                   FROM booking b
                   JOIN patient p on b.patient_id = p.patient_id
                   WHERE booking_status == 'attended'
                   AND b.gp_id =={}""".format(gp_id)

        df_object = u.db_read_query(pending_query)
        df_object['Patient + ID'] = df_object['Patient + ID'].astype(str) + ' ' + \
                                    df_object['P. Last Name'].astype(str) + ' (' + \
                                    df_object['patient_id'].astype(str) + ')'

        df_object['Apt. ID'] = "[" + df_object['Apt. ID'].astype(str) + "]"
        # Dropping no longer needed columns
        df_object = df_object.drop(columns=['P. Last Name', "patient_id"])
        df_object['Agenda'] = df_object['Agenda'].str.wrap(30)
        df_print = df_object.to_markdown(tablefmt="grid", index=False)

        return df_print

    # Displays the DF of confirmed appointments for a specific GP after the current time
    @staticmethod
    def select_GP_confirmed(gp_id):

        pending_query = """SELECT booking_id AS 'Apt. ID', b.patient_id, p.patient_first_name AS 'Patient + ID',
                   p.patient_last_name AS 'P. Last Name', booking_start_time AS 'Date', booking_status 
                   AS 'Status', booking_status_change_time AS 'Status change time',
                   booking_agenda AS 'Agenda',booking_type AS 'Type'
                   FROM booking b
                   JOIN patient p on b.patient_id = p.patient_id
                   WHERE booking_status == 'confirmed'
                   AND b.gp_id =={}""".format(gp_id)

        df_object = u.db_read_query(pending_query)

        df_object['Patient + ID'] = df_object['Patient + ID'].astype(str) + ' ' + \
                                    df_object['P. Last Name'].astype(str) + ' (' + \
                                    df_object['patient_id'].astype(str) + ')'

        df_object['Apt. ID'] = "[" + df_object['Apt. ID'].astype(str) + "]"

        # Dropping no longer needed columns
        df_with_p_id = df_object
        df_object = df_object.drop(columns=['P. Last Name', "patient_id"])
        df_object['Agenda'] = df_object['Agenda'].str.wrap(30)
        df_print = df_object.to_markdown(tablefmt="grid", index=False)

        return df_print, df_object, df_with_p_id

    # Displays the DF of all pending appointment for a specific GP after the current time
    @staticmethod
    def select_GP_pending(gp_id):
        """
        :param gp_id: GP specific id that we can fetch from the  global variables
        :return: df_object is a raw dataframe that can be used to pull data from it
        :return: df_print is a user friendly DF that can be used to display information to the user
        """

        pending_query = """SELECT booking_id AS 'Apt. ID', p.patient_first_name AS 'Patient + ID',
                   p.patient_last_name AS 'P. Last Name', b.patient_id, booking_start_time AS 'Date', booking_status 
                   AS 'Status', booking_status_change_time AS 'Status change time',
                   booking_agenda AS 'Agenda',booking_type AS 'Type'
                   FROM booking b
                   JOIN patient p on b.patient_id = p.patient_id
                   WHERE booking_status == 'booked' 
                   AND b.booking_start_time > '{}' 
                   AND b.gp_id =={}""".format(dt.datetime.now().strftime("%Y-%m-%d %H:%M"), gp_id)

        df_object = u.db_read_query(pending_query)
        df_object['Patient + ID'] = df_object['Patient + ID'].astype(str) + ' ' + \
                                    df_object['P. Last Name'].astype(str) + ' (' + \
                                    df_object['patient_id'].astype(str) + ')'

        df_object['Apt. ID'] = "[" + df_object['Apt. ID'].astype(str) + "]"
        # Dropping no longer needed columns
        df_object = df_object.drop(columns=['P. Last Name', "patient_id"])
        df_object['Agenda'] = df_object['Agenda'].str.wrap(30)
        df_print = df_object.to_markdown(tablefmt="grid", index=False)

        return df_object, df_print

    # Select patient record of appointments that they have already attended and any
    # appointments they might have in the future
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

        query = """SELECT booking_id AS 'Apt. ID',b.gp_id AS 'GP ID', printf('Dr. %s',b.gp_last_name) as GP,
                   strftime('%Y-%m-%d %H:%M',booking_start_time) 'Date', 
                   booking_status AS 'Status',booking_type AS 'Type', 
                   booking_agenda AS 'Booking Agenda', booking_notes AS 'Notes'
                   FROM booking b
                   JOIN gp g ON b.gp_id = g.gp_id
                   WHERE patient_id == {}
                   AND b.booking_status <> 'cancelled'
                   AND booking_start_time {}= '{}'""".format(patient_id, sign[timeframe],
                                                             dt.datetime.now().strftime("%Y-%m-%d %H:%M"))

        query_results = u.db_read_query(query)

        # Wrapping the text in Booking agenda and Notes from the Appointment
        query_results['GP'] = query_results['GP'].astype(str) + ' (ID: ' + query_results['GP ID'].astype(str) + ')'
        query_results = query_results.drop(columns='GP ID')
        # This variable stores the printable version of the DF

        if timeframe == 'previous' and status == 'confirmed':
            # Matt this ↓ is a DF for you to use, only with confirmed bookings
            # your input would look like select_patient('previous',patient_id,'confirmed')
            df_object = query_results[query_results['Status'] == 'confirmed'].drop(columns=['Status',
                                                                                            'Booking Agenda'])
            df_print = df_object.to_markdown(tablefmt="grid", index=False)
            return df_object, df_print

        else:
            query_results['Booking Agenda'] = query_results['Booking Agenda'].str.wrap(30)
            query_results['Notes'] = query_results['Notes'].str.wrap(30)
            df_object = query_results
            df_print = df_object.to_markdown(tablefmt="grid", index=False)
            return df_object, df_print

    # Select the booking of a specific GP for a specific start_date with specification of day or week
    @staticmethod
    def select_availability(select_type, gp_id, start_date):
        """
        :param select_type: Patient can select either the day view or the week view of their schedule
        :param gp_id: GP specific ID that we can fetch from the  global variables
        :param start_date: GP can specify the first day of the week they wish to see
        :return: df_object raw DataFrame containing all of the booking slots and their status
        :return: df_print user friendly DataFrame containing all of the booking slots and their status
        """

        if select_type == 'day':
            df_object = Schedule.select(gp_id, select_type, start_date)[0]
            df_object = df_object.drop(['Agenda', 'Type',
                                        'Patient (ID)'], axis=1).rename(columns={'Status': start_date})

        elif select_type == 'week':
            df_object = Schedule.select(gp_id, select_type, start_date)[0]

        df_object = df_object.replace(('rejected', 'cancelled'), "").replace(
            ('WEEKEND', 'booked', 'rejected', 'confirmed', 'cancelled', 'time off', 'sick leave', 'LUNCH', 'attended'),
            'Unavailable')

        column_number_list = list(range(0, df_object.shape[1]))
        row_number_list = list(range(0, df_object.shape[0]))

        for column_index in column_number_list:
            for row_index in row_number_list:
                if df_object.iloc[row_index, column_index] == "":
                    df_object.iloc[row_index, column_index] = '[' + str(column_index) + str(row_index) + ']'

        df_print = df_object.to_markdown(tablefmt="grid", index=True)
        df_print_morning, df_print_afternoon = u.split_week_df(df_object, gp_id)
        # The first number of the index that the user inputs is the column number and the rest is row position.
        # From the users input you can establish the date and time for a booking
        return df_object, df_print, df_print_morning, df_print_afternoon

    # Gets availabilities of a all GPs for specific start_date except for specified GP
    @staticmethod
    def select_other_availability(select_type, gp_id, start_date):

        """
        :param select_type: Patient can select either the day view or the week view of their schedule
        :param gp_id: GP specific ID that we can fetch from the  global variables, current GP ID
                      so we can exclude them from the search
        :param start_date: GP can specify the first day of the week they wish to see or a day, depending on the input
        :return: df_object raw DataFrame containing all of the booking slots and their status
        :return: df_print user friendly DataFrame containing all of the booking slots and their status
        :return: other_gp_id return the ID of the other ID that was found having the fewest appointments on date range
        :return:other_gp_last_name return the last name of that GP in the form "Dr.LastName"
        """

        start_date = dt.datetime.strptime(start_date, '%Y-%m-%d').date()

        if select_type == 'day':
            end_date = start_date
        elif select_type == 'week':
            end_date = start_date + dt.timedelta(days=6)

        query_get_gp_id = """SELECT b.gp_id, COUNT(date(booking_start_time)) Bookings_Per_Day, b.gp_last_name
                             FROM booking b
                             JOIN gp ON gp.gp_id = b.gp_id
                             WHERE (date(booking_start_time) BETWEEN '{}' AND '{}')
                             AND (booking_status <> 'canceled' AND booking_status <>'rejected') AND (b.gp_id <> {})
                             AND gp.gp_status == 'active'                             
                             GROUP BY b.gp_id
                             ORDER BY Bookings_Per_Day
                             LIMIT 1;""".format(start_date, end_date, gp_id)
        query_result = u.db_read_query(query_get_gp_id)

        if query_result.empty:
            #     Other GPs don't have any bookings for this date thus we can allocate the GP at Random
            gp_id_query = """SELECT gp_id, gp_last_name FROM gp WHERE gp_status == 'active'"""
            result = u.db_read_query(gp_id_query)
            other_gp_id = random.choice(result['gp_id'].tolist())
            other_gp_last_name = "DR." + result.loc[result['gp_id'] == other_gp_id, 'gp_last_name'].tolist()[0]
            number_of_bookings = 0

        else:
            number_of_bookings = query_result.loc[0, 'Bookings_Per_Day']
            other_gp_id = query_result.loc[0, 'gp_id']
            other_gp_last_name = "DR." + query_result.loc[0, 'gp_last_name']

        if (select_type == 'day' and number_of_bookings < 49) or (select_type == 'week' and number_of_bookings < 245):
            boolean_available = True
        else:
            df_object, df_print, other_gp_id, other_gp_last_name, \
            boolean_available, df_print_morning, df_print_afternoon = None, None, None, None, False, None, None

            return df_object, df_print, other_gp_id, other_gp_last_name, boolean_available, df_print_morning, \
                   df_print_afternoon

        df_object, df_print, df_print_morning, \
        df_print_afternoon = Appointment.select_availability(select_type, other_gp_id, str(start_date))

        return df_object, df_print, other_gp_id, other_gp_last_name, \
               boolean_available, df_print_morning, df_print_afternoon

    # Change status of a specific appointment
    @staticmethod
    def change_status(booking_id, new_status, reject_reason=None):
        """"
        :param booking_id: booking specific ID to change status for
        :param new_status: prove a new status to update to
        :param reject_reason: Optional input where we the GP must provide a reason for why they rejected an appointment
        """
        if new_status == 'rejected':

            query = """UPDATE booking SET booking_status = '{}', booking_agenda = '{}'
                       WHERE booking_id = {};""".format(new_status, reject_reason, booking_id)
            # print(query)
            u.db_execute(query)

        else:

            query = """UPDATE booking SET booking_status = '{}' WHERE booking_id = {};""".format(new_status, booking_id)
            u.db_execute(query)

    # Confirm all of the appointments for a specific GP
    @staticmethod
    def confirm_all_GP_pending(gp_id):
        """"
        :param gp_id: GP ID to confirm all of the appointments
        """
        query = """UPDATE booking SET booking_status = 'confirmed' 
                   WHERE gp_id = {} AND booking_status = 'booked';""".format(gp_id)
        u.db_execute(query)
        print("\nAll appointments have been confirmed!\n")

    @staticmethod
    def get_gp_last_name(gp_id):
        gp_last_name_query = """SELECT gp_last_name FROM gp WHERE gp_id == {} """.format(gp_id)
        return u.db_read_query(gp_last_name_query).loc[0, 'gp_last_name']


# DEVELOPMENT

if __name__ == "__main__":
    # Appointment.change_status(51, 'confirmed')
    # Appointment.change_status(52, 'confirmed')

    # print(Appointment.select_GP('week', 16, '2020-12-25')[2])
    # print(Appointment.select_GP('day', 16, '2020-12-25')[3])

    # confirmed_id = Appointment.select_GP_confirmed(16)[1]['Apt. ID'].values
    # print(confirmed_id)

    # gp_note = "test test test"
    # appointment = Appointment(booking_id=51, gp_id=51)
    # appointment.booking_notes = gp_note
    # appointment.update()
    # print(Appointment.select(globals.appt_id)[1].loc[0,"Notes [4]"])

    # tmp = Appointment.select_GP_pending(16)[0].index.values.size
    # print(tmp)
    # tmp = Appointment.select_GP_pending(16)[0]['Apt. ID'].values
    # usr_input = '['+'51'+']'
    # print(usr_input in tmp)
    # print(Appointment.select(51)[1].loc[0,"Apt. ID []"])
    # print(Appointment.select(51)[1].loc[0,"Notes [4]"])
    # print(Appointment.select_GP_appt(16))
    # print(Appointment.select_availability('week', 16, '2020-12-27')[2])
    # print(Appointment.select_availability('day', 1, '2020-12-23'))
    pass

    # Method test
    # Sequence for input for the class: booking_id, booking_start_time, booking_status,
    #                     booking_agenda, booking_type,gp_id,patient_id

    # THIS WORKS! : Testing book appointment method
    # print(Appointment('Null', '2021-01-12 12:00', 'booked',
    #                   'Testing booking a rejected appointment', 'offline', ' ', 9, 2).book())

    # THIS WORKS! : Testing Update Method
    # Appointment(booking_id=16, booking_notes='Testing updating').update()
    # print(Appointment.select(16)[1].loc[0,"Notes [4]"])

    # THIS WORKS! : Returns a DF for a specific booking based on the booking_id provided
    # print(Appointment.select(51)[3])

    # THIS WORKS! : Showing DF schedule for GP and Admin view
    # print(Appointment.select_GP('week', 1, '2020-12-13')[3])
    # print(Appointment.select_GP('day', 1, '2020-12-17')[3])

    # THIS WORKS! : Displays all of the appointments with a status 'booked' for a particular GP where date > now
    # print(Appointment.select_GP_pending(1)[1])

    # THIS WORKS! : Displays all of the upcoming appointments for a specific patient
    # To get the dataframe of only confirmed appointments then you will have to add a parameter at end 'confirmed'
    # I've combined select_patient_previous and select_patient_upcoming
    # print(Appointment.select_patient('previous', 2)[1])
    # print(Appointment.select_patient('upcoming', 51)[1])

    # THIS WORKS! : Showing DF schedule for Patient view
    # For this test I've used patient 9 since their GP by default is 2 so
    # we can easily compare the DF to make sure they look the same
    # print(Appointment.select_availability('week', 9, '2020-12-12')[1])
    # print(Appointment.select_availability('day', 10, '2020-12-28')[1])

    # THIS WORKS! : Showing DF schedule for Patient view
    # Queries the DB for a GP that is not current GP and finds a GP with fewest appointments.
    # Displays the DF of the availability for that GP
    # Appointment.select_other_availability(week, 16, 2020 - 12 - 29)
    # print(Appointment.select_other_availability('week', 16, '2021-01-29'))
    # print(Appointment.select_other_availability('week', 1, '2020-12-24')[5])

    # THIS WORKS! : Changes status for a specific booking
    # reject_reason = 'the booking was rejected for this reason: Test'
    # Appointment.change_status(2, 'booked')

    # THIS WORKS! : Confirms all of the appointments
    # Appointment.confirm_all_GP_pending(2)

    # tmp = Appointment.select_GP_confirmed(16)[2]
    #
    # # print(tmp)
    # # row = tmp.loc[tmp['Apt. ID'] == '[51]']
    # # print(int(row['patient_id'].values))
    #
    # id = int(tmp.loc[tmp['Apt. ID'] == '[51]']['patient_id'].values)
    # print(id)
    # # print(Appointment.select_GP_confirmed(2)[0])
    # print(dt.datetime.strptime(dt.datetime.now().strftime("%Y-%m-%d %H:%M"), '%Y-%m-%d %H:%M'))
