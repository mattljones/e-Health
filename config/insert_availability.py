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
        '2020-12-09 15:00:00',
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
today_10min_split = today.strftime("%Y-%m-%d 8:00")
day_name = today.strftime("%A")

rng = pd.date_range(today_10min_split, periods=54, freq='10T')
df_raw = pd.DataFrame({ 'availability_start_time': rng})


# Read sqlite query results into a pandas DataFrame
conn = sqlite3.connect("database/db_comp0066.db")
df_db = pd.read_sql_query("SELECT availability_start_time, availability_status, availability_agenda FROM availability;", conn)
conn.close()

# change data type to perform join
df_db.availability_start_time = df_db.availability_start_time.astype('datetime64[ns]')

# perform join
df_new = pd.merge(df_raw, df_db, on='availability_start_time', how='left')
# replace nan values with 'Available'
df_new["availability_status"].fillna("Available", inplace = True)






