# e_health_main.py

# Importing built-in modules 
import os
import sys

# Importing utility methods from the 'system' package
from system import globals
from system import utils
from system import asciiart

# Importing menu paths for each user from the 'user_menu_flow' package
from user_menu_flow.register_login_flow import main_flow_register

############################# MAIN CODE ###############################

globals.init()
print(asciiart.launch_art)

try:
    utils.display(main_flow_register)
except KeyboardInterrupt:
    print("\n\n" + "=" * 65 + "\n")
    print("\U0001F51A THANK YOU FOR USING E-HEALTH. SEE YOU NEXT TIME!")
    print(asciiart.exit_art)
    try:
        sys.exit()
    except SystemExit:
        os._exit(0)