# import libraries
import pandas as pd
import datetime as dt
import sqlite3 as sql
# import calendar
from tabulate import tabulate


def db_execute(query):
    conn = sql.connect('../database/db_comp0066.db')
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


"""
week_empty_df function creates an empty dataframe that can get populated
using .loc pinpointing the date and time from the database
"""


def week_empty_df(start_date):
    days = pd.date_range(start=start_date, periods=7, freq='D')
    times = pd.date_range(start='08:00:00', periods=54, freq='10Min')  # .to_frame(name='Working Hours',index=False)
    df = pd.DataFrame(index=times.time, columns=days.date)
    return df


# This snippet of code fetches the bookings for a week specified
# In your method you will have to dynamically generate the the end date and
# input in into the SQL query

week_empt_df = week_empty_df('2020-12-08')
query = """SELECT date(booking_start_time) start_date,strftime('%H:%M:%S',booking_start_time) time,booking_status
           FROM booking
           WHERE gp_id = 10 AND start_date BETWEEN '{}' and '{}';""".format('2020-12-08', '2020-12-15')
sql_result_df = db_read_query(query)

# This snippet of code populates the empty week dataframe with bookings
for i in range(sql_result_df.shape[0]):
    date_column = dt.datetime.strptime(sql_result_df.loc[i, 'start_date'], '%Y-%m-%d').date()
    time_row = dt.datetime.strptime(sql_result_df.loc[i, 'time'], '%H:%M:%S').time()
    week_empt_df.loc[time_row, date_column] = sql_result_df.loc[i, 'booking_status']

#####################################
working_day = 0  # will need a query to pull the first working day for a specific GP

# This part of the code works out when the GP has weekends and populates those days with status "Weekend"
weekend_day_range = [(working_day + 5) % 7, (working_day + 6) % 7]
print(weekend_day_range)
for i in range(7):
    if week_empt_df.columns[i].weekday() in weekend_day_range:
        week_empt_df[week_empt_df.columns[i]] = 'Weekend'

week_empt_df = tabulate(week_empt_df.fillna(" "), headers='keys', tablefmt='psql')
print(week_empt_df)
