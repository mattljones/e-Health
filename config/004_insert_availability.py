import sqlite3
import datetime

# Create connection to db
conn = sqlite3.connect('config/db_comp0066.db')

# Create cursor
c = conn.cursor()

# Insert into user
c.execute("""
    INSERT INTO
        availability (
        availability_status,
        availability_date,
        availability_status_change_time,
        availability_agenda,
        availability_start_time,
        availability_type,
        availability_notes,
        gp_id)
    VALUES
        ('available',
        datetime('now'),
        datetime('now'),
        'initial slot',
        datetime('now'),
        'offline',
        'its a test',
        2);
""")

# generate datelist
Today = datetime.datetime(2020, 12, 7, 8)
date_list = [Today + datetime.timedelta(minutes=10*x) for x in range(0, 55)]
# datetext=[x.strftime('%Y-%m-%d T%H:%M Z') for x in date_list]

c.execute("""
    INSERT INTO
        availability (
        availability_status,
        availability_date,
        availability_status_change_time,
        availability_agenda,
        availability_start_time,
        availability_type,
        availability_notes,
        gp_id)
    VALUES
        ('available',
        datetime.datetime(2020, 12, 7),
        datetime('now'),
        'initial slot',
        ?,
        'offline',
        'its a test',
        2)""", date_list)





# Check
print("Availability successfully inserted")

# Commit to db
conn.commit()

# Close db
conn.close()
