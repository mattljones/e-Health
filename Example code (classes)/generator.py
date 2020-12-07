import sqlite3
import datetime
import pandas as pd

conn = sqlite3.connect("database.db")
c = conn.cursor()

c.execute("DROP TABLE IF EXISTS gp;")

c.execute('''CREATE TABLE gp (
                gp_id INTEGER PRIMARY KEY,
                first_name TEXT,
                last_name TEXT,
                gender INTEGER,
                birth_date TEXT,
                email TEXT,
                password TEXT,
                registration_date TEXT,
                specialisation_id INTEGER,
                department_id INTEGER,
                working_days INTEGER,
                status INTEGER
             )
         ''')

c.execute('''INSERT INTO gp VALUES (NULL,
                                    'Matt', 
                                    'Jones', 
                                    1, 
                                    '1991-08-12', 
                                    'ucabmlj@ucl.ac.uk',
                                    'test',
                                    '2020-12-07',
                                    1,
                                    1,
                                    1,
                                    1
                                    );
         ''')

c.execute("DROP TABLE IF EXISTS appointment;")

c.execute('''CREATE TABLE appointment (
                appointment_id INTEGER PRIMARY KEY,
                date TEXT,
                time TEXT,
                status INTEGER,
                status_change_timestamp TEXT,
                agenda TEXT,
                type TEXT,
                gp_notes TEXT,
                gp_id INTEGER,
                patient_id INTEGER
             );
         ''')

start = datetime.datetime(2020, 12, 7, 9)
end = datetime.datetime(2020, 12, 7, 18)
while start < end:
    c.execute('''INSERT INTO appointment VALUES (NULL,
                                                 ?,
                                                 ?,
                                                 0,
                                                 NULL,
                                                 NULL,
                                                 NULL,
                                                 NULL, 
                                                 1,
                                                 NULL
                                                 );''', (str(start)[0:10],str(start)[11:20]))
    start = start + datetime.timedelta(minutes = 10)

conn.commit()

appointment = pd.read_sql_query("SELECT * FROM appointment;", conn)
print(appointment)

conn.close()
