# e_health_main.py

# library imports 
from pathlib import Path
import sys 

# Change python path for imports
p = Path(__file__).parents[1]
sys.path.insert(1, str(p))

# Importing utility methods from the 'system' package
from system import globals
from system import utils

# Importing menu paths for each user from the 'user_menu_flow' package
from user_menu_flow.register_login_flow import main_flow

############################# MAIN CODE ###############################

globals.init()
utils.display(main_flow)