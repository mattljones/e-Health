## COMP0066 Coursework Group 7
# This script downs the sqlite database

# library imports
import sqlite3
from pathlib import Path
import sys

# Change python path for imports
package_dir = Path(__file__).parents[1]
sys.path.insert(0, str(package_dir))

try:
    # Create a database
    conn = sqlite3.connect('database/db_comp0066.db')

    # Create cursor
    c = conn.cursor()

    # Drop tables
    c.execute("""DROP TABLE IF EXISTS admin;""")
    c.execute("""DROP TABLE IF EXISTS gp;""")
    c.execute("""DROP TABLE IF EXISTS patient;""")
    c.execute("""DROP TABLE IF EXISTS booking;""")
    c.execute("""DROP TABLE IF EXISTS booking;""")
    c.execute("""DROP TABLE IF EXISTS gp_department;""")
    c.execute("""DROP TABLE IF EXISTS gp_specialisation;""")
    c.execute("""DROP TABLE IF EXISTS drug;""")
    c.execute("""DROP TABLE IF EXISTS prescription;""")
    c.execute("""DROP TABLE IF EXISTS patient_medical_condition_type;""")
    c.execute("""DROP TABLE IF EXISTS patient_medical_condition;""")

    # Return success message
    print("DB successfully dropped")

    # Commit to db
    conn.commit()

    # Close db
    conn.close()
except sqlite3.Error as e:
    print("An error occurred while taking down the database:", e.args[0])
except:
    print("An error occurred while taking down the database.")