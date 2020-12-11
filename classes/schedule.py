# schedule.py

# import libraries
import pandas as pd
import sqlite3 as sql
import datetime
from tabulate import tabulate


class Schedule:
    '''
    Class defining all 'schedule' related methods.
    '''

    @staticmethod  # SELECT day - STATIC
    def select_day(gp_id, date):
        '''
        Selection of all database entries for a specific day
        :param gp_id: gp_id from database
        :param date: date as string in Format (YYYY-MM-D(D))
        :return: DataFrame containing all slots of a day showing that is available (nan values) and what not
        '''
        # this is in format '%Y-%m-%d %H:%M:%S' and cannot be changed
        date_values = datetime.datetime.strptime(date, '%Y-%m-%d')
        # this is the same date as below but in format '%Y-%m-%d'
        day_selection = date_values.date()

        # database queries
        conn = sql.connect("database/db_comp0066.db")
        schedule_day = pd.read_sql_query(
            "SELECT strftime('%Y-%m-%d', availability_start_time) av_dates, strftime('%H:%M', availability_start_time) av_hours, availability_status, availability_agenda, availability_type, patient_id FROM availability WHERE gp_id = ? AND av_dates = ?;",
            conn, params=(gp_id, day_selection))
        conn.close()

        # DataFrame Production
        # Producing the DF for a day
        today = datetime.date.today()
        today_10min_split = today.strftime("%Y-%m-%d 8:00")

        # produce a DateTimeIndex of daily_slots
        daily_slots = pd.date_range(today_10min_split, periods=54, freq='10T')
        df_raw = pd.DataFrame({'availability_start_time': daily_slots})

        # transform datatype to be able to join later
        schedule_day.av_hours = schedule_day.av_hours.astype('datetime64[ns]')

        # perform join
        df_select_day = pd.merge(df_raw, schedule_day, left_on='availability_start_time', right_on='av_hours',
                                 how='left')

        # drop av_dates and av_hours as they are not needed anymore
        df_select_day = df_select_day.drop(columns=['av_dates', 'av_hours'])

        # primitive fillna for the moment
        df_select_day = df_select_day.fillna("")

        return print(tabulate(df_select_day, headers='keys', tablefmt='psql'))

    @staticmethod  # SELECT week - STATIC
    def select_week(gp_id, year, month, day):
        '''

        :param gp_id:
        :param date_day1:
        :return:
        '''
        # creates a df with groups of columns as days (e.g. time, status)
        # day_selection = datetime.date(year, month, day)
        # week_selection = pd.date_range(start=date_day1, periods=7, freq='d')
        # conn = sql.connect("database/db_comp0066.db")
        # schedule_day = pd.read_sql_query("SELECT strftime('%Y-%m-%d', availability_start_time) av_t, availability_status, availability_agenda, availability_type, patient_id FROM availability WHERE gp_id = ? AND av_t = ?;", conn, params=(1, week_selection))
        # conn.close()
        # return schedule_week
        pass

    @staticmethod  # COMBINED SELECT
    def select_custom(gp_id, **kwargs):
        if len(kwargs) == 1:
            # select_day, defined here or elsewhere
            return len(kwargs)
        if len(kwargs) == 2:
            # select_week or select_custom, possibly with intelligent sizing based on # days, defined here or elsewhere
            return len(kwargs)
        pass

    @staticmethod  # SELECT select_upcoming_timeoff - STATIC
    def select_upcoming_timeoff(gp_id):
        '''
        Select all upcoming time offs (sick leave and time off) for a gp
        :param gp_id: gp_id that is stored in database/db_comp0066.db
        :return: DataFrame with upcoming timeoffs of a specific gp
        '''
        current_time = datetime.datetime.now()
        conn = sql.connect("database/db_comp0066.db")
        upcoming_timeoff = pd.read_sql_query(
            "SELECT availability_start_time AS av_t, availability_status, availability_agenda, availability_type, patient_id FROM availability WHERE gp_id = ? AND av_t >= ? AND availability_status IN ('time off', 'sick leave');",
            conn, params=(gp_id, current_time))
        conn.close()
        return print(tabulate(upcoming_timeoff, headers='keys', tablefmt='psql'))

    @staticmethod  # SELECT select_upcoming_timeoff - STATIC
    # TODO: whole method
    def check_timeoff_conflict(gp_id, start_date, end_date):
        '''

        :param gp_id:
        :param start_date:
        :param end_date:
        :return: BOOLean
        '''

        pass

    @staticmethod  # INSERT insert_timeoff_day  - STATIC
    ## TODO: prevent insertion for non-working hours slots
    def insert_timeoff_day(gp_id, timeoff_type, date):
        '''
        Insert a time off (sick leave or time off) for a whole day for a gp
        :param gp_id: gp_id that is stored in database/db_comp0066.db
        :param timeoff_type: 'sick leave' or 'time off'
        :param date: date as string in Format (YYYY-MM-D(D))
        :return: 'daily insertion done'
        '''

        # this is in format '%Y-%m-%d %H:%M:%S' and cannot be changed
        date_values = datetime.datetime.strptime(date, '%Y-%m-%d')
        # this is the same date as below but in format '%Y-%m-%d'
        day_selection = datetime.datetime.combine(date_values.date(), datetime.time(8, 0))
        timeoff_range = pd.date_range(day_selection, periods=54, freq='10T').strftime('%Y-%m-%d %H:%M').tolist()

        # connection to database
        conn = sql.connect("database/db_comp0066.db")
        # Create cursor
        c = conn.cursor()
        # insert into database
        for i in range(0, len(timeoff_range)):
            c.execute("""
                            INSERT INTO
                                availability (
                                availability_id,
                                availability_start_time,
                                availability_status,
                                availability_status_change_time,
                                availability_agenda,
                                availability_type,
                                availability_notes,
                                gp_id,
                                patient_id)
                            VALUES
                                (NULL,
                                ?,
                                ?,
                                datetime('now'),
                                NULL,
                                NULL,
                                NULL,
                                ?,
                                NULL);""", (timeoff_range[i], timeoff_type, gp_id))

        conn.commit()
        conn.close()

        return 'daily insertion done'

    @staticmethod  # INSERT insert_timeoff_day  - STATIC
    ## TODO: whole method
    def insert_timeoff_week(gp_id, timeoff_type, day1):
        pass

    @staticmethod  # INSERT insert_timeoff_custom  - STATIC
    ## TODO: prevent insertion for non-working hours slots
    def insert_timeoff_custom(gp_id, timeoff_type, start_date, end_date):
        '''
        Insert time off or sick leave into availability table.
        :param gp_id: gp_id that is stored in database/db_comp0066.db
        :param timeoff_type: 'sick leave' or 'time off'
        :param start_date: e.g. 2020-12-8 8:00
        :param end_date: e.g. 2020-12-8 15:00
        :return: DataFrame with upcoming timeoffs of a specific gp
        '''

        timeoff_range = pd.date_range(start_date, end_date, freq='10min').strftime('%Y-%m-%d %H:%M').tolist()
        # connection to database
        conn = sql.connect("database/db_comp0066.db")
        # Create cursor
        c = conn.cursor()
        # insert into database
        for i in range(0, len(timeoff_range)):
            c.execute("""
                    INSERT INTO
                        availability (
                        availability_id,
                        availability_start_time,
                        availability_status,
                        availability_status_change_time,
                        availability_agenda,
                        availability_type,
                        availability_notes,
                        gp_id,
                        patient_id)
                    VALUES
                        (NULL,
                        ?,
                        ?,
                        datetime('now'),
                        NULL,
                        NULL,
                        NULL,
                        ?,
                        NULL);""", (timeoff_range[i], timeoff_type, gp_id))

        conn.commit()
        conn.close()

        return 'custom insertion done'

    @staticmethod  # DELETE all - STATIC
    ## TODO: maybe limit it to only future timeoffs and make timeoff_type optional
    def delete_timeoff_all(gp_id, timeoff_type):
        '''
        Deletes all timeoff of availability_status = 'timeoff_type' entries in availability table
        :param gp_id: gp_id that is stored in database/db_comp0066.db
        :param timeoff_type: 'sick leave' or 'time off'
        :return: 'all entries were deleted'
        '''
        # connection to database
        conn = sql.connect("database/db_comp0066.db")
        # Create cursor
        c = conn.cursor()
        c.execute('''
            DELETE FROM
                availability
            WHERE
                availability_status = ?
            AND
                gp_id = ?;''', (timeoff_type, gp_id))
        conn.commit()
        conn.close()
        return 'all entries were deleted'

    @staticmethod  # DELETE day - STATIC
    ## TODO: maybe limit it to only future timeoffs, make timeoffs specific and make timeoff_type optional
    def delete_timeoff_day(gp_id, timeoff_type, date):
        '''
        Deletes all time off of availability_status = 'timeoff_type' entries in availability table for the given date
        :param gp_id: gp_id that is stored in database/db_comp0066.db
        :param timeoff_type: 'sick leave' or 'time off'
        :param date: date as string in Format (YYYY-MM-D(D))
        :return: DataFrame with upcoming timeoffs of a specific gp
        '''
        # this is in format '%Y-%m-%d %H:%M:%S' and cannot be changed
        date_values = datetime.datetime.strptime(date, '%Y-%m-%d')
        # this is the same date as below but in format '%Y-%m-%d'
        day_selection = date_values.date()

        # connection to database
        conn = sql.connect("database/db_comp0066.db")
        # Create cursor
        c = conn.cursor()
        c.execute('''
                DELETE FROM
                    availability
                WHERE
                    strftime('%Y-%m-%d', availability_start_time) = ?
                AND    
                    availability_status = ?
                AND
                    gp_id = ?;''', (day_selection, timeoff_type, gp_id))
        conn.commit()
        conn.close()
        return 'all entries for that day were deleted'

    @staticmethod  # DELETE week - STATIC
    ## TODO: whole method
    def delete_timeoff_week():
        pass

    @staticmethod  # DELETE custom - STATIC
    ## TODO: whole method
    def delete_timeoff_custom():
        pass


### DEVELOPMENT ###

if __name__ == "__main__":
    pass

### TESTING ###
# call classes
schedule = Schedule()

## testing select_day
schedule.select_day(1, '2020-12-9')

## testing select_upcoming_timeoff
schedule.select_upcoming_timeoff(1)

## testing insert_timeoff_day
schedule.insert_timeoff_day(1, 'sick leave', '2020-12-10')

## testing insert_timeoff_custom
schedule.insert_timeoff_custom(1, 'time off', '2020-12-11 8:00', '2020-12-13 15:00')

## testing delete_timeoff_all
schedule.delete_timeoff_all(1, 'sick leave')

## testing delete_timeoff_day
schedule.delete_timeoff_day(1, 'time off', '2020-12-13')
