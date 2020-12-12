# schedule.py

# import libraries
import pandas as pd
import sqlite3 as sql
import datetime


class Schedule:
    '''
    Class defining all 'schedule' related methods.
    '''

    @staticmethod  # SELECT day - STATIC
    # TODO: make nice and insert working days (or remove join again)
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
        # "SELECT strftime('%Y-%m-%d', booking_start_time) booking_dates, strftime('%Y-%m-%d %H:%M', booking_start_time) booking_hours, booking_status AS 'Booking Status', booking_agenda AS 'Agenda', booking_type AS 'Type', patient_id AS 'Patient ID' FROM booking WHERE gp_id = ? AND booking_dates = ?;"
        # database queries
        conn = sql.connect("database/db_comp0066.db")
        schedule_day = pd.read_sql_query(
            "Select strftime('%Y-%m-%d', booking_start_time) booking_dates, strftime('%Y-%m-%d %H:%M', booking_start_time) booking_hours, booking_status AS 'Booking Status', booking_agenda AS 'Agenda', booking_type AS 'Type', patient_id AS 'Patient ID', gp_working_days AS 'Working Days' FROM booking b left join gp g on b.gp_id = g.gp_id WHERE b.gp_id = ? AND booking_dates = ?;",
            conn, params=(gp_id, day_selection))
        conn.close()

        # Producing the empty DataFrame for a day
        date_for_splits = datetime.datetime.combine(date_values.date(), datetime.time(8, 0))
        # produce a DateTimeIndex of daily_slots
        daily_slots = pd.date_range(date_for_splits, periods=54, freq='10T')
        # Putting it together
        df_raw = pd.DataFrame({'Booking Start Time': daily_slots})

        # transform datatype to be able to join later
        schedule_day.booking_hours = schedule_day.booking_hours.astype('datetime64[ns]')

        # perform join
        df_select_day = pd.merge(df_raw, schedule_day, left_on='Booking Start Time', right_on='booking_hours', how='left')

        # drop booking_dates and booking_hours as they are not needed anymore
        df_select_day = df_select_day.drop(columns=['booking_dates', 'booking_hours'])

        # primitive fillna for the moment
        df_select_day = df_select_day.fillna("")

        df_formatted = df_select_day.to_markdown(tablefmt="grid", index=True)

        return df_formatted

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
        # schedule_day = pd.read_sql_query("SELECT strftime('%Y-%m-%d', booking_start_time) av_t, booking_status, booking_agenda, booking_type, patient_id FROM booking WHERE gp_id = ? AND av_t = ?;", conn, params=(1, week_selection))
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
        conn = sql.connect("database/db_comp0066.db")
        upcoming_timeoff = pd.read_sql_query(
            "SELECT booking_start_time AS 'Booking Start Time', booking_status AS 'Status', booking_agenda AS 'Agenda', booking_type AS 'Type', patient_id AS 'Patient ID' FROM booking WHERE gp_id = ? AND 'Booking Start Time' >= ? AND booking_status IN ('time off', 'sick leave');",
            conn, params=(gp_id, datetime.datetime.now()))
        conn.close()

        df_formatted = upcoming_timeoff.to_markdown(tablefmt="grid", index=True)

        return df_formatted

    @staticmethod  # SELECT check_timeoff_conflict - STATIC
    # TODO: whole method
    def check_timeoff_conflict(gp_id, start_date, end_date):
        '''
        Checks if a gp has no time off during a specific time period and returns a Boolean.
        :param gp_id: gp_id that is stored in database/db_comp0066.db
        :param start_date: e.g. 2020-12-8 8:00
        :param end_date: e.g. 2020-12-8 15:00
        :return: BOOLean: 'True' if there was a conflict, 'False' is there was no conflict
        '''

        # Range of 10 min slots from start_date to end_date
        timeoff_range = pd.date_range(start_date, end_date, freq='10min').strftime('%Y-%m-%d %H:%M').tolist()

        # Deletion of 10 min slots that are outside of GP working hours
        new_timeoff_range = []
        for i in range(0, len(timeoff_range)):
            if '08:00' <= timeoff_range[i][11:] <= '16:50':
                new_timeoff_range.append(timeoff_range[i])

        # connection to database
        conn = sql.connect("database/db_comp0066.db")
        # Create cursor
        c = conn.cursor()
        # insert into database
        for i in range(0, len(new_timeoff_range)):
            c.execute("""
                        SELECT booking_start_time, booking_status
                        FROM booking
                        WHERE strftime('%Y-%m-%d %H:%M', booking_start_time) = ? AND gp_id = ? AND booking_status IN ('time off', 'sick leave');""", (new_timeoff_range[i], gp_id))

        query_result = c.fetchall()

        if len(query_result) >= 1:
            result = True
        elif len(query_result) == 0:
            result = False
        conn.close()

        return result



    @staticmethod  # INSERT insert_timeoff_day  - STATIC
    # TODO: not relevant right now focusing on custom insertion
    # TODO: prevent insertion for non-working hours slots
    # at the moment not really relevant as it is super nice if doctors can insert custom time offs
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
                                booking (
                                booking_id,
                                booking_start_time,
                                booking_status,
                                booking_status_change_time,
                                booking_agenda,
                                booking_type,
                                booking_notes,
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

    @staticmethod  # INSERT insert_timeoff_week  - STATIC
    ## TODO not relevant right now focusing on custom insertion
    # TODO: whole method
    def insert_timeoff_week(gp_id, timeoff_type, day1):
        pass

    @staticmethod  # INSERT insert_timeoff_custom  - STATIC
    def insert_timeoff_custom(gp_id, timeoff_type, start_date, end_date):
        '''
        Insert time off or sick leave into booking table for custom time period.
        Only time slots during working hours are added.
        :param gp_id: gp_id that is stored in database/db_comp0066.db
        :param timeoff_type: 'sick leave' or 'time off'
        :param start_date: e.g. 2020-12-8 8:00
        :param end_date: e.g. 2020-12-8 15:00
        :return: DataFrame with upcoming timeoffs of a specific gp
        '''
        # Range of 10 min slots from start_date to end_date
        timeoff_range = pd.date_range(start_date, end_date, freq='10min').strftime('%Y-%m-%d %H:%M').tolist()

        # Deletion of 10 min slots that are outside of GP working hours
        new_timeoff_range = []
        for i in range(0, len(timeoff_range)):
            if '08:00' <= timeoff_range[i][11:] <= '16:50':
                new_timeoff_range.append(timeoff_range[i])

        # connection to database
        conn = sql.connect("database/db_comp0066.db")
        # Create cursor
        c = conn.cursor()
        # insert into database
        for i in range(0, len(new_timeoff_range)):
            c.execute("""
                            INSERT INTO
                                booking (booking_id, booking_start_time, booking_status, booking_status_change_time, booking_agenda, booking_type, booking_notes, gp_id, patient_id)
                            VALUES
                                (NULL, ?, ?, datetime('now'), NULL, NULL, NULL, ?, NULL);""", (new_timeoff_range[i], timeoff_type, gp_id))

        conn.commit()
        conn.close()

        return 'custom time_off insertion done'

    @staticmethod  # DELETE all - STATIC
    ## TODO: limit it to only future timeoffs
    def delete_timeoff_all(gp_id, timeoff_type):
        '''
        Deletes all timeoff of booking_status = 'timeoff_type' entries in booking table
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
                booking
            WHERE
                booking_status = ?
            AND
                strftime('%Y-%m-%d', booking_start_time) > datetime.datetime.today()
            AND
                gp_id = ?;''', (timeoff_type, gp_id))
        conn.commit()
        conn.close()
        return 'all entries were deleted'

    @staticmethod  # DELETE day - STATIC
    ## TODO --> not really relevant for now
    # TODO: maybe limit it to only future timeoffs
    def delete_timeoff_day(gp_id, timeoff_type, date):
        '''
        Deletes all time off of booking_status = 'timeoff_type' entries in booking table for the given date
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
                    booking
                WHERE
                    strftime('%Y-%m-%d', booking_start_time) = ?
                AND    
                    booking_status = ?
                AND
                    gp_id = ?;''', (day_selection, timeoff_type, gp_id))
        conn.commit()
        conn.close()
        return 'all entries for that day were deleted'

    @staticmethod  # DELETE week - STATIC
    ## TODO --> not really relevant for now
    ## TODO: whole method
    def delete_timeoff_week():
        pass

    @staticmethod  # DELETE custom - STATIC
    def delete_timeoff_custom(gp_id, timeoff_type, start_date, end_date):
        '''
        Deletes time off or sick leave in booking table for custom time period.
        Only time slots during working hours are affected.
        :param gp_id: gp_id that is stored in database/db_comp0066.db
        :param timeoff_type: 'sick leave' or 'time off'
        :param start_date: e.g. 2020-12-8 8:00
        :param end_date: e.g. 2020-12-8 15:00
        :return: 'all timeoffs for the customs date range were deleted'
        '''
        # Range of 10 min slots from start_date to end_date
        timeoff_range = pd.date_range(start_date, end_date, freq='10min').strftime('%Y-%m-%d %H:%M').tolist()

        # Deletion of 10 min slots that are outside of GP working hours
        new_timeoff_range = []
        for i in range(0, len(timeoff_range)):
            if '08:00' <= timeoff_range[i][11:] <= '16:50':
                new_timeoff_range.append(timeoff_range[i])

        # connection to database
        conn = sql.connect("database/db_comp0066.db")
        # Create cursor
        c = conn.cursor()

        # connection to database
        conn = sql.connect("database/db_comp0066.db")
        # Create cursor
        c = conn.cursor()

        for i in range(0, len(new_timeoff_range)):
            c.execute('''
                            DELETE FROM booking
                            WHERE strftime('%Y-%m-%d %H:%M', booking_start_time) = ?
                            AND booking_status = ?
                            AND gp_id = ?;''', (new_timeoff_range[i], timeoff_type, gp_id))

        conn.commit()
        conn.close()

        return 'all timeoffs for the customs date range were deleted'


### DEVELOPMENT ###

if __name__ == "__main__":
    pass

### TESTING ###
# call classes
schedule = Schedule()

## testing select_day
schedule.select_day(1, '2020-12-1')

## testing select_upcoming_timeoff
schedule.select_upcoming_timeoff(1)

## testing insert_timeoff_day
schedule.insert_timeoff_day(1, 'sick leave', '2020-12-10')

## testing insert_timeoff_custom
schedule.insert_timeoff_custom(2, 'time off', '2021-1-11 8:00', '2021-1-13 15:00')

## testing delete_timeoff_all
schedule.delete_timeoff_all(1, 'sick leave')

## testing delete_timeoff_day
schedule.delete_timeoff_day(1, 'time off', '2020-12-13')

## testing delete_timeoff_custom
schedule.delete_timeoff_custom(2, 'time off', '2021-1-11 8:00', '2021-1-13 15:00')


start_date = '2021-12-11 8:00'
end_date = '2021-12-13 15:00'
gp_id = 2

# Range of 10 min slots from start_date to end_date
timeoff_range = pd.date_range(start_date, end_date, freq='10min').strftime('%Y-%m-%d %H:%M').tolist()

# Deletion of 10 min slots that are outside of GP working hours
new_timeoff_range = []
for i in range(0, len(timeoff_range)):
    if '08:00' <= timeoff_range[i][11:] <= '16:50':
        new_timeoff_range.append(timeoff_range[i])

# connection to database
conn = sql.connect("database/db_comp0066.db")
# Create cursor
c = conn.cursor()
# insert into database
for i in range(0, len(new_timeoff_range)):
    c.execute("""
                SELECT booking_start_time, booking_status
                FROM booking
                WHERE strftime('%Y-%m-%d %H:%M', booking_start_time) = ? AND gp_id = ? AND booking_status IN ('time off', 'sick leave');""", (new_timeoff_range[i], gp_id))

query_result = c.fetchall()

if len(query_result) >= 1:
    result = True
elif len(query_result) == 0:
    result = False
conn.close()