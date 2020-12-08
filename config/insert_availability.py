import sqlite3
import datetime
import pandas as pd

# Create connection to db
conn = sqlite3.connect('database/db_comp0066.db')

# Create cursor
c = conn.cursor()

# Insert into user
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
        '2020-12-08 08:00:00',
        'booked',
        datetime('now'),
        'initial slot',
        'offline',
        'its a test',
        1,
        NULL);
""")

# Check
print("Availability successfully inserted")

# Commit to db
conn.commit()

# Close db
conn.close()


# Producing the DF for a day
today = datetime.date.today()
today_10min_split = today.strftime("%d-%m-%Y 8:00")
day_name = today.strftime("%A")

rng = pd.date_range(today_10min_split, periods=54, freq='10T')
df_raw = pd.DataFrame({ 'availability_start_time': rng, day_name : 'Availability' })


# Read sqlite query results into a pandas DataFrame
conn = sqlite3.connect("database/db_comp0066.db")
df_db = pd.read_sql_query("SELECT * FROM availability;", conn)

# print df
print(df.head())

conn.close()

## TODO: make a good join or merge
df_raw.merge(df_db, on='availability_start_time', how='left')




