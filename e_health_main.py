# e_health_main.py

# Importing utility methods from the 'system' package
from system import globals
from system import utils
from system import asciiart

# Importing menu paths for each user from the 'user_menu_flow' package
from user_menu_flow.register_login_flow import main_flow_register

############################# MAIN CODE ###############################

globals.init()
print(asciiart.launch_art)

utils.display(main_flow_register)