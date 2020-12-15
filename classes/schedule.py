# schedule.py

# import libraries
import pandas as pd
import sqlite3 as sql
import datetime

# from system import utils as u

# TODO delete lines 10 to 86 once import of utils works fine
# TODO for now LUNCH and WEEKEND is not capitalized in appointment.py

def week_empty_df(start_date, gp_id):
    days = pd.date_range(start=start_date, periods=7, freq='D')
    times = pd.date_range(start='08:00:00', periods=54, freq='10Min')  # .to_frame(name='Working Hours',index=False)
    week_df = pd.DataFrame(index=times.strftime('%H:%M'), columns=days.date)

    working_day_query = """SELECT gp_working_days FROM gp where gp_id == {};""".format(gp_id)
    working_day = db_read_query(working_day_query).loc[
        0, 'gp_working_days']  # will need a query to pull the first working day for a specific GP

    # This part of the code works out when the GP has weekends and populates those days with status "Weekend"
    weekend_day_range = [(working_day + 5) % 7, (working_day + 6) % 7]

    # Inserting 'Lunch Time'
    if (gp_id % 2) == 0:
        week_df.loc[datetime.datetime.strptime('12:00', '%H:%M').strftime('%H:%M')
                    :datetime.datetime.strptime('12:50', '%H:%M').strftime('%H:%M')] = 'LUNCH'
    elif (gp_id % 2) != 0:
        week_df.loc[datetime.datetime.strptime('13:00', '%H:%M').strftime('%H:%M')
                    :datetime.datetime.strptime('13:50', '%H:%M').strftime('%H:%M')] = 'LUNCH'

    # Inserting 'Weekend'
    for i in range(7):
        if week_df.columns[i].weekday() in weekend_day_range:
            week_df[week_df.columns[i]] = 'WEEKEND'

    week_df = week_df.fillna(" ")

    return week_df


def db_execute(query):
    conn = sql.connect('database/db_comp0066.db')
    c = conn.cursor()
    c.execute(query)
    # Commit to db
    conn.commit()
    # Close db
    conn.close()




def db_read_query(query):
    conn = sql.connect("database/db_comp0066.db")
    result = pd.read_sql_query(query, conn)
    conn.close()
    return result


def day_empty_df(date, gp_id):
    times = pd.date_range(start='08:00', periods=54, freq='10Min').strftime('%H:%M')
    date = pd.date_range(start=date, periods=1, freq='D')
    day_df = pd.DataFrame(index=times, columns=date.date)

    # Handling lunch time
    if (gp_id % 2) == 0:
        day_df.loc['12:00':'12:50'] = 'LUNCH'
    else:
        day_df.loc['13:00':'13:50'] = 'LUNCH'

    # Handling Working Days
    working_day_query = """SELECT gp_working_days FROM gp where gp_id == {};""".format(gp_id)
    working_day = db_read_query(working_day_query).loc[
        0, 'gp_working_days']  # will need a query to pull the first working day for a specific GP

    # This part of the code works out when the GP has weekends and populates those days with status "Weekend"
    weekend_day_range = [(working_day + 5) % 7, (working_day + 6) % 7]

    if day_df.columns[0].weekday() in weekend_day_range:
        day_df[day_df.columns[0]] = 'WEKKEND'

    # Make df pretty
    day_df.columns.values[0] = "Status"
    day_df = day_df.fillna("")

    return day_df


# day_empty_df('2020-12-12',2)
# week_empty_df('2020-12-12',2)

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
            # this is in format '%Y-%m-%d'
            start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()

            # database queries
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

            sql_result_df = db_read_query(day_query)

            sql_result_df['Patient (ID)'] = sql_result_df['Patient First Name'].astype(str) + ' ' + sql_result_df['Patient Last Name'].astype(str) + ' (' + sql_result_df['Patient (ID)'].astype(str) + ')'

            # Producing the empty DataFrame for a day
            df_select_day_empty = day_empty_df(start_date, 2)

            df_object = pd.merge(df_select_day_empty,sql_result_df, left_on=df_select_day_empty.index, right_on='booking_hours', how='left')

            for i in range(len(df_object)):
                if pd.isnull(df_object.at[i, 'Booking Status Old']) == False:
                    df_object.at[i, 'Status'] = df_object.at[i, 'Booking Status Old']


            df_object = df_object.drop(columns=['Booking Status Old', 'booking_hours', 'Patient First Name', 'Patient Last Name']).fillna('')
            df_object = df_object.set_index(df_select_day_empty.index)

            # drop booking_dates and booking_hours as they are not needed anymore
            df_print = df_object.to_markdown(tablefmt="grid", index=True)

            return df_object, df_print

        if type == 'week':

            # Works out the end date for a week that was specified
            start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = start_date + datetime.timedelta(days=6)

            # SQLite query and forms a DF df_object with booking for a specific GP
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
            sql_result_df = db_read_query(week_query)

            # forms an empty DF for a week from the date specified for a specific GP
            df_object = week_empty_df(start_date, gp_id)

            # inserts all the data from the df_object into the empty week DF
            for i in range(len(sql_result_df)):
                date_column = datetime.datetime.strptime(sql_result_df.loc[i, 'start_date'], '%Y-%m-%d').date()
                time_row = datetime.datetime.strptime(sql_result_df.loc[i, 'time'], '%H:%M').strftime('%H:%M')
                df_object.loc[time_row, date_column] = sql_result_df.loc[i, 'booking_status']

            df_print = df_object.to_markdown(tablefmt="grid", index=True)
        return df_object, df_print


    @staticmethod  # SELECT select_upcoming_timeoff - STATIC
    def select_upcoming_timeoff(gp_id):
        '''
        Select all upcoming time offs (sick leave and time off) for a gp
        :param gp_id: gp_id that is stored in database/db_comp0066.db
        :return: DataFrame with upcoming timeoffs of a specific gp (non-formatted & formatted)
        '''
        upcoming_timeoff_query = '''
                                SELECT DISTINCT
                                    strftime('%Y-%m-%d', booking_start_time) AS 'Date',
                                    booking_status AS 'Timeoff Type'
                                FROM
                                    booking
                                WHERE
                                        gp_id = {}
                                  AND strftime('%Y-%m-%d', booking_start_time) >= '{}'
                                  AND booking_status IN ('time off', 'sick leave');'''.format(gp_id,
                                                                                              datetime.datetime.now().strftime("%Y-%m-%d"))

        df_object = db_read_query(upcoming_timeoff_query)

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

        # start_date
        start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')
        # this is the same date as below but in format '%Y-%m-%d'
        start_date = datetime.datetime.combine(start_date.date(), datetime.time(8, 0))

        # end_date
        end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d')
        # this is the same date as below but in format '%Y-%m-%d'
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
        # insert into database
        for i in range(len(new_timeoff_range)):
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
            # Appending to DataFrame
            df_object = df_object.append(c.fetchall(), ignore_index=True)

        df_object.rename(columns={0: 'Appointment ID', 1: 'Time', 2: 'Appointment Status'},
                                         inplace=True)

        if len(df_object.index) >= 1:
            boolean = True
        elif len(df_object.index) == 0:
            boolean = False

        conn.close()

        df_print = df_object.to_markdown(tablefmt="grid", index=False)

        return boolean, df_object, df_print

    @staticmethod  # INSERT insert_timeoff- STATIC
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

            # start_date
            start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')
            # this is the same date as below but in format '%Y-%m-%d'
            start_date = datetime.datetime.combine(start_date.date(), datetime.time(8, 0))

            # end_date
            end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d')
            # this is the same date as below but in format '%Y-%m-%d'
            end_date = datetime.datetime.combine(end_date.date(), datetime.time(16, 50))

            # Handling Working Days
            working_day_query = """SELECT gp_working_days FROM gp where gp_id == {};""".format(gp_id)
            working_day = db_read_query(working_day_query).loc[0, 'gp_working_days']

            # This part of the code works out when the GP has weekends and populates those days with status "Weekend"
            weekend_day_range = [(working_day + 5) % 7, (working_day + 6) % 7]

            # Range of 10 min slots from start_date to end_date
            timeoff_range = pd.date_range(start_date, end_date, freq='10min').strftime('%Y-%m-%d %H:%M').tolist()

            # Selection of weekdays (non weekend) slots only
            weekdays_only_helper = []
            for i in range(len(timeoff_range)):
                if datetime.datetime.strptime(timeoff_range[i][:10], '%Y-%m-%d').weekday() not in weekend_day_range:
                    weekdays_only_helper.append(i)

            timeoff_range_weekdays_only = [timeoff_range[i] for i in weekdays_only_helper]

            # Deletion of 10 min slots from timeoff_range_weekdays_only
            new_timeoff_range = []
            for i in range(len(timeoff_range_weekdays_only)):
                if '08:00' <= timeoff_range_weekdays_only[i][11:] <= '16:50':
                    new_timeoff_range.append(timeoff_range_weekdays_only[i])

            # insert into database
            for i in range(len(new_timeoff_range)):
                insert_timeoff_query = '''INSERT INTO
                                                                booking (booking_id, booking_start_time, booking_status, booking_status_change_time, booking_agenda, booking_type, booking_notes, gp_id, patient_id)
                                                            VALUES
                                                                (NULL, '{}', '{}', '{}', NULL, NULL, NULL, {}, NULL);'''.format(
                    new_timeoff_range[i], timeoff_type, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), gp_id)
                db_execute(insert_timeoff_query)

            return 'time off was inserted'

        else:

            print('The timeoffs conflict with existing database entries!')

            return schedule.check_timeoff_conflict(gp_id=gp_id, start_date=start_date, end_date=end_date)

    @staticmethod  # DELETE all - STATIC
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

            # start_date
            start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')
            # this is the same date as below but in format '%Y-%m-%d'
            start_date = datetime.datetime.combine(start_date.date(), datetime.time(8, 0))

            # end_date
            end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d')
            # this is the same date as below but in format '%Y-%m-%d'
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
                delete_timeoff_days_query = '''
                                            DELETE FROM
                                                booking
                                            WHERE
                                                strftime('%Y-%m-%d %H:%M', booking_start_time) = '{}'
                                            AND
                                                booking_status = '{}'
                                            AND
                                                gp_id = {};'''.format(new_timeoff_range[i], timeoff_type, gp_id)
                db_execute(delete_timeoff_days_query)

            return 'timeoffs were deleted for your indicated time period'

        # Delete all upcoming timeoffs
        elif type == 'all':

            delete_timeoff_all_query = '''
                                        DELETE FROM
                                            booking
                                        WHERE
                                            strftime('%Y-%m-%d %H:%M', booking_start_time) >= '{}'
                                        AND
                                            booking_status = '{}'
                                        AND
                                            gp_id = {};'''.format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), timeoff_type, gp_id)
            db_execute(delete_timeoff_all_query)

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
# schedule.select(2, 'week', '2021-1-20')
#
# ## testing check_timeoff_conflict
# df = schedule.check_timeoff_conflict(2, '2020-12-01', '2021-1-13')[2]
#
# ## testing select_upcoming_timeoff
# schedule.select_upcoming_timeoff(2)
#
# ## testing insert_timeoff_custom
# schedule.insert_timeoff(2, 'sick leave', '2020-12-23', '2021-02-23')
#
# ## testing delete_timeoff custom
# schedule.delete_timeoff(gp_id=2, type='custom', timeoff_type='sick leave', start_date='2021-1-20', end_date='2021-1-25')
#
# ## testing delete_timeoff all
# schedule.delete_timeoff(gp_id=2, type='all', timeoff_type='sick leave')
