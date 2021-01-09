# e_health_main.py

import pkg_resources
import subprocess
import sys
import os
required = {'pandas', 'tabulate'}
installed = {pkg.key for pkg in pkg_resources.working_set}
missing = required - installed

if missing:
    print('\n\nInstalling "Pandas" and "Tabulate" for a more pleasant user experience!\n\n')
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', *missing])


# Importing utility methods from the 'system' package
from system import globals
from system import utils
from system import asciiart

# Importing menu paths for each user from the 'user_menu_flow' package
from user_menu_flow.register_login_flow import main_flow_register

############################# MAIN CODE ###############################

os.system('clear')
globals.init()
print(asciiart.launch_art)

utils.display(main_flow_register)