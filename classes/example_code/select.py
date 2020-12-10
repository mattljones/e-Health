import sqlite3
import pandas as pd
import classes

# SELECTING Schedule - STATIC method
gp_id = input("Enter the gp_id: ")
date = input("Enter the date: ")
datetime = date + ""

schedule_day = classes.Schedule.select_day(gp_id, date)
print(schedule_day)
