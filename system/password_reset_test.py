# from system import password_reset as pw_reset
from system import utils as u

random_string_password_reset = u.random_string(8)
user_email = 'manuel.buri@gmail.com'
user_type = 'patient'

# Call after definition of variables above (otherwise one does not know which random_string to enter for validation)
u.send_code_to_registered_user(user_type, user_email, random_string_password_reset)
u.change_password(user_type, user_email, random_string_password_reset)
