# patient.py

# import libraries
import pandas as pd
import sqlite3 as sql
from pathlib import Path
import sys 

# Change python path for imports
p = Path(__file__).parents[1]
sys.path.insert(1, str(p))

# Import required modules and classes
from classes.user import User

class Patient(User):
    '''
    Class defining all 'patient' related methods.
    The patient class instantiates patient objects from the database.
    '''

    # Analogous to GP - will populate once GP method specifics are confirmed

    pass
    








### DEVELOPMENT ###

if __name__ == "__main__":

    p1 = Patient(2)
    print(p1)