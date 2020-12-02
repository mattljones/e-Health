import pandas as pd
import sqlite3

# Read sqlite query results into a pandas DataFrame
conn = sqlite3.connect("config/db_comp0066.db")
df = pd.read_sql_query("select * from users;", conn)

# print df
print(df.head())

con.close()
