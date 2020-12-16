# schedule.py

# import libraries
import pandas as pd
import sqlite3 as sql
import datetime
from system import utils as u


class Schedule:
    '''
    Class defining all 'schedule' related methods.
    '''

    @staticmethod  # SELECT day - STATIC
    def select(gp_id, type, start_date):
        '''
        Selection of all database entries for a specific day
        :param gp_id: gp_id that is stored in database/db_comp0066.db
        :param type: 'day' for a day's schedule, 'week' for a week's schedule (starting at start_date + 6 days)
        :param start_date: e.g. 2020-12-8
        :return: DataFrame for a day or week (non-formatted & formatted)
        '''
        if type == 'day':
            # start_date transformation str to datetime
            start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()

            # Initialize query
            day_query = """
                            Select
                                b.booking_status AS 'Booking Status Old',
                                strftime('%H:%M', b.booking_start_time) AS 'booking_hours',
                                b.booking_agenda AS 'Agenda',
                                b.booking_type AS 'Type',
                                b.patient_id AS 'Patient (ID)',
                                p.patient_first_name AS 'Patient First Name',
                                p.patient_last_name AS 'Patient Last Name'
                            FROM
                                booking as b
                            LEFT JOIN
                                patient p on b.patient_id = p.patient_id
                            WHERE
                                b.gp_id = {}
                            AND
                                strftime('%Y-%m-%d', b.booking_start_time) = '{}';""".format(gp_id, start_date)
            # Execute query
            sql_result_df = u.db_read_query(day_query)

            # Include 'Patient First Name' and 'Patient Last Name' in 'Patient (ID)' column
            sql_result_df['Patient (ID)'] = sql_result_df['Patient First Name'].astype(str) + ' ' + sql_result_df[
                'Patient Last Name'].astype(str) + ' (' + sql_result_df['Patient (ID)'].astype(str) + ')'

            # Producing the empty DataFrame for a day
            df_select_day_empty = u.day_empty_df(start_date, 2)

            df_object = pd.merge(df_select_day_empty, sql_result_df, left_on=df_select_day_empty.index,
                                 right_on='booking_hours', how='left')

            for i in range(len(df_object)):
                if pd.isnull(df_object.at[i, 'Booking Status Old']) == False:
                    df_object.at[i, 'Status'] = df_object.at[i, 'Booking Status Old']

            # drop columns that are not used anymore
            df_object = df_object.drop(
                columns=['Booking Status Old', 'booking_hours', 'Patient First Name', 'Patient Last Name']).fillna('')

            # Wrap text in 'Agenda' column
            df_object['Agenda'] = df_object['Agenda'].str.wrap(30)

            # Set index
            df_object = df_object.set_index(df_select_day_empty.index)

            # Produce df_print
            df_print = df_object.to_markdown(tablefmt="grid", index=True)

            return df_object, df_print

        if type == 'week':

            # Transforms start_date to datatime object
            start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()
            # start_date + 6 days = end_date
            end_date = start_date + datetime.timedelta(days=6)

            # SQLite query and forms a DF df_object with booking for a specific GP
            # Initialize query
            week_query = """
                            SELECT
                                date(booking_start_time) start_date,
                                strftime('%H:%M',booking_start_time) time,
                                booking_status
                            FROM
                                booking
                            WHERE
                                gp_id = {} 
                            AND
                                start_date BETWEEN '{}' and '{}';""".format(gp_id, start_date, end_date)
            # Execute query
            sql_result_df = u.db_read_query(week_query)

            # Produce empty DF for a week from the date specified for a specific GP
            df_object = u.week_empty_df(start_date, gp_id)

            # inserts all the data from the df_object into the empty week DF
            for i in range(len(sql_result_df)):
                date_column = datetime.datetime.strptime(sql_result_df.loc[i, 'start_date'], '%Y-%m-%d').date()
                time_row = datetime.datetime.strptime(sql_result_df.loc[i, 'time'], '%H:%M').strftime('%H:%M')
                df_object.loc[time_row, date_column] = sql_result_df.loc[i, 'booking_status']

            # Produce df_print
            df_print = df_object.to_markdown(tablefmt="grid", index=True)

        return df_object, df_print

    @staticmethod  # SELECT select_upcoming_timeoff - STATIC
    def select_upcoming_timeoff(gp_id):
        '''
        Select all upcoming time offs (sick leave and time off) for a gp
        :param gp_id: gp_id that is stored in database/db_comp0066.db
        :return: DataFrame with upcoming timeoffs of a specific gp (non-formatted & formatted)
        '''

        # Initialize query
        upcoming_timeoff_query = '''
                                SELECT DISTINCT
                                    strftime('%Y-%m-%d', booking_start_time) AS 'Date',
                                    booking_status AS 'Timeoff Type'
                                FROM
                                    booking
                                WHERE
                                    gp_id = {}
                                AND
                                    strftime('%Y-%m-%d', booking_start_time) >= '{}'
                                AND
                                    booking_status IN ('time off', 'sick leave');'''.format(gp_id,
                                                                                              datetime.datetime.now().strftime(
                                                                                                  "%Y-%m-%d"))

        # Execute query
        df_object = u.db_read_query(upcoming_timeoff_query)

        # produce df_print
        df_print = df_object.to_markdown(tablefmt="grid", index=False)

        return df_object, df_print

    @staticmethod  # SELECT check_timeoff_conflict - STATIC
    def check_timeoff_conflict(gp_id, start_date, end_date):
        '''
        Checks if a gp has no time off during a specific time period and returns a Boolean.
        :param gp_id: gp_id that is stored in database/db_comp0066.db
        :param start_date: e.g. 2020-12-8
        :param end_date: e.g. 2020-12-8
        :return: Boolean: True if conflict, False if NO conflict, DataFrame with the conflict slots (non-formatted & formatted)
        '''

        # start_date transformation str to datetime
        start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')
        # adding time: '%Y-%m-%d 08:00'
        start_date = datetime.datetime.combine(start_date.date(), datetime.time(8, 0))

        # end_date transformation str to datetime
        end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d')
        # adding time: '%Y-%m-%d 16:50'
        end_date = datetime.datetime.combine(end_date.date(), datetime.time(16, 50))

        # Range of 10 min slots from start_date to end_date
        timeoff_range = pd.date_range(start_date, end_date, freq='10min').strftime('%Y-%m-%d %H:%M').tolist()

        # Deletion of 10 min slots that are outside of GP working hours
        new_timeoff_range = []
        for i in range(len(timeoff_range)):
            if '08:00' <= timeoff_range[i][11:] <= '16:50':
                new_timeoff_range.append(timeoff_range[i])
        # connection to database
        conn = sql.connect("database/db_comp0066.db")
        # Create cursor
        c = conn.cursor()
        # Creating empty DataFrame
        df_object = pd.DataFrame()
        # Insert into database
        for i in range(len(new_timeoff_range)):
            # Execute query
            c.execute("""
                        SELECT
                            booking_id,
                            booking_start_time,
                            booking_status
                        FROM
                            booking
                        WHERE
                            strftime('%Y-%m-%d %H:%M', booking_start_time) = ?
                        AND
                            gp_id = ?
                        AND
                            booking_status IN ('confirmed', 'booked');""", (new_timeoff_range[i], gp_id))
            # Appending to empty DataFrame
            df_object = df_object.append(c.fetchall(), ignore_index=True)

        df_object.rename(columns={0: 'Appointment ID', 1: 'Time', 2: 'Appointment Status'},
                         inplace=True)

        # Boolean creation
        # if conflict exists = True, else = False
        if len(df_object.index) >= 1:
            boolean = True
        elif len(df_object.index) == 0:
            boolean = False

        conn.close()

        df_print = df_object.to_markdown(tablefmt="grid", index=False)

        return boolean, df_object, df_print

    @staticmethod  # INSERT insert_timeoff - STATIC
    ## TODO: Exception handling is done for weekend, appointments (booked, confirmed)
    def insert_timeoff(gp_id, timeoff_type, start_date, end_date):
        '''
        Insert time off or sick leave into booking table for custom time period.
        Only time slots during working hours are added.
        :param gp_id: gp_id that is stored in database/db_comp0066.db
        :param timeoff_type: 'sick leave' or 'time off'
        :param start_date: e.g. 2020-12-8
        :param end_date: e.g. 2020-12-10
        :return: 'time off was inserted'
        '''
        schedule = Schedule()
        if schedule.check_timeoff_conflict(gp_id=gp_id, start_date=start_date, end_date=end_date)[0] == False:

            # start_date transformation str to datetime
            start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')
            # adding time: '%Y-%m-%d 08:00'
            start_date = datetime.datetime.combine(start_date.date(), datetime.time(8, 0))

            # end_date transformation str to datetime
            end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d')
            # adding time: '%Y-%m-%d 16:50'
            end_date = datetime.datetime.combine(end_date.date(), datetime.time(16, 50))

            # Handling Working Days
            # Initialize query
            working_day_query = """
                                    SELECT
                                        gp_working_days
                                    FROM
                                        gp
                                    WHERE
                                        gp_id == {};""".format(gp_id)
            # Execute query
            working_day = u.db_read_query(working_day_query).loc[0, 'gp_working_days']

            # Extracts GP weekends according to his/her working days
            weekend_day_range = [(working_day + 5) % 7, (working_day + 6) % 7]

            # Range of 10 min slots from start_date to end_date
            timeoff_range = pd.date_range(start_date, end_date, freq='10min').strftime('%Y-%m-%d %H:%M').tolist()

            # Selection of weekdays (non weekend) slots only
            weekdays_only_helper = []
            for i in range(len(timeoff_range)):
                if datetime.datetime.strptime(timeoff_range[i][:10], '%Y-%m-%d').weekday() not in weekend_day_range:
                    weekdays_only_helper.append(i)

            timeoff_range_weekdays_only = [timeoff_range[i] for i in weekdays_only_helper]

            # Getting rid of 10 min slots from timeoff_range_weekdays_only and initializing new_timeoff_range
            new_timeoff_range = []
            for i in range(len(timeoff_range_weekdays_only)):
                if '08:00' <= timeoff_range_weekdays_only[i][11:] <= '16:50':
                    new_timeoff_range.append(timeoff_range_weekdays_only[i])

            # Insert into database
            for i in range(len(new_timeoff_range)):
                # Initialize query
                insert_timeoff_query = '''
                                        INSERT INTO
                                            booking (booking_id,
                                            booking_start_time,
                                            booking_status,
                                            booking_status_change_time,
                                            booking_agenda,
                                            booking_type,
                                            booking_notes,
                                            gp_id,
                                            patient_id)
                                        VALUES
                                            (NULL, '{}', '{}', '{}', NULL, NULL, NULL, {}, NULL);'''.format(
                    new_timeoff_range[i], timeoff_type, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), gp_id)
                # Execute query
                u.db_execute(insert_timeoff_query)

            return 'time off was inserted'

        # If there are already booked or confirmed appointments during start_date to end_date
        else:

            print('The timeoffs conflict with existing database entries!')

            return schedule.check_timeoff_conflict(gp_id=gp_id, start_date=start_date, end_date=end_date)

    @staticmethod  # DELETE delete_timeoff - STATIC
    ## TODO: only if requested by user flow team: make timeoff_type=None
    def delete_timeoff(gp_id, type, timeoff_type, start_date=None, end_date=None):
        '''
        Deletes timeoff from database (either all or for a custom date range.
        :param gp_id: gp_id that is stored in database/db_comp0066.db
        :param type: 'all' to delete all upcoming timeoffs or 'custom' to delete timeoffs during a certain time period
        :param timeoff_type: 'sick leave' or 'time off'
        :param start_date: e.g. 2020-12-8
        :param end_date: e.g. 2020-12-10
        :return: success string
        '''

        # Delete for a custom date range (start_date to end_date)
        if type == 'custom':

            # start_date transformation str to datetime
            start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')
            # adding time: '%Y-%m-%d 08:00'
            start_date = datetime.datetime.combine(start_date.date(), datetime.time(8, 0))

            # end_date transformation str to datetime
            end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d')
            # adding time: '%Y-%m-%d 16:50'
            end_date = datetime.datetime.combine(end_date.date(), datetime.time(16, 50))

            # Range of 10 min slots from start_date to end_date
            timeoff_range = pd.date_range(start_date, end_date, freq='10min').strftime('%Y-%m-%d %H:%M').tolist()

            # Deletion of 10 min slots that are outside of GP working hours
            new_timeoff_range = []
            for i in range(0, len(timeoff_range)):
                if '08:00' <= timeoff_range[i][11:] <= '16:50':
                    new_timeoff_range.append(timeoff_range[i])

            # delete from database
            for i in range(0, len(new_timeoff_range)):
                # Initialize query
                delete_timeoff_days_query = '''
                                            DELETE FROM
                                                booking
                                            WHERE
                                                strftime('%Y-%m-%d %H:%M', booking_start_time) = '{}'
                                            AND
                                                booking_status = '{}'
                                            AND
                                                gp_id = {};'''.format(new_timeoff_range[i], timeoff_type, gp_id)
                # Execute query
                u.db_execute(delete_timeoff_days_query)

            return 'timeoffs were deleted for your indicated time period'

        # Delete all upcoming timeoffs
        elif type == 'all':
            # Initialize query
            delete_timeoff_all_query = '''
                                        DELETE FROM
                                            booking
                                        WHERE
                                            strftime('%Y-%m-%d %H:%M', booking_start_time) >= '{}'
                                        AND
                                            booking_status = '{}'
                                        AND
                                            gp_id = {};'''.format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                                                  timeoff_type, gp_id)
            # Execute query
            u.db_execute(delete_timeoff_all_query)

            return 'all upcoming timeoffs were deleted'


### DEVELOPMENT ###

if __name__ == "__main__":
    pass

# ### TESTING ###
# # call classes
# schedule = Schedule()
#
# ## testing select day
# df = schedule.select(2, 'day', '2020-12-1')[1]
#
# ## testing select week
# schedule.select(2, 'week', '2021-1-18')
#
# ## testing check_timeoff_conflict
# df = schedule.check_timeoff_conflict(2, '2020-12-01', '2021-1-13')[2]
#
# ## testing select_upcoming_timeoff
# schedule.select_upcoming_timeoff(2)
#
# ## testing insert_timeoff_custom --> check_timeoff_conflict False
# schedule.insert_timeoff(2, 'sick leave', '2020-12-23', '2021-01-23')
#
# ## testing insert_timeoff_custom --> check_timeoff_conflict True
# schedule.insert_timeoff(2, 'sick leave', '2020-12-1', '2021-12-23')
#
# ## testing delete_timeoff custom
# schedule.delete_timeoff(gp_id=2, type='custom', timeoff_type='sick leave', start_date='2021-1-20', end_date='2021-1-25')
#
# ## testing delete_timeoff all
# schedule.delete_timeoff(gp_id=2, type='all', timeoff_type='sick leave')
