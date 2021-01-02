from system import password_reset as pw_reset
from system import utils as u

random_string_password_reset = pw_reset.random_string(8)
user_email = 'manuel.buri@gmail.com'
user_type = 'patient'
new_password = u.hash_salt('hahafasfa')

# Call after definition of variables above (otherwise one does not know which random_string to enter for validation)
pw_reset.send_code_to_registered_user(user_type, user_email, random_string_password_reset)
pw_reset.change_password(user_type, user_email, new_password, random_string_password_reset)
